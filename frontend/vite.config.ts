import { UserConfigExport, defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react-swc';
import path from 'path';
import pkg from './package.json';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };

  const config: UserConfigExport = {
    plugins: [react()],
    define: {
      APP_VERSION: JSON.stringify(pkg.version),
    },
    build: {
      cssMinify: true,
    },
    resolve: {
      alias: {
        buffer: 'buffer',
        '@lib': path.resolve('src', 'shared', 'lib'),
        '@ui': path.resolve('src', 'shared', 'ui'),
        '@assets': path.resolve('src', 'shared', 'assets'),
        '@entities': path.resolve('src', 'entities'),
        '@features': path.resolve('src', 'features'),
        '@widgets': path.resolve('src', 'widgets'),
        '@guards': path.resolve('src', 'guards'),
        '@shared': path.resolve('src', 'shared'),
        '@pages': path.resolve('src', 'pages'),
        '@app': path.resolve('src', 'app'),
      },
    },
    server: {
      port: 3000,
      cors: {
        origin: process.env.VITE_BACKEND_URL,
        methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
        preflightContinue: false,
        optionsSuccessStatus: 204,
      },
      proxy: {
        '/api': {
          target: process.env.VITE_BACKEND_URL,
          secure: false,
          changeOrigin: true,
          configure: (proxy) => {
            proxy.on('proxyReq', (proxyReq) => {
              proxyReq.setHeader('origin', process.env.VITE_BACKEND_URL as string);
            });
          },
        },
      },
    },
  };

  return config;
});
