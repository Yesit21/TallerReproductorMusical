/// <reference types="vitest" />

import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true, // ⬅️ Habilita test, expect, describe, etc.
    environment: "jsdom", // ⬅️ Necesario para React + DOM
    setupFiles: "./vitest.setup.ts" // ⬅️ Opcional, para jest-dom
  },
});
