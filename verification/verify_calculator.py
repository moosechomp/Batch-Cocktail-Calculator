from playwright.sync_api import sync_playwright, expect

def verify_calculator():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local server
        page.goto("http://localhost:8000/index.html")

        # Wait for the page to load
        expect(page).to_have_title("Batch Boss - Cocktail Batching Calculator")

        # Select a cocktail (e.g., Negroni)
        page.select_option("#cocktail-selector", "negroni")

        # Verify ingredients are populated
        # Negroni has 3 ingredients
        # We wait for the rows to appear
        page.wait_for_selector(".ingredient-row")

        # Check if "Gin" is present in one of the inputs
        # The inputs don't have unique IDs per row, so we check values
        inputs = page.locator("input[placeholder='Ingredient Name']")
        expect(inputs.first).to_have_value("Gin (94 proof)")

        # Enter number of drinks
        page.fill("#drink-quantity", "10")

        # Click Calculate
        page.click("#calculate-batch")

        # Verify results section appears
        results_section = page.locator("#results-section")
        expect(results_section).to_be_visible()

        # Take a screenshot of the entire page
        page.screenshot(path="verification/calculator_verification.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    verify_calculator()
