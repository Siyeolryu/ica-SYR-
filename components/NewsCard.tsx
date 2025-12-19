import { NewsArticle } from '@/lib/api';

interface NewsCardProps {
  article: NewsArticle;
}

export default function NewsCard({ article }: NewsCardProps) {
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

  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block card hover:border-blue-500 transition-all duration-200 hover:shadow-lg"
    >
      <div className="space-y-3">
        {/* 제목 */}
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white line-clamp-2 transition-colors duration-300">
          {article.title}
        </h4>

        {/* 메타 정보 */}
        <div className="flex items-center gap-3 text-sm text-gray-600 dark:text-gray-400 transition-colors duration-300">
          <span className="flex items-center gap-1">
            <span className="text-blue-500">🔗</span>
            {article.source}
          </span>
          {article.published_date && (
            <>
              <span>•</span>
              <span>{formatDate(article.published_date)}</span>
            </>
          )}
        </div>

        {/* 저자 (있을 경우) */}
        {article.author && (
          <div className="text-sm text-gray-500 dark:text-gray-500 transition-colors duration-300">
            작성자: {article.author}
          </div>
        )}

        {/* 요약 (있을 경우) */}
        {article.summary && article.summary.trim() && (
          <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2 transition-colors duration-300">
            {article.summary}
          </p>
        )}

        {/* 외부 링크 아이콘 */}
        <div className="flex items-center gap-2 text-sm text-blue-500 dark:text-blue-400">
          <span>기사 읽기</span>
          <svg
            className="w-4 h-4"
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

