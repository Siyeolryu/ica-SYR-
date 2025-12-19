import { useState, useEffect } from 'react';
import StockCard from '@/components/StockCard';
import BriefingCard from '@/components/BriefingCard';
import TopStocksComparison from '@/components/TopStocksComparison';
import NewsCard from '@/components/NewsCard';
import Button from '@/components/Button';
import {
  getTopTrendingStock,
  getTop3TrendingStocks,
  mockBriefings,
  mockTrendingStocks,
} from '@/lib/mockData';
import { fetchMultipleStocksNews, NewsArticle } from '@/lib/api';

export default function Dashboard() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [news, setNews] = useState<Record<string, NewsArticle[]>>({});
  const [isLoadingNews, setIsLoadingNews] = useState(true);
  const topStock = getTopTrendingStock();
  const top3Stocks = getTop3TrendingStocks();

  // 최신 뉴스 가져오기
  useEffect(() => {
    const loadNews = async () => {
      setIsLoadingNews(true);
      const tickers = ['AAPL', 'TSLA', 'NVDA'];
      const newsData = await fetchMultipleStocksNews(tickers, 3, 3);
      setNews(newsData);
      setIsLoadingNews(false);
    };

    loadNews();
  }, []);

  const handleGenerateBriefing = async () => {
    setIsGenerating(true);
    // 목업: 브리핑 생성 시뮬레이션
    setTimeout(() => {
      setIsGenerating(false);
      alert('브리핑이 생성되었습니다! (목업)');
    }, 2000);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2 transition-colors duration-300">대시보드</h1>
          <p className="text-gray-600 dark:text-gray-400 transition-colors duration-300">오늘의 화제 종목과 최근 브리핑을 확인하세요</p>
        </div>
        <Button onClick={handleGenerateBriefing} isLoading={isGenerating}>
          브리핑 생성
        </Button>
      </div>

      {/* TOP 3 비교 */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-300">화제 종목 TOP 3 비교</h2>
        <TopStocksComparison stocks={top3Stocks} />
      </section>

      {/* 오늘의 화제 종목 */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-300">오늘의 화제 종목</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <StockCard stock={topStock} isLarge />
          {mockTrendingStocks.slice(1, 4).map((stock) => (
            <StockCard key={stock.symbol} stock={stock} />
          ))}
        </div>
      </section>

      {/* 최근 브리핑 히스토리 */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-300">최근 브리핑</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockBriefings.map((briefing) => (
            <BriefingCard key={briefing.id} briefing={briefing} />
          ))}
        </div>
      </section>

      {/* 최신 뉴스 (EXA API) */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-300">
          📰 최신 뉴스 <span className="text-sm text-blue-500">(실시간 EXA API)</span>
        </h2>
        {isLoadingNews ? (
          <div className="card text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">뉴스를 불러오는 중...</p>
          </div>
        ) : Object.keys(news).length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">뉴스를 불러올 수 없습니다.</p>
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">백엔드 서버가 실행 중인지 확인해주세요.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {Object.entries(news).map(([ticker, articles]) => (
              <div key={ticker}>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 transition-colors duration-300">
                  {ticker} 관련 뉴스
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {articles.map((article, index) => (
                    <NewsCard key={`${ticker}-${index}`} article={article} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

