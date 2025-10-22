/**
 * Macro Economic Indicators API Service
 * Fetches GDP, inflation, unemployment, and interest rate data
 */

import apiClient from './api';

export interface MacroDataPoint {
  country: string;
  date: string;
  year: number;
  value: number;
  indicator: string;
  unit: string;
}

export interface InterestRateData {
  rate_type: string;
  rate_name: string;
  date: string;
  year: number;
  value: number;
  currency: string;
  unit: string;
}

export interface MacroResponse {
  data: MacroDataPoint[];
  meta?: {
    countries: string[];
    start_year: number;
    end_year: number;
    total_records: number;
    data_source: string;
    data_type: string;
  };
}

export interface InterestRateResponse {
  data: InterestRateData[];
}

export const macroService = {
  /**
   * Get GDP growth rates
   */
  async getGDPGrowth(
    countries: string[] = ['NLD', 'BEL', 'LUX', 'DEU'],
    startYear: number = 2015,
    endYear: number = 2023
  ): Promise<MacroResponse> {
    const params = new URLSearchParams();
    countries.forEach(c => params.append('countries', c));
    params.append('start_year', startYear.toString());
    params.append('end_year', endYear.toString());

    const response = await apiClient.getClient().get<MacroResponse>(
      `/api/v1/macro/gdp?${params.toString()}`
    );
    return response.data;
  },

  /**
   * Get inflation rates (HICP)
   */
  async getInflation(
    countries: string[] = ['NLD', 'BEL', 'LUX', 'DEU'],
    startYear: number = 2015,
    endYear: number = 2023
  ): Promise<MacroResponse> {
    const params = new URLSearchParams();
    countries.forEach(c => params.append('countries', c));
    params.append('start_year', startYear.toString());
    params.append('end_year', endYear.toString());

    const response = await apiClient.getClient().get<MacroResponse>(
      `/api/v1/macro/inflation?${params.toString()}`
    );
    return response.data;
  },

  /**
   * Get unemployment rates
   */
  async getUnemployment(
    countries: string[] = ['NLD', 'BEL', 'LUX', 'DEU'],
    startYear: number = 2015,
    endYear: number = 2023
  ): Promise<MacroResponse> {
    const params = new URLSearchParams();
    countries.forEach(c => params.append('countries', c));
    params.append('start_year', startYear.toString());
    params.append('end_year', endYear.toString());

    const response = await apiClient.getClient().get<MacroResponse>(
      `/api/v1/macro/unemployment?${params.toString()}`
    );
    return response.data;
  },

  /**
   * Get ECB interest rates
   */
  async getInterestRates(
    startYear: number = 2015,
    endYear: number = 2023
  ): Promise<InterestRateResponse> {
    const params = new URLSearchParams();
    params.append('start_year', startYear.toString());
    params.append('end_year', endYear.toString());

    const response = await apiClient.getClient().get<InterestRateResponse>(
      `/api/v1/macro/interest-rates?${params.toString()}`
    );
    return response.data;
  },

  /**
   * Export data to CSV
   */
  exportToCSV(data: MacroDataPoint[] | InterestRateData[], filename: string) {
    if (data.length === 0) return;

    // Get headers from first object
    const headers = Object.keys(data[0]);
    
    // Build CSV content
    const csvContent = [
      headers.join(','),
      ...data.map(row => 
        headers.map(header => {
          const value = (row as any)[header];
          // Escape commas and quotes in values
          if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
            return `"${value.replace(/"/g, '""')}"`;
          }
          return value;
        }).join(',')
      )
    ].join('\n');

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `${filename}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

// Country code mapping for display
export const COUNTRY_NAMES: Record<string, string> = {
  'NLD': 'Netherlands',
  'BEL': 'Belgium',
  'LUX': 'Luxembourg',
  'DEU': 'Germany'
};

// Country colors for consistent chart styling
export const COUNTRY_COLORS: Record<string, string> = {
  'NLD': '#FF6B35', // Orange
  'BEL': '#004E89', // Blue
  'LUX': '#1B998B', // Teal
  'DEU': '#A23B72'  // Purple
};
