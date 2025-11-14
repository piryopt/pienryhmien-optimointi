import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: "assets/main.js"
      }
    }
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./testSetup.js"
  }
});
