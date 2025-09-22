import pytest
import allure
from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page, expect

from tests.pages.blankfactor_page import BlankfactorPage

scenarios('../features/blankfactor.feature')

@pytest.fixture
def blankfactor_page(page: Page) -> BlankfactorPage:
    """Create a BlankfactorPage instance for the test."""
    return BlankfactorPage(page)

@given("I navigate to Blankfactor home page")
def i_navigate_to_blankfactor_home_page(blankfactor_page: BlankfactorPage, base_url: str):
    """Navigate to the blankfactor home page."""
    blankfactor_page.navigate_to_blankfactor(base_url)

@when(parsers.parse('I hover over "{select}" and open the "{section}" section'))
def i_hover_over_select_and_open_section(blankfactor_page: BlankfactorPage, select: str, section: str):
  
    """Hover over the select and open the section"""
    with allure.step(f"Hover over the {select} and open the {section} section"):
        try:
            match select:
                case "Industries":
                    blankfactor_page.hover_over_induestries_select()
                case _:
                    raise Exception(f"Invalid select: {select}")
            blankfactor_page.open_item_in_select(section)
            # assert login_page.is_on_login_page(), f"Failed to reach login page. Current URL: {login_page.page.url}"
        except Exception as e:
            raise AssertionError(f"Failed to hover over the {select} and open the {section} section: {str(e)}") 

@when("I copy the text from the 3dht tile")
def i_copy_the_text_from_the_3dht_tile(blankfactor_page: BlankfactorPage):
    """Copy the text from the 3dht tile"""
    with allure.step("Copy the text from the 3dht tile"):
        try:
            tile_text = blankfactor_page.copy_text_from_tile(3)
            print(f"Tile text: {tile_text}")
            expected_text = "Automate your operations and get to market quickly and securely. Leverage predictive data analytics using machine learning to build reliable, yet forward-thinking financial solutions."
            assert tile_text == expected_text, f"The tile text does not match the expected text: {tile_text} != {expected_text}"
        except Exception as e:
            raise AssertionError(f"Failed to copy the text from the 3dht tile: {str(e)}")