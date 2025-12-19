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
      {/* Header */}
      <header className="border-b border-light-border dark:border-dark-border bg-light-card dark:bg-dark-card transition-colors duration-300">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-gray-900 dark:text-white transition-colors duration-300">
              당신이 잠든 사이
            </Link>
            <div className="flex items-center gap-4">
              <nav className="flex gap-4">
                <Link
                  href="/"
                  className={`px-3 py-2 rounded transition-colors duration-200 ${
                    router.pathname === '/'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                  }`}
                >
                  대시보드
                </Link>
              </nav>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 transition-colors duration-300">{children}</main>
    </div>
  );
}

