// The browser tests. `npm test` builds the site, serves it, and opens it at a
// phone size and a laptop size. Screenshots land in test-results/ (not committed).
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  retries: 0,
  reporter: [["list"]],
  use: {
    baseURL: "http://localhost:4321",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "npm run build && npx astro preview --port 4321 --ignore-lock",
    url: "http://localhost:4321",
    reuseExistingServer: false,
    timeout: 120_000,
  },
  projects: [
    { name: "phone", use: { ...devices["Pixel 7"] } },
    { name: "laptop", use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 800 } } },
  ],
});
