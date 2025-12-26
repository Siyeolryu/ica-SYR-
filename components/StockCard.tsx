import { Stock, formatCurrency, formatNumber, getScreenerTypeLabel, getStockPriceHistory } from '@/lib/mockData';
import StockChart from './StockChart';
import MiniStockChart from './MiniStockChart';

interface StockCardProps {
  stock: Stock;
  isLarge?: boolean;
}

export default function StockCard({ stock, isLarge = false }: StockCardProps) {
  const isPositive = stock.changePercent >= 0;
  const changeColor = isPositive ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400';
  const bgColor = isPositive
    ? 'bg-gradient-to-r from-emerald-50 to-emerald-100 dark:from-emerald-900/30 dark:to-emerald-800/30'
    : 'bg-gradient-to-r from-rose-50 to-rose-100 dark:from-rose-900/30 dark:to-rose-800/30';

  // 모든 카드에 차트 데이터 가져오기
  const chartData = getStockPriceHistory(stock.symbol, stock.price);

  return (
    <div className={`group card ${isLarge ? 'col-span-full' : ''} hover:scale-[1.02] transition-transform`}>
      {/* 헤더 */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className={`font-bold ${isLarge ? 'text-3xl' : 'text-xl'} mb-1`}>
            <span className="bg-gradient-to-r from-slate-900 via-primary-700 to-slate-900 dark:from-slate-100 dark:via-primary-400 dark:to-slate-100 bg-clip-text text-transparent">
              {stock.name}
            </span>
          </h3>
          <p className="text-slate-500 dark:text-slate-400 text-sm font-medium">{stock.symbol}</p>
        </div>

        {/* 변동률 배지 - 동적 색상과 아이콘 */}
        <div className={`px-4 py-2 rounded-full font-semibold ${bgColor} transition-all duration-300`}>
          <span className={`${changeColor} flex items-center gap-1`}>
            <span className="text-lg">{isPositive ? '↗' : '↘'}</span>
            <span>
              {isPositive ? '+' : ''}
              {stock.changePercent.toFixed(2)}%
            </span>
          </span>
        </div>
      </div>

      {/* 가격 정보 - 강조된 디스플레이 */}
      <div className={`mb-6 ${isLarge ? 'py-4' : 'py-3'} px-4 rounded-xl bg-gradient-to-br from-slate-50/50 to-primary-50/30 dark:from-slate-800/30 dark:to-primary-900/20 border border-slate-200/50 dark:border-slate-700/50`}>
        <div className="flex items-baseline justify-between mb-3">
          <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">현재가</span>
          <span className={`${isLarge ? 'text-4xl' : 'text-2xl'} font-bold text-slate-900 dark:text-white`}>
            {formatCurrency(stock.price)}
          </span>
        </div>
        <div className="flex items-baseline justify-between">
          <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">변동</span>
          <span className={`text-lg font-semibold ${changeColor}`}>
            {isPositive ? '+' : ''}
            {formatCurrency(stock.change)}
          </span>
        </div>
      </div>

      {/* 차트 표시 */}
      {chartData.length > 0 && (
        <div className="mb-6">
          {isLarge ? (
            <StockChart data={chartData} isPositive={isPositive} />
          ) : (
            <MiniStockChart data={chartData} isPositive={isPositive} height={120} />
          )}
        </div>
      )}

      {/* 상세 정보 */}
      <div className="space-y-3">
        <div className="flex justify-between items-center py-2 border-b border-slate-200/50 dark:border-slate-700/50">
          <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">거래량</span>
          <span className="text-slate-900 dark:text-white font-semibold">{formatNumber(stock.volume)}</span>
        </div>
        {isLarge && (
          <>
            <div className="flex justify-between items-center py-2 border-b border-slate-200/50 dark:border-slate-700/50">
              <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">시가총액</span>
              <span className="text-slate-900 dark:text-white font-semibold">{formatNumber(stock.marketCap)}</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">화제도 점수</span>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-bold bg-gradient-to-r from-secondary-500 to-rose-500 dark:from-secondary-400 dark:to-rose-400 bg-clip-text text-transparent">
                  {(stock.score * 100).toFixed(1)}
                </span>
                <span className="text-sm text-slate-500 dark:text-slate-400">점</span>
              </div>
            </div>
          </>
        )}
      </div>

      {/* 선정 기준 배지 */}
      {stock.screenerTypes.length > 0 && (
        <div className={`${isLarge ? 'mt-6' : 'mt-4'} pt-4 border-t border-slate-200/50 dark:border-slate-700/50`}>
          <p className="text-slate-600 dark:text-slate-400 text-sm font-medium mb-3">선정 기준</p>
          <div className="flex flex-wrap gap-2">
            {stock.screenerTypes.map((type) => (
              <span
                key={type}
                className="inline-flex items-center px-3 py-1 rounded-full bg-gradient-to-r from-primary-100 to-primary-200 dark:from-primary-900/30 dark:to-primary-800/30 text-primary-700 dark:text-primary-400 text-xs font-semibold"
              >
                {getScreenerTypeLabel(type)}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

