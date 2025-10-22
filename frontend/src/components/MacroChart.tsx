/**
 * MacroChart Component
 * Reusable chart component for displaying economic data
 */

import { FC } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  TooltipProps,
} from 'recharts';
import { COUNTRY_COLORS } from '../services/macroService';

export type ChartType = 'line' | 'bar' | 'area';

interface MacroChartProps {
  data: any[];
  chartType?: ChartType;
  title: string;
  yAxisLabel: string;
  countries?: string[];
  height?: number;
}

const MacroChart: FC<MacroChartProps> = ({
  data,
  chartType = 'line',
  title,
  yAxisLabel,
  countries = ['NLD', 'BEL', 'LUX', 'DEU'],
  height = 400,
}) => {
  // Custom tooltip formatter
  const CustomTooltip: FC<TooltipProps<number, string>> = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-800 mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {typeof entry.value === 'number' ? entry.value.toFixed(2) : entry.value}%
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  // Render appropriate chart based on type
  const renderChart = () => {
    const commonProps = {
      data,
      margin: { top: 5, right: 30, left: 20, bottom: 5 },
    };

    const commonAxisProps = {
      xAxis: {
        dataKey: 'year',
        stroke: '#6B7280',
      },
      yAxis: {
        stroke: '#6B7280',
        label: { value: yAxisLabel, angle: -90, position: 'insideLeft' },
      },
    };

    switch (chartType) {
      case 'bar':
        return (
          <BarChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis {...commonAxisProps.xAxis} />
            <YAxis {...commonAxisProps.yAxis} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            {countries.map((country) => (
              <Bar
                key={country}
                dataKey={country}
                fill={COUNTRY_COLORS[country as keyof typeof COUNTRY_COLORS]}
                name={country}
              />
            ))}
          </BarChart>
        );

      case 'area':
        return (
          <AreaChart {...commonProps}>
            <defs>
              {countries.map((country) => (
                <linearGradient
                  key={`gradient-${country}`}
                  id={`color-${country}`}
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop
                    offset="5%"
                    stopColor={COUNTRY_COLORS[country as keyof typeof COUNTRY_COLORS]}
                    stopOpacity={0.8}
                  />
                  <stop
                    offset="95%"
                    stopColor={COUNTRY_COLORS[country as keyof typeof COUNTRY_COLORS]}
                    stopOpacity={0.1}
                  />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis {...commonAxisProps.xAxis} />
            <YAxis {...commonAxisProps.yAxis} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            {countries.map((country) => (
              <Area
                key={country}
                type="monotone"
                dataKey={country}
                stroke={COUNTRY_COLORS[country as keyof typeof COUNTRY_COLORS]}
                fillOpacity={1}
                fill={`url(#color-${country})`}
                name={country}
              />
            ))}
          </AreaChart>
        );

      case 'line':
      default:
        return (
          <LineChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis {...commonAxisProps.xAxis} />
            <YAxis {...commonAxisProps.yAxis} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            {countries.map((country) => (
              <Line
                key={country}
                type="monotone"
                dataKey={country}
                stroke={COUNTRY_COLORS[country as keyof typeof COUNTRY_COLORS]}
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
                name={country}
              />
            ))}
          </LineChart>
        );
    }
  };

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={height}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
};

export default MacroChart;
