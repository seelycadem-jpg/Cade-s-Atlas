// Meanwhile Atlas: the site build. Every page is a static file built in advance,
// so each loads on its own and Google can read it (docs/architecture.md).
import { defineConfig } from "astro/config";

export default defineConfig({
  output: "static",
  // The public address goes here once the domain exists (Phase 10); canonical
  // addresses and the sitemap need it.
  // site: "https://example.org",
});
