import { NewsArticle } from '@/lib/api';
import { useState, useEffect } from 'react';

interface NewsCardProps {
  article: NewsArticle;
}

export default function NewsCard({ article }: NewsCardProps) {
  const [formattedDate, setFormattedDate] = useState<string>('');
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    
    const formatDate = (dateString: string) => {
      try {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffHours / 24);

        if (diffHours < 1) {
          return '방금 전';
        } else if (diffHours < 24) {
          return `${diffHours}시간 전`;
        } else if (diffDays < 7) {
          return `${diffDays}일 전`;
        } else {
          return date.toLocaleDateString('ko-KR', {
            month: 'short',
            day: 'numeric',
          });
        }
      } catch {
        return '';
      }
    };

    if (article.published_date) {
      setFormattedDate(formatDate(article.published_date));
    }
  }, [article.published_date]);

  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group block card hover:border-accent-300 dark:hover:border-accent-700 transition-all duration-200 hover:shadow-lg hover:shadow-accent-500/10"
    >
      <div className="space-y-4">
        {/* 제목 */}
        <h4 className="text-lg font-bold text-slate-900 dark:text-white line-clamp-2 group-hover:text-accent-600 dark:group-hover:text-accent-400 transition-colors">
          {article.title}
        </h4>

        {/* 메타 정보 */}
        <div className="flex items-center gap-3 text-sm">
          <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded-lg bg-accent-100 dark:bg-accent-900/30 text-accent-700 dark:text-accent-400 font-medium">
            <span>🔗</span>
            <span>{article.source}</span>
          </span>
          {isMounted && formattedDate && (
            <>
              <span className="text-slate-400 dark:text-slate-600">•</span>
              <span className="text-slate-500 dark:text-slate-400">
                {formattedDate}
              </span>
            </>
          )}
        </div>

        {/* 저자 (있을 경우) */}
        {article.author && (
          <div className="text-sm text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
            <span>✍️</span>
            <span>{article.author}</span>
          </div>
        )}

        {/* 요약 (있을 경우) */}
        {article.summary && article.summary.trim() && (
          <p className="text-sm text-slate-700 dark:text-slate-300 line-clamp-3 leading-relaxed">
            {article.summary}
          </p>
        )}

        {/* 외부 링크 CTA */}
        <div className="flex items-center gap-2 text-sm font-semibold text-accent-600 dark:text-accent-400 pt-2 border-t border-slate-200/50 dark:border-slate-700/50">
          <span>기사 읽기</span>
          <svg
            className="w-4 h-4 group-hover:translate-x-1 transition-transform"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </div>
      </div>
    </a>
  );
}



