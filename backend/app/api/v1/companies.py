"""
Company API endpoints
Handles company data, financials, and risk analysis
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_, desc, asc
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.company import Company, FinancialStatement, CashFlow, CompanyRiskScore
from app.schemas.company import (
    CompanyResponse,
    CompanyCreate,
    CompanyUpdate,
    CompanyDetailResponse,
    CompanyFinancialsResponse,
    CompanySearchParams,
    CompanySearchResult,
    CompanySearchResponse,
    CompanyComparisonRequest,
    CompanyComparisonResponse,
    CompanyIngestRequest,
    CompanyIngestResponse,
    CompanyRiskAnalysis,
)
from app.services.yahoo_finance import yahoo_client
from app.services.normalization import normalization_service
from app.services.company_risk import risk_scoring_service
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/search", response_model=CompanySearchResponse)
async def search_companies(
    query: Optional[str] = Query(None, description="Search by company name"),
    country_code: Optional[str] = Query(None, min_length=2, max_length=2),
    sector: Optional[str] = None,
    is_listed: Optional[bool] = None,
    min_risk_score: Optional[float] = Query(None, ge=0, le=100),
    max_risk_score: Optional[float] = Query(None, ge=0, le=100),
    sort_by: str = Query("name", regex="^(name|revenue|risk_score)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search companies with filters and pagination
    """
    # Build base query
    stmt = select(Company)
    
    # Apply filters
    filters = []
    if query:
        filters.append(Company.name.ilike(f"%{query}%"))
    if country_code:
        filters.append(Company.country_code == country_code.upper())
    if sector:
        filters.append(Company.sector.ilike(f"%{sector}%"))
    if is_listed is not None:
        filters.append(Company.is_listed == is_listed)
    
    if filters:
        stmt = stmt.where(and_(*filters))
    
    # Count total
    count_stmt = select(func.count()).select_from(Company).where(and_(*filters) if filters else True)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()
    
    # Apply sorting
    if sort_by == "name":
        stmt = stmt.order_by(asc(Company.name) if sort_order == "asc" else desc(Company.name))
    
    # Apply pagination
    stmt = stmt.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(stmt)
    companies = result.scalars().all()
    
    # Enrich with latest financial data and risk scores
    results = []
    for company in companies:
        # Get latest financial data
        financial_stmt = select(FinancialStatement).where(
            FinancialStatement.company_id == company.id
        ).order_by(desc(FinancialStatement.fiscal_year)).limit(1)
        
        financial_result = await db.execute(financial_stmt)
        latest_financial = financial_result.scalar_one_or_none()
        
        # Get latest risk score
        risk_stmt = select(CompanyRiskScore).where(
            CompanyRiskScore.company_id == company.id
        ).order_by(desc(CompanyRiskScore.calculation_date)).limit(1)
        
        risk_result = await db.execute(risk_stmt)
        latest_risk = risk_result.scalar_one_or_none()
        
        # Apply risk score filter
        if min_risk_score is not None or max_risk_score is not None:
            if not latest_risk:
                continue
            if min_risk_score and latest_risk.overall_risk_score < min_risk_score:
                continue
            if max_risk_score and latest_risk.overall_risk_score > max_risk_score:
                continue
        
        results.append(CompanySearchResult(
            company={
                "id": company.id,
                "name": company.name,
                "country_code": company.country_code,
                "sector": company.sector,
                "ticker": company.ticker,
                "is_listed": company.is_listed,
            },
            latest_revenue=latest_financial.revenue if latest_financial else None,
            latest_net_income=latest_financial.net_income if latest_financial else None,
            latest_ebitda=latest_financial.ebitda if latest_financial else None,
            risk_score=latest_risk.overall_risk_score if latest_risk else None,
            risk_category=latest_risk.risk_category if latest_risk else None,
        ))
    
    return CompanySearchResponse(
        results=results,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{company_id}", response_model=CompanyDetailResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get detailed company information
    """
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest financial statement
    financial_stmt = select(FinancialStatement).where(
        FinancialStatement.company_id == company_id
    ).order_by(desc(FinancialStatement.fiscal_year)).limit(1)
    financial_result = await db.execute(financial_stmt)
    latest_financial = financial_result.scalar_one_or_none()
    
    # Get latest cash flow
    cashflow_stmt = select(CashFlow).where(
        CashFlow.company_id == company_id
    ).order_by(desc(CashFlow.fiscal_year)).limit(1)
    cashflow_result = await db.execute(cashflow_stmt)
    latest_cashflow = cashflow_result.scalar_one_or_none()
    
    # Get latest risk score
    risk_stmt = select(CompanyRiskScore).where(
        CompanyRiskScore.company_id == company_id
    ).order_by(desc(CompanyRiskScore.calculation_date)).limit(1)
    risk_result = await db.execute(risk_stmt)
    latest_risk = risk_result.scalar_one_or_none()
    
    return CompanyDetailResponse(
        **company.__dict__,
        latest_financial=latest_financial,
        latest_cashflow=latest_cashflow,
        latest_risk_score=latest_risk,
    )


@router.get("/{company_id}/financials", response_model=CompanyFinancialsResponse)
async def get_company_financials(
    company_id: int,
    years: int = Query(5, ge=1, le=10, description="Number of years of historical data"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get multi-year financial statements and cash flows
    """
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get financial statements
    financial_stmt = select(FinancialStatement).where(
        FinancialStatement.company_id == company_id
    ).order_by(desc(FinancialStatement.fiscal_year)).limit(years)
    financial_result = await db.execute(financial_stmt)
    financials = financial_result.scalars().all()
    
    # Get cash flows
    cashflow_stmt = select(CashFlow).where(
        CashFlow.company_id == company_id
    ).order_by(desc(CashFlow.fiscal_year)).limit(years)
    cashflow_result = await db.execute(cashflow_stmt)
    cashflows = cashflow_result.scalars().all()
    
    return CompanyFinancialsResponse(
        company=company,
        financial_statements=financials,
        cashflows=cashflows,
    )


@router.get("/{company_id}/risk", response_model=CompanyRiskAnalysis)
async def get_company_risk_analysis(
    company_id: int,
    fiscal_year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get detailed risk analysis for a company
    """
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Determine fiscal year
    if not fiscal_year:
        # Get latest fiscal year
        stmt = select(FinancialStatement.fiscal_year).where(
            FinancialStatement.company_id == company_id
        ).order_by(desc(FinancialStatement.fiscal_year)).limit(1)
        result = await db.execute(stmt)
        fiscal_year = result.scalar_one_or_none()
        
        if not fiscal_year:
            raise HTTPException(status_code=404, detail="No financial data available")
    
    # Get or calculate risk score
    risk_stmt = select(CompanyRiskScore).where(
        CompanyRiskScore.company_id == company_id,
        CompanyRiskScore.fiscal_year == fiscal_year
    ).order_by(desc(CompanyRiskScore.calculation_date)).limit(1)
    risk_result = await db.execute(risk_stmt)
    risk_score = risk_result.scalar_one_or_none()
    
    if not risk_score:
        # Calculate risk score
        risk_data = await risk_scoring_service.calculate_company_risk(
            db, company_id, fiscal_year
        )
        
        if not risk_data:
            raise HTTPException(status_code=404, detail="Cannot calculate risk score - missing data")
        
        # Save risk score
        risk_score = CompanyRiskScore(**risk_data)
        db.add(risk_score)
        await db.commit()
        await db.refresh(risk_score)
    
    # Get financial statement
    financial_stmt = select(FinancialStatement).where(
        FinancialStatement.company_id == company_id,
        FinancialStatement.fiscal_year == fiscal_year
    )
    financial_result = await db.execute(financial_stmt)
    financial = financial_result.scalar_one_or_none()
    
    # Get cash flow
    cashflow_stmt = select(CashFlow).where(
        CashFlow.company_id == company_id,
        CashFlow.fiscal_year == fiscal_year
    )
    cashflow_result = await db.execute(cashflow_stmt)
    cashflow = cashflow_result.scalar_one_or_none()
    
    return CompanyRiskAnalysis(
        company={
            "id": company.id,
            "name": company.name,
            "country_code": company.country_code,
            "sector": company.sector,
            "ticker": company.ticker,
            "is_listed": company.is_listed,
        },
        risk_score=risk_score,
        financial_statement=financial,
        cashflow=cashflow,
    )


@router.post("/compare", response_model=CompanyComparisonResponse)
async def compare_companies(
    request: CompanyComparisonRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Compare multiple companies side-by-side
    """
    if len(request.company_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 companies required")
    
    if len(request.company_ids) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 companies allowed")
    
    # Determine fiscal year
    fiscal_year = request.fiscal_year
    if not fiscal_year:
        # Use latest common year
        fiscal_year = 2024  # Default to current year - 1
    
    companies_data = []
    for company_id in request.company_ids:
        try:
            company_detail = await get_company(company_id, db, current_user)
            companies_data.append(company_detail)
        except HTTPException:
            continue
    
    if len(companies_data) < 2:
        raise HTTPException(status_code=404, detail="Not enough valid companies found")
    
    return CompanyComparisonResponse(
        companies=companies_data,
        fiscal_year=fiscal_year,
    )


@router.post("/ingest", response_model=CompanyIngestResponse)
async def ingest_company_data(
    request: CompanyIngestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Fetch and store company data from Yahoo Finance
    Admin/authenticated users only
    """
    try:
        # Fetch company info
        company_info = await yahoo_client.get_company_info(request.ticker)
        if not company_info:
            return CompanyIngestResponse(
                success=False,
                message=f"Could not fetch data for ticker {request.ticker}",
            )
        
        # Normalize company info
        normalized_info = await normalization_service.normalize_company_info(company_info)
        
        # Check if company exists
        stmt = select(Company).where(Company.ticker == request.ticker)
        result = await db.execute(stmt)
        company = result.scalar_one_or_none()
        
        if not company:
            # Create new company
            company = Company(
                **normalized_info,
                ticker=request.ticker,
                data_source='yahoo_finance'
            )
            db.add(company)
            await db.commit()
            await db.refresh(company)
        
        # Fetch financial statements
        financial_data = await yahoo_client.get_financial_statements(request.ticker, request.years)
        cashflow_data = await yahoo_client.get_cashflow_statements(request.ticker, request.years)
        
        financial_years = []
        validation_errors = []
        
        if financial_data:
            for financial in financial_data:
                # Normalize data
                normalized_financial = await normalization_service.normalize_financial_statement(
                    financial, company_info.get('currency', 'USD')
                )
                
                if normalization_service.has_validation_errors():
                    validation_errors.extend(normalization_service.get_validation_errors())
                
                # Check if already exists
                stmt = select(FinancialStatement).where(
                    FinancialStatement.company_id == company.id,
                    FinancialStatement.fiscal_year == normalized_financial['fiscal_year']
                )
                result = await db.execute(stmt)
                existing = result.scalar_one_or_none()
                
                if not existing:
                    financial_stmt = FinancialStatement(
                        company_id=company.id,
                        data_source='yahoo_finance',
                        **normalized_financial
                    )
                    db.add(financial_stmt)
                    financial_years.append(normalized_financial['fiscal_year'])
        
        if cashflow_data:
            for cashflow in cashflow_data:
                normalized_cashflow = await normalization_service.normalize_cashflow_statement(
                    cashflow, company_info.get('currency', 'USD')
                )
                
                # Check if already exists
                stmt = select(CashFlow).where(
                    CashFlow.company_id == company.id,
                    CashFlow.fiscal_year == normalized_cashflow['fiscal_year']
                )
                result = await db.execute(stmt)
                existing = result.scalar_one_or_none()
                
                if not existing:
                    cashflow_stmt = CashFlow(
                        company_id=company.id,
                        data_source='yahoo_finance',
                        **normalized_cashflow
                    )
                    db.add(cashflow_stmt)
        
        await db.commit()
        
        return CompanyIngestResponse(
            success=True,
            company_id=company.id,
            message=f"Successfully ingested data for {company.name}",
            financial_years=financial_years,
            validation_errors=validation_errors,
        )
        
    except Exception as e:
        await db.rollback()
        return CompanyIngestResponse(
            success=False,
            message=f"Error ingesting data: {str(e)}",
        )


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update company information
    """
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Update fields
    update_data = company_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    await db.commit()
    await db.refresh(company)
    
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a company and all its related data
    """
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    await db.delete(company)
    await db.commit()
    
    return None
