/**
 * Company API service
 */
import apiClient from './api';
import type {
  CompanySearchParams,
  CompanySearchResponse,
  CompanyDetail,
  CompanyFinancials,
  CompanyRiskAnalysis,
  CompanyIngestRequest,
  CompanyIngestResponse,
} from '@/types/company';

export const companyService = {
  /**
   * Search companies with filters
   */
  async searchCompanies(params: CompanySearchParams): Promise<CompanySearchResponse> {
    const queryParams = new URLSearchParams();
    
    if (params.query) queryParams.append('query', params.query);
    if (params.country_code) queryParams.append('country_code', params.country_code);
    if (params.sector) queryParams.append('sector', params.sector);
    if (params.is_listed !== undefined) queryParams.append('is_listed', String(params.is_listed));
    if (params.min_risk_score !== undefined) queryParams.append('min_risk_score', String(params.min_risk_score));
    if (params.max_risk_score !== undefined) queryParams.append('max_risk_score', String(params.max_risk_score));
    if (params.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params.sort_order) queryParams.append('sort_order', params.sort_order);
    if (params.skip !== undefined) queryParams.append('skip', String(params.skip));
    if (params.limit !== undefined) queryParams.append('limit', String(params.limit));
    
    const response = await apiClient.getClient().get<CompanySearchResponse>(
      `/api/v1/companies/search?${queryParams.toString()}`
    );
    return response.data;
  },

  /**
   * Get company details by ID
   */
  async getCompany(companyId: number): Promise<CompanyDetail> {
    const response = await apiClient.getClient().get<CompanyDetail>(
      `/api/v1/companies/${companyId}`
    );
    return response.data;
  },

  /**
   * Get multi-year financial data
   */
  async getCompanyFinancials(companyId: number, years: number = 5): Promise<CompanyFinancials> {
    const response = await apiClient.getClient().get<CompanyFinancials>(
      `/api/v1/companies/${companyId}/financials?years=${years}`
    );
    return response.data;
  },

  /**
   * Get company risk analysis
   */
  async getCompanyRisk(companyId: number, fiscalYear?: number): Promise<CompanyRiskAnalysis> {
    const url = fiscalYear
      ? `/api/v1/companies/${companyId}/risk?fiscal_year=${fiscalYear}`
      : `/api/v1/companies/${companyId}/risk`;
    
    const response = await apiClient.getClient().get<CompanyRiskAnalysis>(url);
    return response.data;
  },

  /**
   * Compare multiple companies
   */
  async compareCompanies(companyIds: number[], fiscalYear?: number): Promise<any> {
    const response = await apiClient.getClient().post('/api/v1/companies/compare', {
      company_ids: companyIds,
      fiscal_year: fiscalYear,
    });
    return response.data;
  },

  /**
   * Ingest company data from Yahoo Finance
   */
  async ingestCompany(request: CompanyIngestRequest): Promise<CompanyIngestResponse> {
    const response = await apiClient.getClient().post<CompanyIngestResponse>(
      '/api/v1/companies/ingest',
      request
    );
    return response.data;
  },

  /**
   * Update company information
   */
  async updateCompany(companyId: number, data: Partial<CompanyDetail>): Promise<CompanyDetail> {
    const response = await apiClient.getClient().put<CompanyDetail>(
      `/api/v1/companies/${companyId}`,
      data
    );
    return response.data;
  },

  /**
   * Delete company
   */
  async deleteCompany(companyId: number): Promise<void> {
    await apiClient.getClient().delete(`/api/v1/companies/${companyId}`);
  },
};
