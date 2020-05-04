import json

# import urllib
import os

import time
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from ingredients import IngredientsBrowser
from webdriver_manager.chrome import ChromeDriverManager


class FindationBrowser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-proxy-server")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--start-maximized")
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_SHIM", None)
        # self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        self.browser.get("https://www.findation.com/")

    def close_out(self):
        self.browser.close()

    def process_matches(self, products, outputs):
        try:
            get_started_button = WebDriverWait(self.browser, 20, 0.1).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='hide-splash']"))
            )
            get_started_button.click()
            n_products = len(products)
            results = []
            for p in range(n_products):
                print(p)
                product = products[p]
                brand = product[0]
                product_name = product[1]
                shade = product[2]
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                WebDriverWait(self.browser, 20, 0.1).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div[2]"))
                )
                brand_input = WebDriverWait(self.browser, 20, 0.1).until(
                    EC.element_to_be_clickable((By.ID, "brand-search"))
                )
                brand_input.send_keys("  " + brand.strip())
                time.sleep(0.1)
                brand_input.send_keys(Keys.ENTER)
                product_input = WebDriverWait(self.browser, 20, 2).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[2]/div/div/div[3]/div[2]/div/div[2]/div[1]/input")
                    )
                )
                product_input.send_keys(" " + product_name.strip())
                time.sleep(0.1)
                product_input.send_keys(Keys.ENTER)
                WebDriverWait(self.browser, 20, 2).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/input")
                    )
                )
                time.sleep(0.1)
                shade_input = self.browser.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/input"
                )
                shade_input.send_keys(shade)
                time.sleep(0.1)
                shade_input.send_keys(Keys.ENTER)
                time.sleep(0.1)
                if p < n_products - 1:
                    WebDriverWait(self.browser, 20, 0.1).until(
                        EC.invisibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div[2]"))
                    )
                    WebDriverWait(self.browser, 20, 0.1).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/a")
                        )
                    )
                    add_another_button = WebDriverWait(self.browser, 20, 0.1).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/a")
                        )
                    )
                    add_another_button.click()
                else:
                    WebDriverWait(self.browser, 20, 2).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "actions"))
                    )
                    find_matches_button = (
                        WebDriverWait(self.browser, 20, 0.1)
                        .until(EC.element_to_be_clickable((By.CLASS_NAME, "actions")))
                        .find_element_by_class_name("btn-default")
                    )
                    find_matches_button.click()
                    WebDriverWait(self.browser, 20, 0.1).until(EC.url_contains("searches"))
                    WebDriverWait(self.browser, 20, 0.1).until(
                        EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[4]/div[3]/div"))
                    )
                    matches = self.browser.find_elements_by_class_name("match-meta")
                    print("Found " + str(len(matches)) + " matches")
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
                        # match_product["url"] = match.find_element_by_class_name("media").get_attribute("href")

                        if match_brand in outputs and match_name in outputs[match_brand]:
                            m = outputs[match_brand][match_name]
                            match_product["ingredients"] = m["ingredients"]
                            match_product["prices"] = m["prices"]
                            match_product["health_score"] = m["health_score"]
                            match_product["sentiment"] = m["sentiment"]
                        # else:
                        #     match_product["ingredients"] = "Ingredients not found"
                        #     match_product["prices"] = []
                        #     match_product["health_score"] = "N/A"
                        results.append(match_product)
            return results
        except Exception as e:
            print("Failed: " + products[0][0] + " " + products[0][1])
            print(e)


# f = FindationBrowser()
# brand = "Prescriptives"
# product_name = "Flawless Skin Total Protection Makeup"
# shade = "29 Tawny"
# product = [[brand, product_name, shade], [brand, product_name, shade]]
# f.process_matches(product)
# f.close_out()
# print("DONE")
