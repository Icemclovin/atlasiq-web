import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Loading } from '@/components/Loading';
import { companyService } from '@/services/company';
import { Search, Building2, TrendingUp, TrendingDown, AlertTriangle, Plus, LogOut } from 'lucide-react';
import type { CompanySearchResult, CompanySearchParams } from '@/types/company';

export const Companies = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<CompanySearchResult[]>([]);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState('');
  
  // Search params
  const [searchQuery, setSearchQuery] = useState('');
  const [countryFilter, setCountryFilter] = useState('');
  const [sectorFilter, setSectorFilter] = useState('');
  const [page, setPage] = useState(0);
  const limit = 20;

  useEffect(() => {
    searchCompanies();
  }, [page, countryFilter, sectorFilter]);

  const searchCompanies = async () => {
    try {
      setLoading(true);
      setError('');

      const params: CompanySearchParams = {
        query: searchQuery || undefined,
        country_code: countryFilter || undefined,
        sector: sectorFilter || undefined,
        skip: page * limit,
        limit: limit,
        sort_by: 'name',
        sort_order: 'asc',
      };

      const response = await companyService.searchCompanies(params);
      setResults(response.results);
      setTotal(response.total);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to search companies');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(0);
    searchCompanies();
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getRiskColor = (score?: number) => {
    if (!score) return 'text-gray-500 bg-gray-100';
    if (score < 30) return 'text-green-600 bg-green-100';
    if (score < 50) return 'text-yellow-600 bg-yellow-100';
    if (score < 70) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const formatCurrency = (value?: number) => {
    if (!value) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'EUR',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Companies</h1>
                <p className="text-sm text-gray-600">
                  Search and analyze companies in Benelux + Germany
                </p>
              </div>
              <nav className="flex gap-4">
                <Button 
                  onClick={() => navigate('/dashboard')} 
                  variant="ghost"
                  className="text-sm"
                >
                  Dashboard
                </Button>
                <Button 
                  onClick={() => navigate('/companies')} 
                  variant="ghost"
                  className="text-sm"
                >
                  Companies
                </Button>
              </nav>
            </div>
            <div className="flex gap-2">
              <Button onClick={() => navigate('/companies/ingest')}>
                <Plus className="h-5 w-5 mr-2" />
                Add Company
              </Button>
              <Button onClick={handleLogout} variant="ghost">
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <Card className="mb-6 p-6">
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2">
                <Input
                  label="Search"
                  placeholder="Company name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Country
                </label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  value={countryFilter}
                  onChange={(e) => setCountryFilter(e.target.value)}
                >
                  <option value="">All Countries</option>
                  <option value="NL">Netherlands</option>
                  <option value="BE">Belgium</option>
                  <option value="LU">Luxembourg</option>
                  <option value="DE">Germany</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Sector
                </label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  value={sectorFilter}
                  onChange={(e) => setSectorFilter(e.target.value)}
                >
                  <option value="">All Sectors</option>
                  <option value="Technology">Technology</option>
                  <option value="Financial Services">Financial Services</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Consumer">Consumer</option>
                  <option value="Industrial">Industrial</option>
                  <option value="Energy">Energy</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end">
              <Button type="submit" loading={loading}>
                <Search className="h-5 w-5 mr-2" />
                Search
              </Button>
            </div>
          </form>
        </Card>

        {/* Results */}
        {error && (
          <Card className="p-6 mb-6 border-red-200 bg-red-50">
            <div className="flex items-center text-red-800">
              <AlertTriangle className="h-5 w-5 mr-2" />
              {error}
            </div>
          </Card>
        )}

        {loading ? (
          <Loading message="Searching companies..." />
        ) : (
          <>
            <div className="mb-4 text-sm text-gray-600">
              Found {total} {total === 1 ? 'company' : 'companies'}
            </div>

            <div className="grid grid-cols-1 gap-4">
              {results.map((result) => (
                <div
                  key={result.company.id}
                  onClick={() => navigate(`/companies/${result.company.id}`)}
                  className="cursor-pointer"
                >
                  <Card className="p-6 hover:shadow-lg transition-shadow">
                    <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <Building2 className="h-6 w-6 text-primary-600" />
                        <div>
                          <h3 className="text-lg font-bold text-gray-900">
                            {result.company.name}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {result.company.country_code} • {result.company.sector || 'N/A'}
                            {result.company.ticker && ` • ${result.company.ticker}`}
                          </p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Revenue</p>
                          <p className="text-lg font-semibold text-gray-900">
                            {formatCurrency(result.latest_revenue)}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs text-gray-600 mb-1">Net Income</p>
                          <div className="flex items-center">
                            <p className="text-lg font-semibold text-gray-900">
                              {formatCurrency(result.latest_net_income)}
                            </p>
                            {result.latest_net_income && result.latest_net_income > 0 ? (
                              <TrendingUp className="h-4 w-4 text-green-600 ml-2" />
                            ) : result.latest_net_income && result.latest_net_income < 0 ? (
                              <TrendingDown className="h-4 w-4 text-red-600 ml-2" />
                            ) : null}
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-600 mb-1">EBITDA</p>
                          <p className="text-lg font-semibold text-gray-900">
                            {formatCurrency(result.latest_ebitda)}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs text-gray-600 mb-1">Risk Score</p>
                          <div className={`inline-flex px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(result.risk_score)}`}>
                            {result.risk_score ? result.risk_score.toFixed(0) : 'N/A'}
                          </div>
                        </div>
                      </div>
                      </div>
                    </div>
                  </Card>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {total > limit && (
              <div className="mt-6 flex justify-center gap-2">
                <Button
                  onClick={() => setPage(Math.max(0, page - 1))}
                  disabled={page === 0}
                  variant="secondary"
                >
                  Previous
                </Button>
                <span className="px-4 py-2 text-gray-700">
                  Page {page + 1} of {Math.ceil(total / limit)}
                </span>
                <Button
                  onClick={() => setPage(page + 1)}
                  disabled={(page + 1) * limit >= total}
                  variant="secondary"
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
};
