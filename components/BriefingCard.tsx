import Link from 'next/link';
import { useState, useEffect } from 'react';
import { Briefing, formatDate } from '@/lib/mockData';

interface BriefingCardProps {
  briefing: Briefing;
}

export default function BriefingCard({ briefing }: BriefingCardProps) {
  const [formattedDate, setFormattedDate] = useState<string>('');
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    if (briefing.generatedAt) {
      setFormattedDate(formatDate(briefing.generatedAt));
    }
  }, [briefing.generatedAt]);

  return (
    <Link href={`/briefings/${briefing.id}`}>
      <div className="group card cursor-pointer hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-glow">
        {/* 헤더 */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
              {briefing.textContent.title}
            </h3>
            <p className="text-slate-500 dark:text-slate-400 text-sm flex items-center gap-2">
              <span>📅</span>
              {isMounted && formattedDate ? (
                <span>{formattedDate}</span>
              ) : (
                <span className="text-slate-400 dark:text-slate-600">로딩 중...</span>
              )}
            </p>
          </div>

          {/* 상태 배지 */}
          <span
            className={`px-3 py-1 rounded-full text-xs font-semibold ${
              briefing.status === 'completed'
                ? 'bg-gradient-to-r from-emerald-100 to-emerald-200 dark:from-emerald-900/30 dark:to-emerald-800/30 text-emerald-700 dark:text-emerald-400'
                : briefing.status === 'processing'
                ? 'bg-gradient-to-r from-secondary-100 to-secondary-200 dark:from-secondary-900/30 dark:to-secondary-800/30 text-secondary-700 dark:text-secondary-400'
                : 'bg-gradient-to-r from-rose-100 to-rose-200 dark:from-rose-900/30 dark:to-rose-800/30 text-rose-700 dark:text-rose-400'
            }`}
          >
            {briefing.status === 'completed'
              ? '✓ 완료'
              : briefing.status === 'processing'
              ? '⏳ 처리중'
              : '✗ 실패'}
          </span>
        </div>

        {/* 요약 */}
        <p className="text-slate-700 dark:text-slate-300 text-sm mb-4 line-clamp-2">
          {briefing.textContent.summary}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-200/50 dark:border-slate-700/50">
          {/* 종목 태그 */}
          <div className="flex gap-2 flex-wrap">
            {briefing.stocks.slice(0, 3).map((stock) => (
              <span
                key={stock.symbol}
                className="px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 text-xs font-mono font-semibold rounded"
              >
                {stock.symbol}
              </span>
            ))}
            {briefing.stocks.length > 3 && (
              <span className="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 text-xs rounded">
                +{briefing.stocks.length - 3}
              </span>
            )}
          </div>

          {/* 메타 정보 */}
          <div className="flex items-center gap-3 text-sm text-slate-500 dark:text-slate-400">
            <span className="flex items-center gap-1">
              <span>👁️</span>
              <span>{briefing.viewCount}</span>
            </span>
            <div className="flex gap-1">
              {briefing.sentChannels.includes('email') && (
                <span className="text-lg">📧</span>
              )}
              {briefing.sentChannels.includes('slack') && (
                <span className="text-lg">💬</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}







