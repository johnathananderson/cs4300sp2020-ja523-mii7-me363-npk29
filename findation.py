import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Browser:
    def __init__(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.url = "https://www.findation.com/"

    def start(self):
        self.browser.get(self.url)
        time.sleep(1)

    def close_out(self):
        self.browser.close()

    def process_matches(self, products):
        get_started_button = self.browser.find_element_by_xpath("//*[@id='hide-splash']")
        get_started_button.click()
        n_products = len(products)
        results = []
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
                    match_shade = lines[2].replace("Your shade: ", "")
                    match_thumbnail = match.find_element_by_class_name("micro").get_attribute("src")
                    match_url = match.find_element_by_class_name("media").get_attribute("href")
                    match_product = {}
                    match_product["brand"] = match_brand
                    match_product["name"] = match_name
                    match_product["shade"] = match_shade
                    match_product["thumbnail"] = match_thumbnail
                    match_product["url"] = match_url
                    results.append(match_product)
        return results


b = Browser()
b.start()
with open("./products.json", encoding="utf8") as j:
    data = json.load(j)
brand1 = "Mary Kay"
product1 = "Full-Coverage Foundation"
shade1 = "Bronze 507"

brand2 = "Mary Kay"
product2 = "Medium-Coverage Foundation "
shade2 = "Bronze 507 (Natural)"

products = [[brand1, product1, shade1], [brand2, product2, shade2]]
results = b.process_matches(products)
b.close_out()

print("DONE")

with open("findation_output.txt", "w") as outfile:
    outfile.writelines("%s\n" % product for product in results)
