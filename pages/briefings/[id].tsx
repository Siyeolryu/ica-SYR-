import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import { getBriefingById, formatDate } from '@/lib/mockData';
import Button from '@/components/Button';
import StockCard from '@/components/StockCard';
import NewsCard from '@/components/NewsCard';
import { fetchMultipleStocksNews, NewsArticle } from '@/lib/api';

export default function BriefingDetail() {
  const router = useRouter();
  const { id } = router.query;
  const briefing = id ? getBriefingById(id as string) : null;
  const [isSending, setIsSending] = useState(false);
  const [sendChannel, setSendChannel] = useState<'email' | 'slack' | null>(null);
  const [news, setNews] = useState<Record<string, NewsArticle[]>>({});
  const [isLoadingNews, setIsLoadingNews] = useState(true);

  // 브리핑에 포함된 종목들의 뉴스 가져오기
  useEffect(() => {
    if (briefing && briefing.stocks.length > 0) {
      const loadNews = async () => {
        setIsLoadingNews(true);
        const tickers = briefing.stocks.map(stock => stock.symbol);
        const newsData = await fetchMultipleStocksNews(tickers, 3, 7);
        setNews(newsData);
        setIsLoadingNews(false);
      };
      loadNews();
    }
  }, [briefing]);

  if (!briefing) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-400 text-lg">브리핑을 찾을 수 없습니다.</p>
        <Button
          variant="secondary"
          className="mt-4"
          onClick={() => router.push('/')}
        >
          대시보드로 돌아가기
        </Button>
      </div>
    );
  }

  const handleSend = async (channel: 'email' | 'slack') => {
    setSendChannel(channel);
    setIsSending(true);
    
    // 목업: 발송 시뮬레이션
    setTimeout(() => {
      setIsSending(false);
      setSendChannel(null);
      alert(`${channel === 'email' ? '이메일' : '슬랙'}으로 발송되었습니다! (목업)`);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={() => router.back()}
            className="text-gray-400 hover:text-white mb-2"
          >
            ← 뒤로가기
          </button>
          <h1 className="text-3xl font-bold text-white">{briefing.textContent.title}</h1>
          <p className="text-gray-400 mt-1">{formatDate(briefing.generatedAt)}</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="primary"
            onClick={() => handleSend('email')}
            isLoading={isSending && sendChannel === 'email'}
            disabled={isSending}
          >
            📧 이메일 발송
          </Button>
          <Button
            variant="primary"
            onClick={() => handleSend('slack')}
            isLoading={isSending && sendChannel === 'slack'}
            disabled={isSending}
          >
            💬 슬랙 발송
          </Button>
        </div>
      </div>

      {/* 브리핑 이미지 미리보기 */}
      <section className="card">
        <h2 className="text-xl font-semibold text-white mb-4">브리핑 이미지</h2>
        <div className="bg-dark-bg rounded-lg border border-dark-border p-4 flex items-center justify-center">
          <div className="relative w-full max-w-3xl aspect-[3/4]">
            <Image
              src={briefing.imageUrl}
              alt="브리핑 이미지"
              fill
              className="object-contain rounded-lg"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 80vw, 1200px"
              priority
              onError={(e) => {
                // 이미지 로드 실패 시 플레이스홀더 표시
                const target = e.target as HTMLImageElement;
                target.src = `https://via.placeholder.com/1200x1600/1e293b/64748b?text=브리핑+이미지`;
              }}
            />
          </div>
        </div>
      </section>

      {/* 리포트 텍스트 */}
      <section className="card">
        <h2 className="text-xl font-semibold text-white mb-4">리포트</h2>
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">요약</h3>
            <p className="text-gray-300 leading-relaxed">{briefing.textContent.summary}</p>
          </div>

          {briefing.textContent.sections.map((section, index) => (
            <div key={index} className="border-t border-dark-border pt-6">
              <h3 className="text-lg font-semibold text-white mb-2">{section.title}</h3>
              <p className="text-gray-300 leading-relaxed">{section.content}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 포함된 종목 */}
      <section>
        <h2 className="text-xl font-semibold text-white mb-4">포함된 종목</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {briefing.stocks.map((stock) => (
            <StockCard key={stock.symbol} stock={stock} />
          ))}
        </div>
      </section>

      {/* 메타데이터 */}
      <section className="card">
        <h2 className="text-xl font-semibold text-white mb-4">상세 정보</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-gray-400 text-sm mb-1">상태</p>
            <p className="text-white font-semibold">
              {briefing.status === 'completed'
                ? '완료'
                : briefing.status === 'processing'
                ? '처리중'
                : '실패'}
            </p>
          </div>
          <div>
            <p className="text-gray-400 text-sm mb-1">조회수</p>
            <p className="text-white font-semibold">{briefing.viewCount}</p>
          </div>
          <div>
            <p className="text-gray-400 text-sm mb-1">발송 채널</p>
            <div className="flex gap-2">
              {briefing.sentChannels.includes('email') && (
                <span className="text-blue-400">📧</span>
              )}
              {briefing.sentChannels.includes('slack') && (
                <span className="text-purple-400">💬</span>
              )}
            </div>
          </div>
          <div>
            <p className="text-gray-400 text-sm mb-1">종목 수</p>
            <p className="text-white font-semibold">{briefing.stocks.length}개</p>
          </div>
        </div>
      </section>

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
        ) : Object.keys(news).length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">관련 뉴스가 없습니다.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {Object.entries(news).map(([ticker, articles]) => (
              articles.length > 0 && (
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
              )
            ))}
          </div>
        )}
      </section>
    </div>
  );
}












