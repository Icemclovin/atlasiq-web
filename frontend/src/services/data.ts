import apiClient from './api';
import type {
  Country,
  Indicator,
  DataSource,
  DataPoint,
  TimeSeriesData,
  DataQueryParams,
  DashboardSummary,
  CountryDetail,
  RiskScore,
} from '@/types';

export const dataService = {
  /**
   * Get list of supported countries
   */
  async getCountries(): Promise<Country[]> {
    const response = await apiClient.getClient().get<Country[]>('/api/v1/data/countries');
    return response.data;
  },

  /**
   * Get list of available indicators
   */
  async getIndicators(): Promise<Indicator[]> {
    const response = await apiClient.getClient().get<Indicator[]>('/api/v1/data/indicators');
    return response.data;
  },

  /**
   * Get list of data sources
   */
  async getDataSources(): Promise<DataSource[]> {
    const response = await apiClient.getClient().get<DataSource[]>('/api/v1/data-sources');
    return response.data;
  },

  /**
   * Query time-series data
   */
  async queryData(params: DataQueryParams): Promise<DataPoint[]> {
    const response = await apiClient.getClient().get<DataPoint[]>('/api/v1/data', { params });
    return response.data;
  },

  /**
   * Get time series data for specific indicator and country
   */
  async getTimeSeries(indicatorCode: string, countryCode: string): Promise<TimeSeriesData> {
    const response = await apiClient.getClient().get<TimeSeriesData>(
      `/api/v1/data/timeseries/${indicatorCode}/${countryCode}`
    );
    return response.data;
  },

  /**
   * Get dashboard summary with all countries
   */
  async getDashboardSummary(): Promise<DashboardSummary> {
    const response = await apiClient.getClient().get<DashboardSummary>('/api/v1/data/dashboard');
    return response.data;
  },

  /**
   * Get detailed country data
   */
  async getCountryDetail(countryCode: string): Promise<CountryDetail> {
    const response = await apiClient.getClient().get<CountryDetail>(`/api/v1/data/countries/${countryCode}`);
    return response.data;
  },

  /**
   * Get risk scores
   */
  async getRiskScores(countryCode?: string): Promise<RiskScore[]> {
    const params = countryCode ? { country_code: countryCode } : {};
    const response = await apiClient.getClient().get<RiskScore[]>('/api/v1/data/risk-scores', { params });
    return response.data;
  },

  /**
   * Trigger manual data fetch (admin only)
   */
  async triggerDataFetch(sourceCode: string): Promise<{ message: string }> {
    const response = await apiClient.getClient().post<{ message: string }>('/api/v1/fetch', {
      source_code: sourceCode,
    });
    return response.data;
  },

  /**
   * Export data to CSV
   */
  async exportToCSV(params: DataQueryParams): Promise<Blob> {
    const response = await apiClient.getClient().post('/api/v1/data/export/csv', params, {
      responseType: 'blob',
    });
    return response.data;
  },

  /**
   * Export data to Excel
   */
  async exportToExcel(params: DataQueryParams): Promise<Blob> {
    const response = await apiClient.getClient().post('/api/v1/data/export/excel', params, {
      responseType: 'blob',
    });
    return response.data;
  },
};
