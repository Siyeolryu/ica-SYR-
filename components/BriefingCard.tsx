import Link from 'next/link';
import { Briefing, formatDate } from '@/lib/mockData';

interface BriefingCardProps {
  briefing: Briefing;
}

export default function BriefingCard({ briefing }: BriefingCardProps) {
  return (
    <Link href={`/briefings/${briefing.id}`}>
      <div className="card hover:border-blue-500 transition-colors cursor-pointer">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1 transition-colors duration-300">
              {briefing.textContent.title}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">{formatDate(briefing.generatedAt)}</p>
          </div>
          <span
            className={`px-2 py-1 rounded text-xs ${
              briefing.status === 'completed'
                ? 'bg-green-600/20 text-green-400'
                : briefing.status === 'processing'
                ? 'bg-yellow-600/20 text-yellow-400'
                : 'bg-red-600/20 text-red-400'
            }`}
          >
            {briefing.status === 'completed'
              ? '완료'
              : briefing.status === 'processing'
              ? '처리중'
              : '실패'}
          </span>
        </div>

        <p className="text-gray-700 dark:text-gray-300 text-sm mb-4 line-clamp-2 transition-colors duration-300">
          {briefing.textContent.summary}
        </p>

        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            {briefing.stocks.slice(0, 3).map((stock) => (
              <span
                key={stock.symbol}
                className="px-2 py-1 bg-light-border dark:bg-dark-border text-gray-700 dark:text-gray-300 text-xs rounded transition-colors duration-300"
              >
                {stock.symbol}
              </span>
            ))}
            {briefing.stocks.length > 3 && (
              <span className="px-2 py-1 bg-light-border dark:bg-dark-border text-gray-600 dark:text-gray-400 text-xs rounded transition-colors duration-300">
                +{briefing.stocks.length - 3}
              </span>
            )}
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 transition-colors duration-300">
            <span>조회 {briefing.viewCount}</span>
            <div className="flex gap-1">
              {briefing.sentChannels.includes('email') && (
                <span className="text-blue-400">📧</span>
              )}
              {briefing.sentChannels.includes('slack') && (
                <span className="text-purple-400">💬</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}







