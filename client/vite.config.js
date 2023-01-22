import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';


export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // import bootstrap
      '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
    }
  },
  server: {
    open: true,
    // proxy to run app locally, forwarding to local api instance
    proxy: {
      '^/api/v1': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace("/api/v1", ""),
      },
    }
  }
})
