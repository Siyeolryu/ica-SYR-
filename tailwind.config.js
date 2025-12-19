/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class', // 클래스 기반 다크 모드
  theme: {
    extend: {
      colors: {
        'stock-up': '#10b981', // green-500
        'stock-down': '#ef4444', // red-500
        // 다크 모드 색상
        'dark-bg': '#0f172a', // slate-900
        'dark-card': '#1e293b', // slate-800
        'dark-border': '#334155', // slate-700
        // 라이트 모드 색상
        'light-bg': '#ffffff', // white
        'light-card': '#f8fafc', // slate-50
        'light-border': '#e2e8f0', // slate-200
      },
      transitionProperty: {
        'colors': 'background-color, border-color, color, fill, stroke',
      },
    },
  },
  plugins: [],
}







