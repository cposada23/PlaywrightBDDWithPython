"""
Login Page Object Model for Playwright BDD Framework.

This module contains the LoginPage class with all locators and methods
needed to interact with the login page elements.
"""

import allure
from playwright.sync_api import Page
from tests.pages.base_page import BasePage

class BlankfactorPage(BasePage):
    """Page Object Model for the blankfactor page."""
    
    def __init__(self, page: Page):
        """Initialize the blankfactor page with the Playwright page instance."""
        super().__init__(page)
        self.page = page

        # Define locators for blankfactor page elements
        self.industries_select = page.locator("//header//a/span[normalize-space(text()) = 'Industries']")
        self.lets_get_started_button = page.locator('//a[normalize-space(text()) = "Let\'s get started"]')
    
    def navigate_to_blankfactor(self, base_url: str):
        """Navigate to the blankfactor page."""
        with allure.step(f"Navigate to {base_url}"):
            try:
                self.page.goto(base_url)
                self.wait_for_page_load()
            except Exception as e:
                raise Exception(f"Failed to navigate to {base_url}: {str(e)}")

    def hover_over_induestries_select(self):
        """Hover over the industries select."""
        with allure.step("Hover over the industries select"):
            try:
                self.industries_select.hover()
            except Exception as e:
                raise Exception(f"Failed to hover over the industries select: {str(e)}")

    def open_item_in_select(self, item: str):
        """Open an item in the select."""
        with allure.step(f"Open the {item} item in the select"):
            try:
                item = self.page.locator(f"//*[contains(@class, 'item__title') and text() = '{item}']")
                item.wait_for(state="visible")
                item.click()
            except Exception as e:
                raise Exception(f"Failed to open the {item} item in the select: {str(e)}")

    def copy_text_from_tile(self, tile_index: int) -> str:
        """Copy the text from the tile."""
        with allure.step(f"Copy the text from the {tile_index} tile"):
            try:
                tile = self.page.locator(f"(//*[contains(@class, 'flip-card-front')])[{tile_index}]")
                tile.wait_for(state="visible")
                tile.scroll_into_view_if_needed()
                tile.hover()

                tile_back = self.page.locator(f"(//*[contains(@class, 'card-back')])[{tile_index}]/div")
                tile_back.wait_for(state="visible")

                tile_text = tile_back.text_content()
                return tile_text.strip()
            except Exception as e:
                raise Exception(f"Failed to copy the text from the {tile_index} tile: {str(e)}")

    def click_on_the_lets_get_started_button(self):
        """Click on the Let's get started button."""
        with allure.step("Click on the Let's get started button"):
            try:
                self.lets_get_started_button.wait_for(state="visible")
                self.lets_get_started_button.click()
            except Exception as e:
                raise Exception(f"Failed to click on the Let's get started button: {str(e)}")