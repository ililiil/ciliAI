import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3003,
    open: false,
    proxy: {
      // RuoYi 后端 API
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      },
      // 火山引擎 AI API
      '/dify-api': {
        target: 'https://ark.cn-beijing.volces.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/dify-api/, '/api/v3'),
        secure: false,
        timeout: 180000
      },
      // 火山引擎服务
      '/whhongyi-api': {
        target: 'https://ark.cn-beijing.volces.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/whhongyi-api/, ''),
        secure: false,
        timeout: 180000,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }
    }
  }
})
