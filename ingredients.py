import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class IngredientsBrowser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_SHIM", None)
        self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver")

    def close_out(self):
        self.browser.close()

    def wait_for_page_load(self):
        try:
            element_present = EC.presence_of_element_located((By.ID, "main"))
            WebDriverWait(self.browser, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

    def find_ingredients(self, brand, product):
        base_url = "https://www.ewg.org/skindeep/search/?utf8=%E2%9C%93&search="
        self.browser.get(base_url + brand + "+" + product)
        self.wait_for_page_load()
        found = False
        while not found:
            try:
                search_header = self.browser.find_element_by_class_name("browse-search-header")
                found = True
            except:
                self.wait_for_page_load()
        if search_header.text[0] == "0":
            base_url = "https://www.beautypedia.com/?s="
            self.browser.get(base_url + brand + "+" + product)
            self.wait_for_page_load()
            found = False
            while not found:
                try:
                    search_header = self.browser.find_element_by_class_name("search-results-summary")
                    found = True
                except:
                    self.wait_for_page_load()
            if search_header.text[0] == "0":
                return "Ingredients not found"
            else:
                review_results = self.browser.find_element_by_class_name("review-results")
                self.browser.get(review_results.find_element_by_class_name("review-product").get_attribute("href"))
                self.wait_for_page_load()
                try:
                    i = self.browser.find_element_by_xpath("//*[@id='ingredients']")
                    ingredients = (
                        i.get_attribute("innerHTML")
                        .replace("Active: ", "")
                        .replace("Other: ", "")
                        .replace("May Contain: ", "")
                        .replace("May contain: ", "")
                        .strip()
                        .split(",  ")
                    )
                    return ingredients
                except:
                    return "Ingredients not found"
        else:
            listings = self.browser.find_element_by_class_name("product-listings")
            self.browser.get(listings.find_element_by_tag_name("a").get_attribute("href"))
            self.wait_for_page_load()
            ingredients = self.browser.find_elements_by_class_name("td-ingredient-interior")
            return list(map(lambda x: x.text.split("\n")[0].title(), ingredients))
