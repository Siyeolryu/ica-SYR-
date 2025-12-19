/// <reference types="react" />
/// <reference types="react-dom" />

declare namespace NodeJS {
  interface ProcessEnv {
    readonly NODE_ENV: 'development' | 'production' | 'test';
  }
}

declare var process: {
  env: NodeJS.ProcessEnv;
};

// React JSX 타입 정의 (타입 정의를 찾지 못할 때를 대비)
declare namespace React {
  namespace JSX {
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
}

// Next.js 모듈 타입 선언 (타입 정의를 찾지 못할 때를 대비)
declare module 'next/app' {
  import { ComponentType } from 'react';
  export interface AppProps {
    Component: ComponentType<any>;
    pageProps: any;
  }
}

declare module 'next/head' {
  import { ComponentType } from 'react';
  const Head: ComponentType<{ children?: React.ReactNode; [key: string]: any }>;
  export default Head;
}

declare module 'react' {
  export interface ReactNode {}
  export function useState<T>(initialState: T | (() => T)): [T, (value: T | ((prev: T) => T)) => void];
  export function useEffect(effect: () => void | (() => void), deps?: any[]): void;
}

declare module 'next/router' {
  export function useRouter(): {
    pathname: string;
    push: (url: string) => void;
    [key: string]: any;
  };
}

