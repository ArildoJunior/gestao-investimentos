// FILE: frontend/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
// Importar os plugins PostCSS diretamente
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  // Configuração explícita do PostCSS
  css: {
    postcss: {
      plugins: [
        tailwindcss(), // Chamar como função
        autoprefixer(), // Chamar como função
      ],
    },
  },
});