import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default defineConfig({
  build: {
    target: "modules",
  },
  plugins: [
    svelte({
      compilerOptions: {
        dev: process.env.NODE_ENV === "development",
      },
    }),
  ],
});
