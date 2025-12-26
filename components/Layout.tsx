import Link from 'next/link';
import { useRouter } from 'next/router';
import ThemeToggle from './ThemeToggle';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-light-bg dark:bg-dark-bg transition-colors duration-300">
      {/* Header - 그라데이션 배경과 글로우 효과 */}
      <header className="relative border-b border-light-border/50 dark:border-dark-border/50 bg-gradient-to-r from-white via-primary-50/30 to-secondary-50/20 dark:from-dark-card dark:via-dark-card/80 dark:to-dark-card backdrop-blur-sm transition-colors duration-300">
        {/* 헤더 배경 장식 요소 */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-0 right-1/4 w-64 h-64 bg-primary-200/20 dark:bg-primary-800/5 rounded-full blur-3xl" />
          <div className="absolute top-0 left-1/4 w-48 h-48 bg-secondary-200/20 dark:bg-secondary-800/5 rounded-full blur-3xl" />
        </div>

        <div className="container mx-auto px-4 py-5 relative z-10">
          <div className="flex items-center justify-between">
            {/* 로고 - 그라데이션 텍스트 */}
            <Link href="/" className="group">
              <h1 className="text-2xl md:text-3xl font-bold">
                <span className="bg-gradient-to-r from-primary-600 via-purple-600 to-secondary-600 dark:from-primary-400 dark:via-purple-400 dark:to-secondary-400 bg-clip-text text-transparent transition-all duration-300 group-hover:from-primary-700 group-hover:via-purple-700 group-hover:to-secondary-700">
                  당신이 잠든 사이
                </span>
              </h1>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                While You Were Sleeping
              </p>
            </Link>

            <div className="flex items-center gap-6">
              {/* Navigation */}
              <nav className="hidden md:flex gap-2">
                <Link
                  href="/"
                  className={`relative px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    router.pathname === '/'
                      ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg shadow-primary-500/30'
                      : 'text-slate-600 dark:text-slate-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20'
                  }`}
                >
                  <span className="relative z-10">대시보드</span>
                </Link>
              </nav>

              {/* Theme Toggle */}
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 transition-colors duration-300">
        {children}
      </main>

      {/* Footer - 부드러운 그라데이션 */}
      <footer className="mt-16 border-t border-light-border/50 dark:border-dark-border/50 bg-gradient-to-b from-transparent to-primary-50/20 dark:to-primary-900/5">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-sm text-slate-500 dark:text-slate-400">
            <p className="mb-2">
              🌅 매일 아침 새로운 기회를 발견하세요
            </p>
            <p className="text-xs">
              © 2024 당신이 잠든 사이. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

