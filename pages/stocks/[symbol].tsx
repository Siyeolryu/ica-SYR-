import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import { getStockBySymbol, formatCurrency, formatNumber, getScreenerTypeLabel, getStockPriceHistory } from '@/lib/mockData';
import StockChart from '@/components/StockChart';
import NewsCard from '@/components/NewsCard';
import Button from '@/components/Button';
import { fetchStockNews, NewsArticle } from '@/lib/api';

export default function StockDetail() {
  const router = useRouter();
  const { symbol } = router.query;
  const stock = symbol ? getStockBySymbol(symbol as string) : null;
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [isLoadingNews, setIsLoadingNews] = useState(true);

  // 뉴스 가져오기
  useEffect(() => {
    if (symbol && typeof symbol === 'string') {
      const loadNews = async () => {
        setIsLoadingNews(true);
        const newsData = await fetchStockNews(symbol, 6, 7);
        setNews(newsData);
        setIsLoadingNews(false);
      };
      loadNews();
    }
  }, [symbol]);

  if (!stock) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-600 dark:text-gray-400 text-lg mb-4 transition-colors duration-300">종목을 찾을 수 없습니다.</p>
        <Button variant="secondary" onClick={() => router.push('/')}>
          대시보드로 돌아가기
        </Button>
      </div>
    );
  }

  const isPositive = stock.changePercent >= 0;
  const changeColor = isPositive ? 'text-stock-up' : 'text-stock-down';
  const bgColor = isPositive ? 'bg-stock-up/10' : 'bg-stock-down/10';
  const chartData = getStockPriceHistory(stock.symbol, stock.price);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2 transition-colors duration-300">{stock.name}</h1>
          <p className="text-gray-600 dark:text-gray-400 transition-colors duration-300">{stock.symbol}</p>
        </div>
        <Button variant="secondary" onClick={() => router.push('/')}>
          대시보드로 돌아가기
        </Button>
      </div>

      {/* 주요 정보 카드 */}
      <section className="card">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 transition-colors duration-300">주요 정보</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-1 transition-colors duration-300">현재가</p>
            <p className="text-gray-900 dark:text-white font-bold text-2xl transition-colors duration-300">{formatCurrency(stock.price)}</p>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-1 transition-colors duration-300">변동</p>
            <div className="flex items-center gap-2">
              <span className={`font-bold text-xl ${changeColor}`}>
                {isPositive ? '+' : ''}
                {formatCurrency(stock.change)}
              </span>
              <span className={`px-3 py-1 rounded-full ${bgColor}`}>
                <span className={`font-semibold ${changeColor}`}>
                  {isPositive ? '+' : ''}
                  {stock.changePercent.toFixed(2)}%
                </span>
              </span>
            </div>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-1 transition-colors duration-300">거래량</p>
            <p className="text-gray-900 dark:text-white font-semibold text-xl transition-colors duration-300">{formatNumber(stock.volume)}</p>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-1 transition-colors duration-300">시가총액</p>
            <p className="text-gray-900 dark:text-white font-semibold text-xl transition-colors duration-300">{formatNumber(stock.marketCap)}</p>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-1 transition-colors duration-300">화제도 점수</p>
            <p className="text-gray-900 dark:text-white font-semibold text-xl transition-colors duration-300">{(stock.score * 100).toFixed(1)}점</p>
          </div>
          {stock.screenerTypes.length > 0 && (
            <div>
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-2 transition-colors duration-300">선정 기준</p>
              <div className="flex flex-wrap gap-2">
                {stock.screenerTypes.map((type) => (
                  <span
                    key={type}
                    className="px-3 py-1 bg-blue-600/20 text-blue-400 text-sm rounded"
                  >
                    {getScreenerTypeLabel(type)}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* 주가 차트 */}
      {chartData.length > 0 && (
        <section className="card">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-300">최근 5일 주가 추이</h2>
          <StockChart data={chartData} isPositive={isPositive} />
        </section>
      )}

      {/* 관련 뉴스 (EXA API) */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-300">
          📰 관련 뉴스 <span className="text-sm text-blue-500">(실시간 EXA API)</span>
        </h2>
        {isLoadingNews ? (
          <div className="card text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">뉴스를 불러오는 중...</p>
          </div>
        ) : news.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">최근 뉴스가 없습니다.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {news.map((article, index) => (
              <NewsCard key={index} article={article} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

