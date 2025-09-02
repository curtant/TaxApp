import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // Percorso base per i file statici, deve corrispondere a STATIC_URL
  base: '/static/',
  server: {
    // Assicura che Vite accetti connessioni dalla rete
    host: '0.0.0.0',
    port: 5173,
  },
  build: {
    // Dove Vite salverà i file compilati
    outDir: './dist',
    // Genera un file manifest.json che django-vite userà
    manifest: true,
    rollupOptions: {
      // Sovrascrive il punto di ingresso di default di Vite
      input: './src/main.js',
    },
  },
})

