import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig(async ({ mode }) => {
  const isProduction = mode === "production";
  const isDevelopment = mode === "development";

  return {
    plugins: [react()],
    css: {
      postcss: "./postcss.config.js",
    },

    // Path resolution
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
        "@core": path.resolve(__dirname, "./src/core"),
        "@services": path.resolve(__dirname, "./src/services"),
        "@components": path.resolve(__dirname, "./src/components"),
        "@pages": path.resolve(__dirname, "./src/pages"),
        "@hooks": path.resolve(__dirname, "./src/hooks"),
        "@utils": path.resolve(__dirname, "./src/utils"),
        "@types": path.resolve(__dirname, "./src/types"),
        "@config": path.resolve(__dirname, "./src/config"),
        "@lib": path.resolve(__dirname, "./src/lib"),
        "@styles": path.resolve(__dirname, "./src/styles"),
        "@assets": path.resolve(__dirname, "../assets"),
      },
    },

    // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
    // prevent vite from obscuring rust errors
    clearScreen: false,
    // tauri expects a fixed port, fail if that port is not available
    server: {
      port: 1420,
      strictPort: true,
      hmr: {
        protocol: "ws",
        host: "localhost",
        port: 1420,
      },
    },
    // to make use of `TAURI_DEBUG` and other env variables
    // https://tauri.studio/v1/api/config#buildconfig.beforedevcommand
    envPrefix: ["VITE_", "TAURI_"],
    build: {
      // Tauri supports es2021
      target: process.env.TAURI_PLATFORM == "windows" ? "chrome105" : "safari15",
      // Enterprise production optimizations
      minify: isProduction ? "esbuild" : false,
      sourcemap: isDevelopment || !!process.env.TAURI_DEBUG,
      // Production optimizations
      cssCodeSplit: true,
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        external: [
          "@tauri-apps/api/core",
          "@tauri-apps/api/tauri",
          "@tauri-apps/api/window",
          "@tauri-apps/api/fs",
          "@tauri-apps/api/path",
          "@tauri-apps/api/shell",
          "@tauri-apps/api/dialog",
          "@tauri-apps/api/notification",
          "@tauri-apps/api/clipboard",
          "@tauri-apps/api/http",
          "@tauri-apps/api/event",
          "@tauri-apps/api/globalShortcut",
          "@tauri-apps/api/app",
          "@tauri-apps/api/os",
          "@tauri-apps/api/process",
        ],
        output: {
          // Code splitting for better caching
          manualChunks: isProduction
            ? {
                vendor: ["react", "react-dom"],
                router: [], // Add router if used
              }
            : undefined,
          // Asset naming
          assetFileNames: isProduction
            ? "assets/[name]-[hash][extname]"
            : "assets/[name][extname]",
          chunkFileNames: isProduction
            ? "assets/[name]-[hash].js"
            : "assets/[name].js",
          entryFileNames: isProduction
            ? "assets/[name]-[hash].js"
            : "assets/[name].js",
        },
      },
      // Build optimizations
      reportCompressedSize: true,
      emptyOutDir: true,
      // Tree shaking
      treeshake: {
        moduleSideEffects: false,
      },
    },
    // Optimize dependencies
    optimizeDeps: {
      include: ["react", "react-dom"],
      exclude: ["@tauri-apps/api"],
    },
  };
});