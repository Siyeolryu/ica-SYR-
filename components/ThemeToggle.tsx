import { useTheme } from '@/contexts/ThemeContext';

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="relative w-16 h-9 rounded-full bg-gradient-to-r from-secondary-200 to-secondary-300 dark:from-primary-800 dark:to-primary-900 transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-primary-400/30 dark:focus:ring-primary-600/30 hover:shadow-lg hover:shadow-primary-500/20"
      aria-label={`${theme === 'dark' ? '라이트' : '다크'} 모드로 전환`}
      type="button"
    >
      {/* 배경 장식 */}
      <span className="absolute inset-0 rounded-full overflow-hidden">
        <span className={`absolute inset-0 bg-gradient-to-r from-secondary-100 to-primary-100 dark:from-primary-900 dark:to-purple-900 opacity-50 transition-opacity duration-300`} />
      </span>

      {/* 토글 스위치 */}
      <span
        className={`absolute top-1 w-7 h-7 rounded-full bg-white dark:bg-slate-800 shadow-lg transform transition-all duration-300 flex items-center justify-center border-2 border-secondary-300 dark:border-primary-700 ${
          theme === 'dark' ? 'translate-x-8 left-0' : 'translate-x-1 left-0'
        }`}
      >
        <span className="text-xl transition-transform duration-300 hover:scale-110" role="img" aria-hidden="true">
          {theme === 'dark' ? '🌙' : '☀️'}
        </span>
      </span>
    </button>
  );
}














