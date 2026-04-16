import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3003,
    open: false,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      },
      '/dify-api': {
        target: 'https://whhongyi.com.cn',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/dify-api/, '/v1'),
        secure: false,
        timeout: 180000
      },
      '/whhongyi-api': {
        target: 'https://whhongyi.com.cn',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/whhongyi-api/, ''),
        secure: false,
        timeout: 120000,
        headers: {
          'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
          'Referer': 'https://whhongyi.com.cn/',
          'Origin': 'https://whhongyi.com.cn'
        }
      }
    }
  }
})
