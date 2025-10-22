import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { CompanyDetail, CompanyFinancials, CompanyRiskAnalysis } from '@/types/company';
import { companyService } from '@/services/company';

type TabType = 'overview' | 'financials' | 'risk';

export const CompanyDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [company, setCompany] = useState<CompanyDetail | null>(null);
  const [financials, setFinancials] = useState<CompanyFinancials | null>(null);
  const [risk, setRisk] = useState<CompanyRiskAnalysis | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;
      
      setLoading(true);
      setError(null);

      try {
        const [companyData, financialsData, riskData] = await Promise.all([
          companyService.getCompany(parseInt(id)),
          companyService.getCompanyFinancials(parseInt(id), 5),
          companyService.getCompanyRisk(parseInt(id))
        ]);

        setCompany(companyData);
        setFinancials(financialsData);
        setRisk(riskData);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load company data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const formatCurrency = (value: number | null | undefined): string => {
    if (value === null || value === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'EUR',
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  };

  const formatPercent = (value: number | null | undefined): string => {
    if (value === null || value === undefined) return 'N/A';
    return `${value.toFixed(2)}%`;
  };

  const getRiskColor = (score: number | null | undefined): string => {
    if (score === null || score === undefined) return 'bg-gray-100 text-gray-800';
    if (score < 30) return 'bg-green-100 text-green-800';
    if (score < 50) return 'bg-yellow-100 text-yellow-800';
    if (score < 70) return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  const getRiskLabel = (score: number | null | undefined): string => {
    if (score === null || score === undefined) return 'N/A';
    if (score < 30) return 'Low Risk';
    if (score < 50) return 'Medium Risk';
    if (score < 70) return 'High Risk';
    return 'Critical Risk';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading company data...</p>
        </div>
      </div>
    );
  }

  if (error || !company) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-700 mb-4">{error || 'Company not found'}</p>
          <Button onClick={() => navigate('/companies')}>
            Back to Companies
          </Button>
        </Card>
      </div>
    );
  }

  // Prepare chart data
  const revenueChartData = financials?.financial_statements.map((f) => ({
    year: f.fiscal_year,
    revenue: f.revenue || 0,
    ebitda: f.ebitda || 0,
    netIncome: f.net_income || 0
  })).sort((a, b) => a.year - b.year) || [];

  const cashFlowChartData = financials?.cashflows.map((cf) => ({
    year: cf.fiscal_year,
    operating: cf.operating_cashflow || 0,
    investing: cf.investing_cashflow || 0,
    financing: cf.financing_cashflow || 0,
    free: cf.free_cashflow || 0
  })).sort((a, b) => a.year - b.year) || [];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <Button
                variant="ghost"
                onClick={() => navigate('/companies')}
                className="mb-2"
              >
                ← Back to Companies
              </Button>
              <h1 className="text-3xl font-bold text-gray-900">{company.name}</h1>
              <div className="mt-2 flex items-center gap-4 text-sm text-gray-600">
                <span>{company.country_code}</span>
                {company.sector && <span>• {company.sector}</span>}
                {company.ticker && <span>• {company.ticker}</span>}
              </div>
            </div>
            {company.latest_risk_score && company.latest_risk_score.overall_risk_score !== undefined && (
              <div className="text-right">
                <div className={`inline-block px-4 py-2 rounded-lg ${getRiskColor(company.latest_risk_score.overall_risk_score)}`}>
                  <div className="text-2xl font-bold">
                    {company.latest_risk_score.overall_risk_score.toFixed(1)}
                  </div>
                  <div className="text-sm">
                    {getRiskLabel(company.latest_risk_score.overall_risk_score)}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {(['overview', 'financials', 'risk'] as TabType[]).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card className="p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Revenue</h3>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(company.latest_financial?.revenue)}
                </p>
                {company.latest_financial?.fiscal_year && (
                  <p className="text-xs text-gray-500 mt-1">FY {company.latest_financial.fiscal_year}</p>
                )}
              </Card>

              <Card className="p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">EBITDA</h3>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(company.latest_financial?.ebitda)}
                </p>
              </Card>

              <Card className="p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Net Income</h3>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(company.latest_financial?.net_income)}
                </p>
              </Card>

              <Card className="p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Total Assets</h3>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(company.latest_financial?.total_assets)}
                </p>
              </Card>
            </div>

            {/* Company Info */}
            <Card className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Company Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {company.nace_code && (
                  <div>
                    <span className="text-sm font-medium text-gray-500">NACE Code:</span>
                    <span className="ml-2 text-sm text-gray-900">{company.nace_code}</span>
                  </div>
                )}
                {company.ticker && (
                  <div>
                    <span className="text-sm font-medium text-gray-500">Ticker:</span>
                    <span className="ml-2 text-sm text-gray-900">{company.ticker}</span>
                  </div>
                )}
                {company.website && (
                  <div>
                    <span className="text-sm font-medium text-gray-500">Website:</span>
                    <span className="ml-2 text-sm text-gray-900">{company.website}</span>
                  </div>
                )}
                {company.lei_code && (
                  <div>
                    <span className="text-sm font-medium text-gray-500">LEI Code:</span>
                    <span className="ml-2 text-sm text-gray-900">{company.lei_code}</span>
                  </div>
                )}
              </div>
            </Card>

            {/* Revenue Trend */}
            {revenueChartData.length > 0 && (
              <Card className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Financial Performance</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={revenueChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip
                      formatter={(value: number) => formatCurrency(value)}
                    />
                    <Legend />
                    <Line type="monotone" dataKey="revenue" stroke="#3b82f6" name="Revenue" strokeWidth={2} />
                    <Line type="monotone" dataKey="ebitda" stroke="#10b981" name="EBITDA" strokeWidth={2} />
                    <Line type="monotone" dataKey="netIncome" stroke="#8b5cf6" name="Net Income" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </Card>
            )}
          </div>
        )}

        {activeTab === 'financials' && financials && (
          <div className="space-y-6">
            {/* Financial Statements Table */}
            <Card className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Financial Statements</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fiscal Year</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Revenue</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">EBITDA</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">EBIT</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Net Income</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Total Assets</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {financials.financial_statements.sort((a, b) => b.fiscal_year - a.fiscal_year).map((f) => (
                      <tr key={f.fiscal_year}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{f.fiscal_year}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">{formatCurrency(f.revenue)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">{formatCurrency(f.ebitda)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">{formatCurrency(f.ebit)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">{formatCurrency(f.net_income)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">{formatCurrency(f.total_assets)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>

            {/* Cash Flow Chart */}
            {cashFlowChartData.length > 0 && (
              <Card className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Cash Flow Trends</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={cashFlowChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip formatter={(value: number) => formatCurrency(value)} />
                    <Legend />
                    <Line type="monotone" dataKey="operating" stroke="#3b82f6" name="Operating CF" strokeWidth={2} />
                    <Line type="monotone" dataKey="investing" stroke="#ef4444" name="Investing CF" strokeWidth={2} />
                    <Line type="monotone" dataKey="financing" stroke="#f59e0b" name="Financing CF" strokeWidth={2} />
                    <Line type="monotone" dataKey="free" stroke="#10b981" name="Free CF" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </Card>
            )}
          </div>
        )}

        {activeTab === 'risk' && risk && (
          <div className="space-y-6">
            {/* Risk Scores */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Macro Risk</h3>
                <p className="text-3xl font-bold text-gray-900">{(risk.risk_score.macro_risk_score || 0).toFixed(1)}</p>
                <p className="text-xs text-gray-500 mt-1">Weight: 30%</p>
              </Card>

              <Card className="p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Sector Risk</h3>
                <p className="text-3xl font-bold text-gray-900">{(risk.risk_score.sector_risk_score || 0).toFixed(1)}</p>
                <p className="text-xs text-gray-500 mt-1">Weight: 20%</p>
              </Card>

              <Card className="p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Financial Health Risk</h3>
                <p className="text-3xl font-bold text-gray-900">{(risk.risk_score.financial_health_score || 0).toFixed(1)}</p>
                <p className="text-xs text-gray-500 mt-1">Weight: 50%</p>
              </Card>
            </div>

            {/* Financial Ratios */}
            <Card className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Financial Ratios</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div>
                  <span className="text-sm font-medium text-gray-500">Debt / EBITDA</span>
                  <p className="mt-1 text-xl font-semibold text-gray-900">
                    {risk.risk_score.debt_to_ebitda?.toFixed(2) || 'N/A'}
                  </p>
                </div>

                <div>
                  <span className="text-sm font-medium text-gray-500">EBITDA Margin</span>
                  <p className="mt-1 text-xl font-semibold text-gray-900">
                    {formatPercent(risk.risk_score.ebitda_margin)}
                  </p>
                </div>

                <div>
                  <span className="text-sm font-medium text-gray-500">ROA</span>
                  <p className="mt-1 text-xl font-semibold text-gray-900">
                    {formatPercent(risk.risk_score.roa)}
                  </p>
                </div>

                <div>
                  <span className="text-sm font-medium text-gray-500">ROE</span>
                  <p className="mt-1 text-xl font-semibold text-gray-900">
                    {formatPercent(risk.risk_score.roe)}
                  </p>
                </div>

                <div>
                  <span className="text-sm font-medium text-gray-500">Current Ratio</span>
                  <p className="mt-1 text-xl font-semibold text-gray-900">
                    {risk.risk_score.current_ratio?.toFixed(2) || 'N/A'}
                  </p>
                </div>

                <div>
                  <span className="text-sm font-medium text-gray-500">Quick Ratio</span>
                  <p className="mt-1 text-xl font-semibold text-gray-900">
                    {risk.risk_score.quick_ratio?.toFixed(2) || 'N/A'}
                  </p>
                </div>

                <div>
                  <span className="text-sm font-medium text-gray-500">FCF Yield</span>
                  <p className="mt-1 text-xl font-semibold text-gray-900">
                    {formatPercent(risk.risk_score.free_cashflow_yield)}
                  </p>
                </div>
              </div>
            </Card>

            {/* Risk Assessment */}
            <Card className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Risk Assessment</h2>
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Overall Risk</h3>
                  <div className="flex items-center">
                    <div className="flex-1 bg-gray-200 rounded-full h-4">
                      <div
                        className={`h-4 rounded-full ${
                          (risk.risk_score.overall_risk_score || 0) < 30 ? 'bg-green-500' :
                          (risk.risk_score.overall_risk_score || 0) < 50 ? 'bg-yellow-500' :
                          (risk.risk_score.overall_risk_score || 0) < 70 ? 'bg-orange-500' :
                          'bg-red-500'
                        }`}
                        style={{ width: `${risk.risk_score.overall_risk_score || 0}%` }}
                      />
                    </div>
                    <span className="ml-3 text-sm font-medium text-gray-700">
                      {(risk.risk_score.overall_risk_score || 0).toFixed(1)}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-gray-600">
                  {getRiskLabel(risk.risk_score.overall_risk_score)}
                </p>
              </div>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
};
