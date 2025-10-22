/**
 * MacroIndicators Component
 * Main component for displaying macroeconomic indicators
 * Includes tabs for different indicators and controls for filtering
 */

import { useState, useEffect } from 'react';
import MacroChart, { ChartType } from './MacroChart';
import { macroService, COUNTRY_NAMES, MacroDataPoint, InterestRateData } from '../services/macroService';

type IndicatorTab = 'gdp' | 'inflation' | 'unemployment' | 'interest-rates';

interface ChartData {
  year: number;
  [key: string]: number;
}

const MacroIndicators = () => {
  const [activeTab, setActiveTab] = useState<IndicatorTab>('gdp');
  const [selectedCountries, setSelectedCountries] = useState<string[]>(['NLD', 'BEL', 'LUX', 'DEU']);
  const [startYear, setStartYear] = useState<number>(2015);
  const [endYear, setEndYear] = useState<number>(2023);
  const [chartType, setChartType] = useState<ChartType>('line');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [rawData, setRawData] = useState<MacroDataPoint[] | InterestRateData[]>([]);

  // Fetch data based on active tab and filters
  useEffect(() => {
    fetchData();
  }, [activeTab, selectedCountries, startYear, endYear]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      let data: MacroDataPoint[] | InterestRateData[] = [];

      switch (activeTab) {
        case 'gdp':
          const gdpResponse = await macroService.getGDPGrowth(selectedCountries, startYear, endYear);
          data = gdpResponse.data;
          break;
        case 'inflation':
          const inflationResponse = await macroService.getInflation(selectedCountries, startYear, endYear);
          data = inflationResponse.data;
          break;
        case 'unemployment':
          const unemploymentResponse = await macroService.getUnemployment(selectedCountries, startYear, endYear);
          data = unemploymentResponse.data;
          break;
        case 'interest-rates':
          const ratesResponse = await macroService.getInterestRates(startYear, endYear);
          data = ratesResponse.data;
          break;
      }

      // Transform data for recharts
      const transformed = transformDataForChart(data, activeTab);
      setChartData(transformed);
      setRawData(data);
    } catch (err) {
      console.error('Error fetching macro data:', err);
      setError('Failed to load data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Transform API data to chart format
  const transformDataForChart = (data: MacroDataPoint[] | InterestRateData[], tab: IndicatorTab): ChartData[] => {
    if (tab === 'interest-rates') {
      // Group interest rates by year and rate type
      const rateData = data as InterestRateData[];
      const yearMap: { [year: number]: ChartData } = {};

      rateData.forEach((item) => {
        if (!yearMap[item.year]) {
          yearMap[item.year] = { year: item.year };
        }
        yearMap[item.year][item.rate_name] = item.value;
      });

      return Object.values(yearMap).sort((a, b) => a.year - b.year);
    } else {
      // Group by year and country
      const macroData = data as MacroDataPoint[];
      const yearMap: { [year: number]: ChartData } = {};

      macroData.forEach((item) => {
        if (!yearMap[item.year]) {
          yearMap[item.year] = { year: item.year };
        }
        yearMap[item.year][item.country] = item.value;
      });

      return Object.values(yearMap).sort((a, b) => a.year - b.year);
    }
  };

  // Handle country selection
  const toggleCountry = (country: string) => {
    if (selectedCountries.includes(country)) {
      if (selectedCountries.length > 1) {
        setSelectedCountries(selectedCountries.filter((c) => c !== country));
      }
    } else {
      setSelectedCountries([...selectedCountries, country]);
    }
  };

  // Export data to CSV
  const handleExport = () => {
    const filename = `${activeTab}_${startYear}_${endYear}.csv`;
    macroService.exportToCSV(rawData, filename);
  };

  // Get chart title and Y-axis label based on active tab
  const getChartConfig = () => {
    switch (activeTab) {
      case 'gdp':
        return { title: 'GDP Growth Rate', yAxisLabel: 'Growth Rate (%)' };
      case 'inflation':
        return { title: 'Inflation Rate (HICP)', yAxisLabel: 'Inflation Rate (%)' };
      case 'unemployment':
        return { title: 'Unemployment Rate', yAxisLabel: 'Unemployment Rate (%)' };
      case 'interest-rates':
        return { title: 'ECB Interest Rates', yAxisLabel: 'Interest Rate (%)' };
    }
  };

  const chartConfig = getChartConfig();
  const years = Array.from({ length: 2024 - 2015 }, (_, i) => 2015 + i);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Economic Indicators</h2>
        <p className="text-sm text-gray-600 mt-1">
          Historical data (2015-2023) • Benelux + Germany
          <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Historical Data</span>
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-4">
          {(['gdp', 'inflation', 'unemployment', 'interest-rates'] as IndicatorTab[]).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              {tab === 'gdp' && 'GDP Growth'}
              {tab === 'inflation' && 'Inflation'}
              {tab === 'unemployment' && 'Unemployment'}
              {tab === 'interest-rates' && 'Interest Rates'}
            </button>
          ))}
        </nav>
      </div>

      {/* Controls */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Country Selection */}
        {activeTab !== 'interest-rates' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Countries</label>
            <div className="space-y-2">
              {Object.entries(COUNTRY_NAMES).map(([code, name]) => (
                <label key={code} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedCountries.includes(code)}
                    onChange={() => toggleCountry(code)}
                    className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{name}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Date Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Start Year</label>
          <select
            value={startYear}
            onChange={(e) => setStartYear(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">End Year</label>
          <select
            value={endYear}
            onChange={(e) => setEndYear(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Chart Type Selector */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex space-x-2">
          <label className="text-sm font-medium text-gray-700 mr-2">Chart Type:</label>
          {(['line', 'bar', 'area'] as ChartType[]).map((type) => (
            <button
              key={type}
              onClick={() => setChartType(type)}
              className={`px-3 py-1 text-sm rounded transition-colors ${
                chartType === type
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>

        {/* Export Button */}
        <button
          onClick={handleExport}
          disabled={loading || chartData.length === 0}
          className="px-4 py-2 bg-green-500 text-white text-sm rounded hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          Export CSV
        </button>
      </div>

      {/* Chart */}
      {loading && (
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
          <button onClick={fetchData} className="mt-2 text-sm text-red-600 hover:text-red-800 underline">
            Try again
          </button>
        </div>
      )}

      {!loading && !error && chartData.length > 0 && (
        <MacroChart
          data={chartData}
          chartType={chartType}
          title={chartConfig.title}
          yAxisLabel={chartConfig.yAxisLabel}
          countries={activeTab === 'interest-rates' ? [] : selectedCountries}
          height={500}
        />
      )}

      {!loading && !error && chartData.length === 0 && (
        <div className="flex items-center justify-center h-96 text-gray-500">
          <p>No data available for the selected criteria.</p>
        </div>
      )}
    </div>
  );
};

export default MacroIndicators;
