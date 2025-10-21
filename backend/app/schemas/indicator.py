"""
Pydantic schemas for indicator data requests and responses
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class IndicatorValueResponse(BaseModel):
    """Schema for indicator value response"""
    id: int
    country_code: str
    sector: Optional[str] = None
    indicator_code: str
    indicator_name: Optional[str] = None
    date: date
    period_type: str
    value: float
    unit: Optional[str] = None
    source: str
    source_dataset: Optional[str] = None
    is_estimated: bool
    is_provisional: bool
    fetched_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class IndicatorQuery(BaseModel):
    """Schema for querying indicator data"""
    country_codes: Optional[List[str]] = Field(
        None,
        description="Filter by country codes (e.g., ['NL', 'BE'])"
    )
    sectors: Optional[List[str]] = Field(
        None,
        description="Filter by sectors"
    )
    indicator_codes: Optional[List[str]] = Field(
        None,
        description="Filter by indicator codes"
    )
    sources: Optional[List[str]] = Field(
        None,
        description="Filter by data sources"
    )
    date_from: Optional[date] = Field(
        None,
        description="Start date (inclusive)"
    )
    date_to: Optional[date] = Field(
        None,
        description="End date (inclusive)"
    )
    limit: int = Field(
        default=1000,
        ge=1,
        le=10000,
        description="Maximum number of records to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of records to skip"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "country_codes": ["NL", "BE"],
                "indicator_codes": ["GDP_GROWTH", "UNEMPLOYMENT"],
                "date_from": "2023-01-01",
                "date_to": "2024-12-31",
                "limit": 100
            }
        }
    )


class IndicatorListResponse(BaseModel):
    """Schema for paginated indicator list"""
    total: int = Field(..., description="Total number of records")
    items: List[IndicatorValueResponse] = Field(..., description="List of indicators")
    limit: int
    offset: int
