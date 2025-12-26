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
  Briefing as MockBriefing,
} from '@/lib/mockData';
import { fetchMultipleStocksNews, NewsArticle, fetchBriefings, Briefing as ApiBriefing } from '@/lib/api';

export default function Dashboard() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [news, setNews] = useState<Record<string, NewsArticle[]>>({});
  const [isLoadingNews, setIsLoadingNews] = useState(true);
  const [briefings, setBriefings] = useState<MockBriefing[]>([]);
  const [isLoadingBriefings, setIsLoadingBriefings] = useState(true);
  const topStock = getTopTrendingStock();
  const top3Stocks = getTop3TrendingStocks();

  // API 브리핑을 mock 형식으로 변환
  const convertApiBriefingToMock = (apiBriefing: ApiBriefing): MockBriefing => {
    return {
      id: apiBriefing.briefing_id,
      generatedAt: apiBriefing.generated_at,
      status: apiBriefing.status as 'completed' | 'processing' | 'failed',
      stocks: apiBriefing.stocks.map(stock => ({
        symbol: stock.symbol,
        name: stock.name,
        price: stock.price,
        change: 0, // API에서 제공하지 않음
        changePercent: stock.change_percent,
        volume: stock.volume,
        marketCap: 0, // API에서 제공하지 않음
        screenerTypes: [],
        score: 0,
      })),
      imageUrl: apiBriefing.content.image?.url || '',
      textContent: {
        title: apiBriefing.content.text.title,
        summary: apiBriefing.content.text.summary,
        sections: apiBriefing.content.text.sections.map(section => ({
          stockSymbol: section.stock_symbol || '',
          title: section.title,
          content: section.content,
        })),
      },
      sentChannels: apiBriefing.sent_channels,
      viewCount: apiBriefing.view_count,
    };
  };

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

  // 브리핑 목록 가져오기
  useEffect(() => {
    const loadBriefings = async () => {
      setIsLoadingBriefings(true);
      try {
        const data = await fetchBriefings(1, 10);
        if (data && data.briefings) {
          const convertedBriefings = data.briefings.map(convertApiBriefingToMock);
          setBriefings(convertedBriefings);
        } else {
          // API 실패 시 목업 데이터 사용
          setBriefings(mockBriefings);
        }
      } catch (error) {
        console.error('브리핑 목록 로드 실패:', error);
        // 에러 시 목업 데이터 사용
        setBriefings(mockBriefings);
      } finally {
        setIsLoadingBriefings(false);
      }
    };

    loadBriefings();
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
    <div className="space-y-10">
      {/* Hero Header - 긍정적이고 환영하는 분위기 */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-dark-card dark:via-dark-card dark:to-secondary-900/10 rounded-2xl p-8 md:p-10 shadow-lg border border-primary-100/50 dark:border-primary-900/20">
        {/* 배경 장식 요소 */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary-200/30 dark:bg-primary-800/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-secondary-200/30 dark:bg-secondary-800/10 rounded-full blur-3xl" />

        {/* 내용 */}
        <div className="relative z-10 flex items-center justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-4xl">🌅</span>
              <h1 className="text-4xl md:text-5xl font-bold">
                <span className="bg-gradient-to-r from-primary-600 via-purple-600 to-secondary-600 dark:from-primary-400 dark:via-purple-400 dark:to-secondary-400 bg-clip-text text-transparent">
                  좋은 아침입니다!
                </span>
              </h1>
            </div>
            <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl">
              오늘도 새로운 투자 기회가 기다리고 있습니다. 화제의 종목과 최신 뉴스를 확인하세요.
            </p>
          </div>

          <div className="hidden md:block">
            <Button
              onClick={handleGenerateBriefing}
              isLoading={isGenerating}
              variant="secondary"
              className="text-lg"
            >
              ✨ 브리핑 생성하기
            </Button>
          </div>
        </div>

        {/* Mobile button */}
        <div className="md:hidden mt-6 relative z-10">
          <Button
            onClick={handleGenerateBriefing}
            isLoading={isGenerating}
            variant="secondary"
            className="w-full"
          >
            ✨ 브리핑 생성하기
          </Button>
        </div>
      </div>

      {/* TOP 3 비교 */}
      <section className="section-bg-cool rounded-2xl p-6 md:p-8 border border-primary-100/50 dark:border-primary-900/20">
        <div className="flex items-center gap-3 mb-6">
          <span className="text-3xl">🏆</span>
          <h2 className="text-3xl font-bold">
            <span className="bg-gradient-to-r from-primary-600 to-purple-600 dark:from-primary-400 dark:to-purple-400 bg-clip-text text-transparent">
              TOP 3 화제 종목
            </span>
          </h2>
        </div>
        <TopStocksComparison stocks={top3Stocks} />
      </section>

      {/* 오늘의 화제 종목 */}
      <section>
        <div className="flex items-center gap-3 mb-6">
          <span className="text-3xl">📈</span>
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white">
            오늘의 화제 종목
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <StockCard stock={topStock} isLarge />
          {mockTrendingStocks.slice(1, 4).map((stock) => (
            <StockCard key={stock.symbol} stock={stock} />
          ))}
        </div>
      </section>

      {/* 최근 브리핑 히스토리 */}
      <section className="section-bg-warm rounded-2xl p-6 md:p-8 border border-secondary-100/50 dark:border-secondary-900/20">
        <div className="flex items-center gap-3 mb-6">
          <span className="text-3xl">📊</span>
          <h2 className="text-3xl font-bold">
            <span className="bg-gradient-to-r from-secondary-500 to-rose-500 dark:from-secondary-400 dark:to-rose-400 bg-clip-text text-transparent">
              최근 브리핑
            </span>
          </h2>
        </div>
        {isLoadingBriefings ? (
          <div className="card text-center py-16">
            <div className="spinner mx-auto mb-4"></div>
            <p className="text-lg text-slate-600 dark:text-slate-400">브리핑을 불러오는 중...</p>
          </div>
        ) : briefings.length === 0 ? (
          <div className="card text-center py-16">
            <div className="text-6xl mb-4">📭</div>
            <p className="text-lg text-slate-600 dark:text-slate-400 mb-2">생성된 브리핑이 없습니다.</p>
            <p className="text-sm text-slate-500 dark:text-slate-500">브리핑을 생성하면 여기에 표시됩니다.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {briefings.map((briefing) => (
              <BriefingCard key={briefing.id} briefing={briefing} />
            ))}
          </div>
        )}
      </section>

      {/* 최신 뉴스 (EXA API) */}
      <section className="section-bg-fresh rounded-2xl p-6 md:p-8 border border-accent-100/50 dark:border-accent-900/20">
        <div className="flex items-center gap-3 mb-6">
          <span className="text-3xl">📰</span>
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white">
            최신 뉴스
            <span className="ml-3 text-sm font-normal badge-primary">
              실시간 EXA API
            </span>
          </h2>
        </div>

        {isLoadingNews ? (
          <div className="card text-center py-16">
            <div className="spinner mx-auto mb-4"></div>
            <p className="text-lg text-slate-600 dark:text-slate-400">뉴스를 불러오는 중...</p>
          </div>
        ) : Object.keys(news).length === 0 ? (
          <div className="card text-center py-16">
            <div className="text-6xl mb-4">📭</div>
            <p className="text-lg text-slate-600 dark:text-slate-400 mb-2">뉴스를 불러올 수 없습니다.</p>
            <p className="text-sm text-slate-500 dark:text-slate-500">백엔드 서버가 실행 중인지 확인해주세요.</p>
          </div>
        ) : (
          <div className="space-y-8">
            {Object.entries(news).map(([ticker, articles]) => (
              <div key={ticker}>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                  <span className="px-3 py-1 rounded-lg bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 font-mono text-sm">
                    {ticker}
                  </span>
                  <span>관련 뉴스</span>
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

