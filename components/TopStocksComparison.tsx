import { useState } from 'react';
import { useRouter } from 'next/router';
import dynamic from 'next/dynamic';
import { Stock, formatCurrency, formatNumber } from '@/lib/mockData';

// recharts는 클라이언트 사이드에서만 렌더링되도록 동적 import
const BarChart = dynamic(
  () => import('recharts').then((mod) => mod.BarChart),
  { ssr: false }
);
const Bar = dynamic(() => import('recharts').then((mod) => mod.Bar), { ssr: false });
const XAxis = dynamic(() => import('recharts').then((mod) => mod.XAxis), { ssr: false });
const YAxis = dynamic(() => import('recharts').then((mod) => mod.YAxis), { ssr: false });
const CartesianGrid = dynamic(
  () => import('recharts').then((mod) => mod.CartesianGrid),
  { ssr: false }
);
const Tooltip = dynamic(() => import('recharts').then((mod) => mod.Tooltip), { ssr: false });
const Cell = dynamic(() => import('recharts').then((mod) => mod.Cell), { ssr: false });
const ResponsiveContainer = dynamic(
  () => import('recharts').then((mod) => mod.ResponsiveContainer),
  { ssr: false }
);

interface TopStocksComparisonProps {
  stocks: Stock[];
}

export default function TopStocksComparison({ stocks }: TopStocksComparisonProps) {
  const router = useRouter();
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const handleCardClick = (symbol: string) => {
    router.push(`/stocks/${symbol}`);
  };

  const getRankBadgeColor = (rank: number) => {
    switch (rank) {
      case 1:
        return 'bg-yellow-500 text-yellow-900';
      case 2:
        return 'bg-gray-400 text-gray-900';
      case 3:
        return 'bg-orange-600 text-orange-100';
      default:
        return 'bg-gray-600 text-gray-100';
    }
  };

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return `${rank}`;
    }
  };

  // 변동률 차트 데이터 준비
  const chartData = stocks.map((stock, index) => ({
    name: stock.symbol,
    변동률: stock.changePercent,
    fullName: stock.name,
    rank: index + 1,
  }));

  return (
    <div className="space-y-6">
      {/* 변동률 비교 그래프 */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-300">
          📊 TOP 3 변동률 비교
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis
              dataKey="name"
              stroke="#94a3b8"
              style={{ fontSize: '14px', fontWeight: 'bold' }}
              tick={{ fill: '#94a3b8' }}
            />
            <YAxis
              stroke="#94a3b8"
              style={{ fontSize: '12px' }}
              tick={{ fill: '#94a3b8' }}
              tickFormatter={(value) => `${value.toFixed(1)}%`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '8px',
                color: '#f1f5f9',
              }}
              labelStyle={{ color: '#94a3b8', fontWeight: 'bold' }}
              formatter={(value: number, name: string, props: any) => {
                const isPositive = value >= 0;
                const color = isPositive ? '#10b981' : '#ef4444';
                return [
                  <span style={{ color }}>
                    {isPositive ? '+' : ''}{value.toFixed(2)}%
                  </span>,
                  '변동률'
                ];
              }}
              labelFormatter={(label, payload) => {
                if (payload && payload.length > 0) {
                  const item = payload[0].payload;
                  return `${item.rank === 1 ? '🥇' : item.rank === 2 ? '🥈' : '🥉'} ${item.fullName} (${label})`;
                }
                return label;
              }}
            />
            <Bar dataKey="변동률" radius={[8, 8, 0, 0]}>
              {chartData.map((entry, index) => {
                const isPositive = entry.변동률 >= 0;
                const color = isPositive ? '#10b981' : '#ef4444';
                return <Cell key={`cell-${index}`} fill={color} />;
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* 종목 카드들 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {stocks.map((stock, index) => {
        const rank = index + 1;
        const isPositive = stock.changePercent >= 0;
        const changeColor = isPositive ? 'text-stock-up' : 'text-stock-down';
        const bgColor = isPositive ? 'bg-stock-up/10' : 'bg-stock-down/10';
        const isHovered = hoveredIndex === index;

        return (
          <div
            key={stock.symbol}
            className="card relative cursor-pointer transition-all duration-200 hover:shadow-xl hover:scale-105 hover:border-blue-500/50"
            onClick={() => handleCardClick(stock.symbol)}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            {/* 순위 뱃지 */}
            <div className="absolute top-4 right-4">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm ${getRankBadgeColor(
                  rank
                )}`}
              >
                {getRankIcon(rank)}
              </div>
            </div>

            {/* 종목 정보 */}
            <div className="mb-4 pr-12">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1 transition-colors duration-300">{stock.name}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">{stock.symbol}</p>
            </div>

            {/* 비교 항목 */}
            <div className="space-y-3">
              {/* 주가 */}
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">주가</span>
                <span className="text-gray-900 dark:text-white font-semibold text-lg transition-colors duration-300">
                  {formatCurrency(stock.price)}
                </span>
              </div>

              {/* 변동률 */}
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">변동률</span>
                <div className={`px-3 py-1 rounded-full ${bgColor}`}>
                  <span className={`font-semibold ${changeColor}`}>
                    {isPositive ? '+' : ''}
                    {stock.changePercent.toFixed(2)}%
                  </span>
                </div>
              </div>

              {/* 거래량 */}
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">거래량</span>
                <span className="text-gray-900 dark:text-white font-medium transition-colors duration-300">{formatNumber(stock.volume)}</span>
              </div>
            </div>

            {/* 호버 시 상세 정보 툴팁 */}
            {isHovered && (
              <div className="absolute bottom-full left-0 right-0 mb-2 p-4 bg-light-card dark:bg-dark-card border border-light-border dark:border-dark-border rounded-lg shadow-xl z-10 transition-colors duration-300">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">시가총액</span>
                    <span className="text-gray-900 dark:text-white font-medium transition-colors duration-300">
                      {formatNumber(stock.marketCap)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">화제도 점수</span>
                    <span className="text-gray-900 dark:text-white font-semibold transition-colors duration-300">
                      {(stock.score * 100).toFixed(1)}점
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">변동액</span>
                    <span className={`font-semibold ${changeColor}`}>
                      {isPositive ? '+' : ''}
                      {formatCurrency(stock.change)}
                    </span>
                  </div>
                  {stock.screenerTypes.length > 0 && (
                    <div className="pt-2 border-t border-light-border dark:border-dark-border transition-colors duration-300">
                      <p className="text-gray-600 dark:text-gray-400 text-xs mb-1 transition-colors duration-300">선정 기준:</p>
                      <div className="flex flex-wrap gap-1">
                        {stock.screenerTypes.map((type) => (
                          <span
                            key={type}
                            className="px-2 py-0.5 bg-blue-600/20 text-blue-400 text-xs rounded"
                          >
                            {type === 'most_actives'
                              ? '거래량 상위'
                              : type === 'day_gainers'
                              ? '상승률 상위'
                              : type === 'day_losers'
                              ? '하락률 상위'
                              : type}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  <div className="pt-2 border-t border-dark-border">
                    <p className="text-blue-400 text-xs text-center">클릭하여 상세 정보 보기</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
      </div>
    </div>
  );
}

