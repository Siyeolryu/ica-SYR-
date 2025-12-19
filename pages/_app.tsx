// @ts-nocheck
import '@/styles/globals.css';
// @ts-ignore - Next.js 타입 정의
import type { AppProps } from 'next/app';
// @ts-ignore - Next.js 타입 정의
import Head from 'next/head';
// @ts-ignore - React 타입 정의
import React, { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import { ThemeProvider } from '@/contexts/ThemeContext';

// 에러 표시 컴포넌트 (개선 버전)
function ErrorFallback({ 
  error, 
  resetError 
}: { 
  error: Error; 
  resetError: () => void;
}) {
  // 사용자 친화적인 에러 메시지
  const getErrorMessage = (error: Error): string => {
    const message = error.message || '알 수 없는 오류가 발생했습니다.';
    
    // 기술적 에러 메시지를 사용자 친화적으로 변환
    if (message.includes('Network') || message.includes('fetch')) {
      return '인터넷 연결을 확인해주세요.';
    }
    if (message.includes('timeout')) {
      return '요청 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.';
    }
    if (message.includes('404')) {
      return '요청한 페이지를 찾을 수 없습니다.';
    }
    
    return '일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
  };

  return (
    <div className="min-h-screen bg-light-bg dark:bg-dark-bg flex items-center justify-center px-4 transition-colors duration-300">
      {/* 인라인 스타일로 스타일 의존성 제거 */}
      <div className="bg-light-card dark:bg-dark-card rounded-lg border border-light-border dark:border-dark-border p-6 shadow-lg text-center max-w-md transition-colors duration-300">
        <h2 className="text-2xl font-bold text-red-500 mb-4" role="alert">
          ⚠️ 오류가 발생했습니다
        </h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4 transition-colors duration-300">
          {getErrorMessage(error)}
        </p>
        {/* 개발 환경에서만 상세 에러 표시 */}
        {(() => {
          // Next.js에서 process.env는 빌드 타임에 주입됨
          try {
            // @ts-ignore - Next.js 환경 변수는 빌드 타임에 주입됨
            return process.env.NODE_ENV === 'development';
          } catch {
            return false;
          }
        })() && (
          <details className="mb-4 text-left">
            <summary className="text-gray-600 dark:text-gray-400 text-sm cursor-pointer mb-2 transition-colors duration-300">
              개발자 정보 (개발 환경에서만 표시)
            </summary>
            <pre className="text-xs text-gray-600 dark:text-gray-500 bg-light-bg dark:bg-dark-bg p-2 rounded overflow-auto transition-colors duration-300">
              {error.message || '알 수 없는 오류'}
            </pre>
          </details>
        )}
        <div className="flex gap-2 justify-center">
          <button
            onClick={resetError}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200"
            type="button"
            aria-label="다시 시도"
          >
            다시 시도
          </button>
          <button
            onClick={() => window.location.href = '/'}
            className="bg-light-card dark:bg-dark-card hover:bg-light-border dark:hover:bg-dark-border border border-light-border dark:border-dark-border text-gray-900 dark:text-gray-100 font-semibold py-2 px-4 rounded-lg transition-colors duration-200"
            type="button"
            aria-label="홈으로 이동"
          >
            홈으로
          </button>
        </div>
      </div>
    </div>
  );
}

export default function App({ Component, pageProps }: AppProps) {
  const [error, setError] = useState<Error | null>(null);

  // 전역 에러 핸들러
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      console.error('Global error:', event.error);
      setError(event.error || new Error('알 수 없는 오류가 발생했습니다.'));
    };

    const handleRejection = (event: PromiseRejectionEvent) => {
      console.error('Unhandled promise rejection:', event.reason);
      const errorMessage = event.reason?.message || '처리되지 않은 오류가 발생했습니다.';
      setError(new Error(errorMessage));
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleRejection);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleRejection);
    };
  }, []);

  // 에러가 있으면 에러 화면 표시
  if (error) {
    return (
      <>
        <Head>
          <title>오류 - 당신이 잠든 사이</title>
          <meta name="robots" content="noindex, nofollow" />
        </Head>
        <ErrorFallback 
          error={error} 
          resetError={() => {
            // 전체 페이지 새로고침 대신 에러 상태만 초기화
            setError(null);
            // 필요시 라우터를 사용하여 네비게이션
            // router.push('/');
          }} 
        />
      </>
    );
  }

  // 페이지에서 Layout을 사용하지 않도록 설정할 수 있는 옵션
  const noLayout = (Component as typeof Component & { noLayout?: boolean }).noLayout || false;

  return (
    <>
      {/* 기본 메타 태그 (페이지에서 오버라이드 가능) */}
      <Head>
        <title>당신이 잠든 사이 - 미국 주식 데일리 브리핑</title>
        <meta 
          name="description" 
          content="한국인 투자자를 위한 미국 주식 데일리 브리핑 서비스. 오늘의 화제 종목을 확인하고 브리핑을 받아보세요." 
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#0f172a" />
        {/* Open Graph 메타 태그 추가 */}
        <meta property="og:type" content="website" />
        <meta property="og:title" content="당신이 잠든 사이 - 미국 주식 데일리 브리핑" />
        <meta property="og:description" content="한국인 투자자를 위한 미국 주식 데일리 브리핑 서비스" />
        {/* Twitter Card 메타 태그 추가 */}
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:title" content="당신이 잠든 사이" />
        <meta name="twitter:description" content="미국 주식 데일리 브리핑 서비스" />
      </Head>
      <ThemeProvider>
        {noLayout ? (
          <Component {...pageProps} />
        ) : (
          <Layout>
            <Component {...pageProps} />
          </Layout>
        )}
      </ThemeProvider>
    </>
  );
}
