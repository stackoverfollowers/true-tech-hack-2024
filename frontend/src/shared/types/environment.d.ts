declare global {
  namespace NodeJS {
    interface ProcessEnv {
      VITE_APP_VERSION: string;
      VITE_BACKEND_URL: string;
    }
  }
}

export {};
