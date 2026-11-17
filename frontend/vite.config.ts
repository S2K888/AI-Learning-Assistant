import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  // 路径别名：@ 指向 src 目录
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },

  // 配置开发服务器代理
  server: {
    proxy: {
      '/chat': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})