import { test, expect } from "@playwright/test";

// The first test: the home page opens, carries its title and description, and
// fits the screen with no sideways scroll. One screenshot per device.
test("home page opens", async ({ page }, testInfo) => {
  const response = await page.goto("/");
  expect(response?.status()).toBe(200);

  await expect(page).toHaveTitle("Meanwhile Atlas");
  await expect(page.locator("h1")).toHaveText("Meanwhile Atlas");
  await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /.+/);

  // No horizontal scroll on any screen (docs/architecture.md: phone first).
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
  );
  expect(overflow).toBe(false);

  await page.screenshot({
    path: testInfo.outputPath(`home-${testInfo.project.name}.png`),
    fullPage: true,
  });
});
