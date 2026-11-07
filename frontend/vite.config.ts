import { defineConfig } from "vite";

export default defineConfig({
  // Relative base so the build works on GitHub Pages under /<repo>/.
  base: "./",
  server: { proxy: { "/api": "http://localhost:8000" } },
});
