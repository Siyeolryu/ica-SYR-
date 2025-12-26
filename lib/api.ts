/**
 * 백엔드 API 호출 유틸리티 함수
 */

const API_BASE_URL = 'http://localhost:8000';

export interface NewsArticle {
  title: string;
  url: string;
  published_date: string;
  author: string | null;
  summary: string;
  source: string;
}

export interface NewsResponse {
  success: boolean;
  data: {
    ticker: string;
    news: NewsArticle[];
    total: number;
    days_back?: number;
    period?: string;
    generated_at: string;
  };
}

export interface MultipleNewsResponse {
  success: boolean;
  data: {
    news_by_ticker: Record<string, NewsArticle[]>;
    total_tickers: number;
    total_articles: number;
    days_back: number;
    generated_at: string;
  };
}

/**
 * 특정 종목의 뉴스를 가져옵니다
 */
export async function fetchStockNews(
  ticker: string,
  limit: number = 5,
  daysBack: number = 7
): Promise<NewsArticle[]> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/v1/news/stock/${ticker}?limit=${limit}&days_back=${daysBack}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data: NewsResponse = await response.json();
    return data.data.news;
  } catch (error) {
    console.error(`Failed to fetch news for ${ticker}:`, error);
    return [];
  }
}

/**
 * 특정 종목의 24시간 뉴스를 가져옵니다
 */
export async function fetchStock24hNews(
  ticker: string,
  limit: number = 5
): Promise<NewsArticle[]> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/v1/news/stock/${ticker}/24h?limit=${limit}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data: NewsResponse = await response.json();
    return data.data.news;
  } catch (error) {
    console.error(`Failed to fetch 24h news for ${ticker}:`, error);
    return [];
  }
}

/**
 * 여러 종목의 뉴스를 한 번에 가져옵니다
 */
export async function fetchMultipleStocksNews(
  tickers: string[],
  limitPerStock: number = 3,
  daysBack: number = 7
): Promise<Record<string, NewsArticle[]>> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/v1/news/stocks/batch?limit_per_stock=${limitPerStock}&days_back=${daysBack}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tickers),
      }
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data: MultipleNewsResponse = await response.json();
    return data.data.news_by_ticker;
  } catch (error) {
    console.error('Failed to fetch multiple stocks news:', error);
    return {};
  }
}

/**
 * 백엔드 헬스체크
 */
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
}

// ============= 브리핑 관련 타입 및 함수 =============

export interface BriefingStock {
  symbol: string;
  name: string;
  price: number;
  change_percent: number;
  volume: number;
}

export interface BriefingContent {
  text: {
    title: string;
    summary: string;
    sections: Array<{
      stock_symbol?: string;
      title: string;
      content: string;
    }>;
  };
  image: {
    url: string;
    thumbnail_url: string;
    width: number;
    height: number;
    format: string;
  } | null;
}

export interface BriefingMetadata {
  template_used: string;
  generation_time_ms?: number;
  ai_model: string;
  language: string;
  docx_url?: string;
}

export interface Briefing {
  briefing_id: string;
  generated_at: string;
  status: string;
  stocks_count: number;
  stocks: BriefingStock[];
  content: BriefingContent;
  metadata: BriefingMetadata;
  sent_channels: string[];
  view_count: number;
}

export interface BriefingListResponse {
  success: boolean;
  data: {
    briefings: Briefing[];
    pagination: {
      page: number;
      limit: number;
      total: number;
      total_pages: number;
      has_next: boolean;
      has_prev: boolean;
    };
  };
}

export interface BriefingDetailResponse {
  success: boolean;
  data: Briefing;
}

/**
 * 브리핑 목록 조회
 */
export async function fetchBriefings(
  page: number = 1,
  limit: number = 20
): Promise<BriefingListResponse['data'] | null> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/v1/briefings?page=${page}&limit=${limit}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data: BriefingListResponse = await response.json();
    return data.data;
  } catch (error) {
    console.error('Failed to fetch briefings:', error);
    return null;
  }
}

/**
 * 브리핑 상세 조회
 */
export async function fetchBriefingById(briefingId: string): Promise<Briefing | null> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/v1/briefings/${briefingId}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data: BriefingDetailResponse = await response.json();
    return data.data;
  } catch (error) {
    console.error(`Failed to fetch briefing ${briefingId}:`, error);
    return null;
  }
}









