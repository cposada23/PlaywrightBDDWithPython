import pytest
import allure
from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page

from tests.pages.blankfactor_page import BlankfactorPage

scenarios('../features/blankfactor.feature')

@pytest.fixture
def blankfactor_page(page: Page) -> BlankfactorPage:
    """Create a BlankfactorPage instance for the test."""
    return BlankfactorPage(page)

@given("I navigate to Blankfactor home page")
def i_navigate_to_blankfactor_home_page(blankfactor_page: BlankfactorPage, base_url: str):
    """Navigate to the blankfactor home page."""
    with allure.step(f"Navigate to Blankfactor home page: {base_url}"):
        try:
            blankfactor_page.navigate_to_blankfactor(base_url)
        except Exception as e:
            raise AssertionError(f"Failed to navigate to Blankfactor home page: {str(e)}")

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

@when("I scroll to the bottom of the page and click on the Let's get started button")
def i_scroll_to_the_bottom_of_the_page_and_click_on_the_lets_get_started_button(blankfactor_page: BlankfactorPage):
    """Scroll to the bottom of the page and click on the Let's get started button"""
    with allure.step("Scroll to the bottom of the page and click on the Let's get started button"):
        try:
            blankfactor_page.scroll_to_the_bottom_of_the_page()
            blankfactor_page.click_on_the_lets_get_started_button()
        except Exception as e:
            raise AssertionError(f"Failed to scroll to the bottom of the page and click on the Let's get started button: {str(e)}")

@then(parsers.parse('I verify that the page is loaded and the page url is "{url}"'))
def i_verify_that_the_page_is_loaded_and_the_page_url_is(blankfactor_page: BlankfactorPage, url: str):
    """Verify that the page is loaded and the page url is {url}"""
    with allure.step(f"Verify that the page is loaded and the page url is {url}"):
        try:
            assert blankfactor_page.get_current_url() == url, f"The page url does not match the expected url: {blankfactor_page.get_current_url()} != {url}"
        except Exception as e:
            raise AssertionError(f"Failed to verify that the page is loaded and the page url is {url}: {str(e)}")

@then(parsers.parse('I verify the page title is "{title}"'))
def i_verify_the_page_title_is(blankfactor_page: BlankfactorPage, title: str):
    """Verify the page title is {title}"""
    with allure.step(f"Verify the page title is {title}"):
        try:
            assert blankfactor_page.get_page_title() == title, f"The page title does not match the expected title: {blankfactor_page.get_page_title()} != {title}"
        except Exception as e:
            raise AssertionError(f"Failed to verify the page title is {title}: {str(e)}")