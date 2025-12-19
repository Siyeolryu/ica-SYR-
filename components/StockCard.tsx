import { Stock, formatCurrency, formatNumber, getScreenerTypeLabel, getStockPriceHistory } from '@/lib/mockData';
import StockChart from './StockChart';
import MiniStockChart from './MiniStockChart';

interface StockCardProps {
  stock: Stock;
  isLarge?: boolean;
}

export default function StockCard({ stock, isLarge = false }: StockCardProps) {
  const isPositive = stock.changePercent >= 0;
  const changeColor = isPositive ? 'text-stock-up' : 'text-stock-down';
  const bgColor = isPositive ? 'bg-stock-up/10' : 'bg-stock-down/10';

  // 모든 카드에 차트 데이터 가져오기
  const chartData = getStockPriceHistory(stock.symbol, stock.price);

  return (
    <div className={`card ${isLarge ? 'col-span-full' : ''}`}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className={`font-bold ${isLarge ? 'text-2xl' : 'text-xl'} text-gray-900 dark:text-white transition-colors duration-300`}>
            {stock.name}
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">{stock.symbol}</p>
        </div>
        <div className={`px-3 py-1 rounded-full ${bgColor}`}>
          <span className={`font-semibold ${changeColor}`}>
            {isPositive ? '+' : ''}
            {stock.changePercent.toFixed(2)}%
          </span>
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">현재가</span>
          <span className="text-gray-900 dark:text-white font-semibold text-lg transition-colors duration-300">
            {formatCurrency(stock.price)}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">변동</span>
          <span className={`font-semibold ${changeColor}`}>
            {isPositive ? '+' : ''}
            {formatCurrency(stock.change)}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">거래량</span>
          <span className="text-gray-900 dark:text-white transition-colors duration-300">{formatNumber(stock.volume)}</span>
        </div>
        {isLarge && (
          <>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">시가총액</span>
              <span className="text-gray-900 dark:text-white transition-colors duration-300">{formatNumber(stock.marketCap)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">화제도 점수</span>
              <span className="text-gray-900 dark:text-white font-semibold transition-colors duration-300">
                {(stock.score * 100).toFixed(1)}점
              </span>
            </div>
          </>
        )}
      </div>

      {/* 차트 표시 */}
      {chartData.length > 0 && (
        <>
          {isLarge ? (
            <StockChart data={chartData} isPositive={isPositive} />
          ) : (
            <MiniStockChart data={chartData} isPositive={isPositive} height={120} />
          )}
        </>
      )}

      {stock.screenerTypes.length > 0 && (
        <div className={`${isLarge ? 'mt-6' : 'mt-4'} pt-4 border-t border-light-border dark:border-dark-border transition-colors duration-300`}>
          <p className="text-gray-600 dark:text-gray-400 text-sm mb-2 transition-colors duration-300">선정 기준:</p>
          <div className="flex flex-wrap gap-2">
            {stock.screenerTypes.map((type) => (
              <span
                key={type}
                className="px-2 py-1 bg-blue-600/20 text-blue-400 text-xs rounded"
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

