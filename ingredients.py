import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


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

    def find_ingredients(self, brand, product):
        base_url = "https://www.ewg.org/skindeep/search/?utf8=%E2%9C%93&search="
        self.browser.get(base_url + brand + "+" + product)
        time.sleep(10)
        found = False
        while not found:
            try:
                search_header = self.browser.find_element_by_class_name("browse-search-header")
                found = True
            except:
                time.sleep(10)
                print(1)
        if search_header.text[0] == "0":
            base_url = "https://www.beautypedia.com/?s="
            self.browser.get(base_url + brand + "+" + product)
            time.sleep(10)
            found = False
            while not found:
                try:
                    search_header = self.browser.find_element_by_class_name("search-results-summary")
                    found = True
                except:
                    time.sleep(10)
            if search_header.text[0] == "0":
                return "Ingredients not found"
            else:
                review_results = self.browser.find_element_by_class_name("review-results")
                self.browser.get(review_results.find_element_by_class_name("review-product").get_attribute("href"))
                time.sleep(10)
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
            time.sleep(10)
            ingredients = self.browser.find_elements_by_class_name("td-ingredient-interior")
            return list(map(lambda x: x.text.split("\n")[0].title(), ingredients))
