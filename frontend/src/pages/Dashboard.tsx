import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { dataService } from '@/services/data';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { Loading } from '@/components/Loading';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Activity, Globe, AlertTriangle, LogOut } from 'lucide-react';
import type { DashboardSummary, CountrySummary } from '@/types';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const data = await dataService.getDashboardSummary();
      setSummary(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return <Loading message="Loading dashboard..." />;
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="max-w-md">
          <div className="text-center">
            <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-gray-900 mb-2">Error Loading Dashboard</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={loadDashboard}>Try Again</Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AtlasIQ Dashboard</h1>
              <p className="text-sm text-gray-600">
                Welcome back, {user?.full_name}
              </p>
            </div>
            <Button onClick={handleLogout} variant="ghost">
              <LogOut className="h-5 w-5 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Countries</p>
                <p className="text-3xl font-bold text-gray-900">{summary?.countries?.length || 0}</p>
              </div>
              <div className="bg-primary-100 p-3 rounded-full">
                <Globe className="h-6 w-6 text-primary-600" />
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Indicators</p>
                <p className="text-3xl font-bold text-gray-900">{summary?.total_indicators || 0}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <Activity className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Data Freshness</p>
                <p className="text-3xl font-bold text-gray-900">{summary?.data_freshness || 0}h</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Last Updated</p>
                <p className="text-sm font-semibold text-gray-900">
                  {summary?.last_updated ? new Date(summary.last_updated).toLocaleDateString() : 'N/A'}
                </p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <Activity className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </Card>
        </div>

        {/* Country Overview */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Country Overview</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {summary?.countries && summary.countries.length > 0 ? (
              summary.countries.map((country) => (
                <CountryCard key={country.country.code} country={country} />
              ))
            ) : (
              <Card className="col-span-2 p-8 text-center">
                <AlertTriangle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
                <p className="text-gray-600">No country data available yet.</p>
                <p className="text-sm text-gray-500 mt-2">
                  Data will be fetched automatically on the next scheduled update.
                </p>
              </Card>
            )}
          </div>
        </div>

        {/* Charts */}
        {summary?.countries && summary.countries.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">GDP Growth by Country</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={summary.countries}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="country.code" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="gdp_growth" fill="#3b82f6" name="GDP Growth %" />
                </BarChart>
              </ResponsiveContainer>
            </Card>

            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Scores by Country</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={summary.countries}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="country.code" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="risk_score" fill="#ef4444" name="Risk Score" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
};

// Country Card Component
interface CountryCardProps {
  country: CountrySummary;
}

const CountryCard: React.FC<CountryCardProps> = ({ country }) => {
  const getRiskColor = (score: number) => {
    if (score >= 70) return 'text-red-600 bg-red-100';
    if (score >= 40) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  return (
    <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-900">{country.country.name}</h3>
          <p className="text-sm text-gray-600">{country.country.code}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(country.risk_score)}`}>
          Risk: {country.risk_score.toFixed(0)}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-gray-600 mb-1">GDP Growth</p>
          <div className="flex items-center">
            <p className="text-lg font-semibold text-gray-900">{country.gdp_growth.toFixed(1)}%</p>
            {country.gdp_growth > 0 ? (
              <TrendingUp className="h-4 w-4 text-green-600 ml-2" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600 ml-2" />
            )}
          </div>
        </div>

        <div>
          <p className="text-xs text-gray-600 mb-1">Unemployment</p>
          <p className="text-lg font-semibold text-gray-900">{country.unemployment.toFixed(1)}%</p>
        </div>

        <div>
          <p className="text-xs text-gray-600 mb-1">Inflation</p>
          <p className="text-lg font-semibold text-gray-900">{country.inflation.toFixed(1)}%</p>
        </div>

        <div>
          <p className="text-xs text-gray-600 mb-1">Business Confidence</p>
          <p className="text-lg font-semibold text-gray-900">{country.business_confidence.toFixed(0)}</p>
        </div>
      </div>
    </Card>
  );
};
