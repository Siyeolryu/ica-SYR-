import dynamic from 'next/dynamic';
import { StockPriceData } from '@/lib/mockData';

// recharts는 클라이언트 사이드에서만 렌더링되도록 동적 import
const ComposedChart = dynamic(
  () => import('recharts').then((mod) => mod.ComposedChart),
  { ssr: false }
);
const Line = dynamic(() => import('recharts').then((mod) => mod.Line), { ssr: false });
const Bar = dynamic(() => import('recharts').then((mod) => mod.Bar), { ssr: false });
const XAxis = dynamic(() => import('recharts').then((mod) => mod.XAxis), { ssr: false });
const YAxis = dynamic(() => import('recharts').then((mod) => mod.YAxis), { ssr: false });
const CartesianGrid = dynamic(
  () => import('recharts').then((mod) => mod.CartesianGrid),
  { ssr: false }
);
const Tooltip = dynamic(() => import('recharts').then((mod) => mod.Tooltip), { ssr: false });
const ResponsiveContainer = dynamic(
  () => import('recharts').then((mod) => mod.ResponsiveContainer),
  { ssr: false }
);

interface StockChartProps {
  data: StockPriceData[];
  isPositive: boolean;
}

export default function StockChart({ data, isPositive }: StockChartProps) {
  const chartColor = isPositive ? '#10b981' : '#ef4444'; // 녹색 또는 빨간색

  // 날짜 포맷팅 (MM/DD 형식)
  const formattedData = data.map((item) => ({
    ...item,
    dateLabel: new Date(item.date).toLocaleDateString('ko-KR', {
      month: '2-digit',
      day: '2-digit',
    }),
  }));

  return (
    <div className="mt-6">
      <h4 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-4 transition-colors duration-300">최근 5일 주가 추이</h4>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={formattedData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="dateLabel"
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            yAxisId="left"
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
            domain={['dataMin - 2', 'dataMax + 2']}
            tickFormatter={(value) => `$${value.toFixed(0)}`}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            stroke="#64748b"
            style={{ fontSize: '12px' }}
            tickFormatter={(value) => `${(value / 1000000).toFixed(0)}M`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
              color: '#f1f5f9',
            }}
            labelStyle={{ color: '#94a3b8' }}
            formatter={(value: number, name: string) => {
              if (name === 'price') {
                return [`$${value.toFixed(2)}`, '주가'];
              }
              if (name === 'volume') {
                return [`${(value / 1000000).toFixed(2)}M`, '거래량'];
              }
              return [value, name];
            }}
          />
          {/* 주가 라인 차트 */}
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="price"
            stroke={chartColor}
            strokeWidth={2}
            dot={{ fill: chartColor, r: 4 }}
            activeDot={{ r: 6 }}
          />
          {/* 거래량 바 차트 */}
          <Bar
            yAxisId="right"
            dataKey="volume"
            fill={isPositive ? '#10b98140' : '#ef444440'}
            radius={[4, 4, 0, 0]}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

