export interface Stock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: number;
  screenerTypes: string[];
  score: number;
}

export interface StockPriceData {
  date: string;
  price: number;
  volume: number;
}

export interface Briefing {
  id: string;
  generatedAt: string;
  status: 'completed' | 'processing' | 'failed';
  stocks: Stock[];
  imageUrl: string;
  textContent: {
    title: string;
    summary: string;
    sections: {
      stockSymbol: string;
      title: string;
      content: string;
    }[];
  };
  sentChannels: string[];
  viewCount: number;
}

export const mockTrendingStocks: Stock[] = [
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: 185.50,
    change: 4.25,
    changePercent: 2.35,
    volume: 45234567,
    marketCap: 2850000000000,
    screenerTypes: ['most_actives', 'day_gainers'],
    score: 0.875,
  },
  {
    symbol: 'TSLA',
    name: 'Tesla, Inc.',
    price: 245.30,
    change: 11.95,
    changePercent: 5.12,
    volume: 38923456,
    marketCap: 780000000000,
    screenerTypes: ['day_gainers'],
    score: 0.823,
  },
  {
    symbol: 'MSFT',
    name: 'Microsoft Corporation',
    price: 378.85,
    change: -2.15,
    changePercent: -0.56,
    volume: 23456789,
    marketCap: 2810000000000,
    screenerTypes: ['most_actives'],
    score: 0.756,
  },
  {
    symbol: 'NVDA',
    name: 'NVIDIA Corporation',
    price: 495.20,
    change: 12.50,
    changePercent: 2.59,
    volume: 45678901,
    marketCap: 1220000000000,
    screenerTypes: ['most_actives', 'day_gainers'],
    score: 0.812,
  },
  {
    symbol: 'AMZN',
    name: 'Amazon.com, Inc.',
    price: 152.30,
    change: -1.20,
    changePercent: -0.78,
    volume: 34567890,
    marketCap: 1580000000000,
    screenerTypes: ['most_actives'],
    score: 0.698,
  },
];

// 오늘 날짜 기준으로 브리핑 날짜 생성
const today = new Date();
const yesterday = new Date(today);
yesterday.setDate(yesterday.getDate() - 1);
const twoDaysAgo = new Date(today);
twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);

export const mockBriefings: Briefing[] = [
  {
    id: `brf_${today.toISOString().split('T')[0].replace(/-/g, '')}_060000_abc123`,
    generatedAt: today.toISOString(),
    status: 'completed',
    stocks: [mockTrendingStocks[0], mockTrendingStocks[1]],
    imageUrl: 'https://via.placeholder.com/1200x1600/1e293b/64748b?text=Today%27s+Briefing',
    textContent: {
      title: '오늘의 화제 종목 브리핑',
      summary: `${today.getFullYear()}년 ${today.getMonth() + 1}월 ${today.getDate()}일 미국 증시에서 가장 활발했던 종목들을 정리했습니다. 애플과 테슬라가 거래량과 상승률에서 두각을 나타냈습니다.`,
      sections: [
        {
          stockSymbol: 'AAPL',
          title: 'Apple Inc. (AAPL)',
          content: '애플은 전일 대비 2.35% 상승하며 거래량 4,523만 주를 기록했습니다. Morgan Stanley가 목표가를 상향 조정하며 투자자들의 관심이 집중되고 있습니다.',
        },
        {
          stockSymbol: 'TSLA',
          title: 'Tesla, Inc. (TSLA)',
          content: '테슬라는 5.12%의 큰 폭 상승을 기록하며 거래량 3,892만 주를 달성했습니다. Cathie Wood의 포트폴리오 조정 소식과 함께 시장의 주목을 받고 있습니다.',
        },
      ],
    },
    sentChannels: ['email', 'slack'],
    viewCount: 24,
  },
  {
    id: `brf_${yesterday.toISOString().split('T')[0].replace(/-/g, '')}_060000_xyz789`,
    generatedAt: yesterday.toISOString(),
    status: 'completed',
    stocks: [mockTrendingStocks[2], mockTrendingStocks[3]],
    imageUrl: 'https://via.placeholder.com/1200x1600/1e293b/64748b?text=Yesterday%27s+Briefing',
    textContent: {
      title: '어제의 화제 종목 브리핑',
      summary: `${yesterday.getFullYear()}년 ${yesterday.getMonth() + 1}월 ${yesterday.getDate()}일 미국 증시 동향입니다.`,
      sections: [
        {
          stockSymbol: 'MSFT',
          title: 'Microsoft Corporation (MSFT)',
          content: '마이크로소프트는 거래량 2,345만 주를 기록했습니다. AI 및 클라우드 성장으로 600달러 돌파 전망이 나오고 있습니다.',
        },
        {
          stockSymbol: 'NVDA',
          title: 'NVIDIA Corporation (NVDA)',
          content: '엔비디아는 AI 관련 수요 증가로 인해 주목받고 있습니다. Tigress Financial이 목표가를 350달러로 상향 조정했습니다.',
        },
      ],
    },
    sentChannels: ['email'],
    viewCount: 18,
  },
  {
    id: `brf_${twoDaysAgo.toISOString().split('T')[0].replace(/-/g, '')}_060000_def456`,
    generatedAt: twoDaysAgo.toISOString(),
    status: 'completed',
    stocks: [mockTrendingStocks[4]],
    imageUrl: 'https://via.placeholder.com/1200x1600/1e293b/64748b?text=Previous+Briefing',
    textContent: {
      title: '이틀 전 화제 종목 브리핑',
      summary: `${twoDaysAgo.getFullYear()}년 ${twoDaysAgo.getMonth() + 1}월 ${twoDaysAgo.getDate()}일 미국 증시 동향입니다.`,
      sections: [
        {
          stockSymbol: 'AMZN',
          title: 'Amazon.com, Inc. (AMZN)',
          content: '아마존은 전자상거래 부문의 성장세를 보이고 있습니다. 연말 쇼핑 시즌 실적이 기대 이상으로 나타났습니다.',
        },
      ],
    },
    sentChannels: ['slack'],
    viewCount: 15,
  },
];

export function getTopTrendingStock(): Stock {
  return mockTrendingStocks[0];
}

export function getTop3TrendingStocks(): Stock[] {
  return mockTrendingStocks.slice(0, 3);
}

export function getStockBySymbol(symbol: string): Stock | undefined {
  return mockTrendingStocks.find((stock) => stock.symbol === symbol);
}

export function getBriefingById(id: string): Briefing | undefined {
  return mockBriefings.find(b => b.id === id);
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatNumber(value: number): string {
  if (value >= 1e9) {
    return `${(value / 1e9).toFixed(2)}B`;
  }
  if (value >= 1e6) {
    return `${(value / 1e6).toFixed(2)}M`;
  }
  if (value >= 1e3) {
    return `${(value / 1e3).toFixed(2)}K`;
  }
  return value.toString();
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

export function getScreenerTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    most_actives: '거래량 상위',
    day_gainers: '상승률 상위',
    day_losers: '하락률 상위',
  };
  return labels[type] || type;
}

/**
 * 종목의 최근 5일간 주가 데이터를 생성합니다 (목업)
 */
export function getStockPriceHistory(symbol: string, currentPrice: number): StockPriceData[] {
  // 현재 가격을 기준으로 5일간의 가격 변동 시뮬레이션
  const basePrice = currentPrice * 0.95; // 5일 전 가격 (현재보다 5% 낮게 시작)
  const priceChange = (currentPrice - basePrice) / 4; // 일일 평균 변동
  
  const today = new Date();
  const history: StockPriceData[] = [];
  
  for (let i = 4; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    
    // 가격 변동 시뮬레이션 (약간의 랜덤성 추가)
    const randomFactor = 1 + (Math.random() - 0.5) * 0.02; // ±1% 랜덤
    const price = basePrice + priceChange * (4 - i) * randomFactor;
    
    // 거래량도 변동 시뮬레이션
    const volumeBase = 30000000; // 기본 거래량
    const volumeVariation = (Math.random() - 0.5) * 0.3; // ±15% 변동
    const volume = volumeBase * (1 + volumeVariation);
    
    history.push({
      date: date.toISOString().split('T')[0], // YYYY-MM-DD 형식
      price: Math.round(price * 100) / 100,
      volume: Math.round(volume),
    });
  }
  
  return history;
}

