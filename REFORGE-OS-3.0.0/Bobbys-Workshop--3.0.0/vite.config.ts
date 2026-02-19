import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react-swc";
import { defineConfig, PluginOption } from "vite";

import sparkPlugin from "@github/spark/spark-vite-plugin";
import createIconImportProxy from "@github/spark/vitePhosphorIconProxyPlugin";
import { resolve } from 'path'

const projectRoot = process.env.PROJECT_ROOT || import.meta.dirname

// https://vite.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'radix-ui': [
            '@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-tabs', '@radix-ui/react-popover', '@radix-ui/react-tooltip',
          ],
          'charts': ['recharts', 'd3'],
          'sonner': ['sonner'],
        },
      },
    },
  },
  plugins: [
    react(),
    tailwindcss(),
    // DO NOT REMOVE
    createIconImportProxy() as PluginOption,
    sparkPlugin() as PluginOption,
  ],
  server: {
    port: 5000,
    strictPort: false,  // Allow port fallback if 5000 is busy
  },
  resolve: {
    alias: {
      '@': resolve(projectRoot, 'src')
    }
  },
});
