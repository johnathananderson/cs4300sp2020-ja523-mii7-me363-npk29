import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ingredients import IngredientsBrowser


class FindationBrowser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_SHIM", None)
        self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver")
        self.url = "https://www.findation.com/"

    def start(self):
        self.browser.get(self.url)
        time.sleep(1)

    def close_out(self):
        self.browser.close()

    def process_matches(self, products):
        with open("ingredients.json", "a+", encoding="utf8") as i:
            try:
                ingredients = json.load(i)
            except:
                ingredients = {}
        get_started_button = self.browser.find_element_by_xpath("//*[@id='hide-splash']")
        get_started_button.click()
        time.sleep(1)
        n_products = len(products)
        results = []
        i = IngredientsBrowser()
        for p in range(n_products):
            product = products[p]
            brand = product[0]
            product_name = product[1]
            shade = product[2]
            brand_input = self.browser.find_element_by_id("brand-search")
            brand_input.send_keys(brand)
            brand_input.send_keys(Keys.ENTER)
            time.sleep(1)
            product_input = self.browser.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[3]/div[2]/div/div[2]/div[1]/input"
            )
            product_input.send_keys(product_name)
            product_input.send_keys(Keys.ENTER)
            time.sleep(1)
            shade_input = self.browser.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/input"
            )
            shade_input.send_keys(shade)
            shade_input.send_keys(Keys.ENTER)
            time.sleep(1)
            if p < n_products - 1:
                add_another_button = self.browser.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/a"
                )
                add_another_button.click()
                time.sleep(1)
            else:
                find_matches_button = self.browser.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/button"
                )
                find_matches_button.click()
                time.sleep(1)
                matches = self.browser.find_elements_by_class_name("match-meta")
                for match in matches:
                    lines = match.text.splitlines()
                    match_brand = lines[0]
                    match_name = lines[1]
                    match_shade = lines[2].replace("Your shade: ", "").replace(" (Natural)", "")
                    match_product = {}
                    match_product["brand"] = match_brand
                    match_product["name"] = match_name
                    match_product["shade"] = match_shade
                    match_product["thumbnail"] = match.find_element_by_class_name("micro").get_attribute("src")
                    match_product["url"] = match.find_element_by_class_name("media").get_attribute("href")

                    brand_product = match_brand + " " + match_name

                    if match_brand in ingredients and match_name in ingredients[match_brand]:
                        if ingredients[match_brand][match_name] == "Ingredients not found":
                            match_product["ingredients"] = "Ingredients not found"
                        else:
                            match_product["ingredients"] = ingredients[brand_product]
                    else:
                        found_ingredients = i.find_ingredients(
                            match_brand.replace(" ", "+"), match_name.replace(" ", "+")
                        )
                        ingredients[match_brand] = ingredients.get(match_brand, {})
                        ingredients[match_brand][match_name] = found_ingredients
                        match_product["ingredients"] = found_ingredients

                    results.append(match_product)
        i.close_out()
        with open("ingredients.json", "w") as outfile:
            json.dump(ingredients, outfile, indent=4)
        return results


f = FindationBrowser()
f.start()
with open("products.json", encoding="utf8") as j:
    data = json.load(j)
brand1 = "Mary Kay"
product1 = "Full-Coverage Foundation"
shade1 = "Bronze 507"

brand2 = "Mary Kay"
product2 = "Medium-Coverage Foundation "
shade2 = "Bronze 507 (Natural)"

products = [[brand1, product1, shade1], [brand2, product2, shade2]]
results = f.process_matches(products)
f.close_out()

print("DONE")


with open("findation_output.txt", "w") as outfile:
    outfile.writelines("%s\n" % product for product in results)
