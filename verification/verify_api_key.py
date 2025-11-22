from playwright.sync_api import sync_playwright, expect

def verify_api_key_logic():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the local server
        page.goto("http://localhost:8000/index.html")

        # 1. Initial State: API Key input should be visible
        page.click("#suggest-recipe-btn")
        expect(page.locator("#api-key-input-container")).to_be_visible()
        expect(page.locator("#api-key-status")).not_to_be_visible()

        # 2. Enter API Key
        page.fill("#gemini-api-key", "TEST_API_KEY_12345")

        # Close modal (cancel)
        page.click("#gemini-cancel")

        # 3. Simulate Saving Key (Since we can't easily mock the API call success in this script without interception,
        # we will manually trigger the storage logic or rely on the 'Change' logic if we had successfully submitted.
        # However, the logic I implemented updates the UI immediately if localStorage has the key on open.
        # Let's manually set localStorage to simulate a previous successful save.)

        page.evaluate("localStorage.setItem('batchBossApiKey', 'TEST_API_KEY_12345')")

        # 4. Re-open Modal
        page.click("#suggest-recipe-btn")

        # 5. Verify Key is Hidden
        expect(page.locator("#api-key-input-container")).not_to_be_visible()
        expect(page.locator("#api-key-status")).to_be_visible()

        # Take screenshot of hidden state
        page.screenshot(path="verification/api_key_hidden.png")

        # 6. Click Change Key
        page.click("#change-api-key-btn")

        # 7. Verify Input Revealed
        expect(page.locator("#api-key-input-container")).to_be_visible()
        expect(page.locator("#api-key-status")).not_to_be_visible()
        expect(page.locator("#gemini-api-key")).to_have_value("TEST_API_KEY_12345")

        # Take screenshot of revealed state
        page.screenshot(path="verification/api_key_revealed.png")

        browser.close()

if __name__ == "__main__":
    verify_api_key_logic()
