import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  root: resolve(__dirname, "src/frontend"),
  build: {
    outDir: resolve(__dirname, "dist/frontend"),
    emptyOutDir: true,
  },
});
