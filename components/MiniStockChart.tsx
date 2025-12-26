import dynamic from 'next/dynamic';
import { StockPriceData } from '@/lib/mockData';

// recharts는 클라이언트 사이드에서만 렌더링되도록 동적 import
const LineChart = dynamic(
  () => import('recharts').then((mod) => mod.LineChart),
  { ssr: false }
);
const Line = dynamic(() => import('recharts').then((mod) => mod.Line), { ssr: false });
const XAxis = dynamic(() => import('recharts').then((mod) => mod.XAxis), { ssr: false });
const YAxis = dynamic(() => import('recharts').then((mod) => mod.YAxis), { ssr: false });
const Tooltip = dynamic(() => import('recharts').then((mod) => mod.Tooltip), { ssr: false });
const ResponsiveContainer = dynamic(
  () => import('recharts').then((mod) => mod.ResponsiveContainer),
  { ssr: false }
);

interface MiniStockChartProps {
  data: StockPriceData[];
  isPositive: boolean;
  height?: number;
}

export default function MiniStockChart({ data, isPositive, height = 150 }: MiniStockChartProps) {
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
    <div className="mt-4">
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={formattedData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <XAxis
            dataKey="dateLabel"
            stroke="#94a3b8"
            style={{ fontSize: '10px' }}
            tick={{ fill: '#94a3b8' }}
          />
          <YAxis
            stroke="#94a3b8"
            style={{ fontSize: '10px' }}
            tick={{ fill: '#94a3b8' }}
            domain={['dataMin - 2', 'dataMax + 2']}
            tickFormatter={(value) => `$${value.toFixed(0)}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
              color: '#f1f5f9',
              fontSize: '12px',
            }}
            labelStyle={{ color: '#94a3b8' }}
            formatter={(value: number) => [`$${value.toFixed(2)}`, '주가']}
          />
          {/* 주가 라인 차트 */}
          <Line
            type="monotone"
            dataKey="price"
            stroke={chartColor}
            strokeWidth={2}
            dot={{ fill: chartColor, r: 3 }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}









