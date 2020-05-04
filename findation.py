import os

import time
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FindationBrowser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-gpu")
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

    def process_matches(self, products):
        try:
            WebDriverWait(self.browser, 20, 0.1).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='hide-splash']"))
            )
            get_started_button = self.browser.find_element_by_xpath("//*[@id='hide-splash']")
            get_started_button.click()
            results = []
            for product in products:
                brand = product[0]
                product_name = product[1]
                shade = product[2]
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(10)
                print(self.browser.find_element_by_id("brand").value_of_css_property("height"))

                WebDriverWait(self.browser, 20, 0.1).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div[2]"))
                )
                print(11)
                WebDriverWait(self.browser, 20, 0.1).until(EC.element_to_be_clickable((By.ID, "brand-search")))
                brand_input = self.browser.find_element_by_id("brand-search")
                brand_input.send_keys("  " + brand.strip())
                time.sleep(0.1)
                brand_input.send_keys(Keys.ENTER)
                WebDriverWait(self.browser, 20, 0.5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[2]/div/div/div[3]/div[2]/div/div[2]/div[1]/input")
                    )
                )
                time.sleep(0.1)
                product_input = self.browser.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[3]/div[2]/div/div[2]/div[1]/input"
                )
                product_input.send_keys(" " + product_name.strip())
                time.sleep(0.1)
                product_input.send_keys(Keys.ENTER)
                WebDriverWait(self.browser, 20, 0.5).until(
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
                print(15)
                if p < n_products - 1:
                    print(16)
                    WebDriverWait(self.browser, 20, 0.1).until(
                        EC.invisibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div[2]"))
                    )
                    print(self.browser.find_element_by_id("brand").value_of_css_property("height"))
                    WebDriverWait(self.browser, 20, 0.1).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/a")
                        )
                    )
                    WebDriverWait(self.browser, 20, 0.1).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/a")
                        )
                    )
                    add_another_button = self.browser.find_element_by_xpath(
                        "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/a"
                    )
                    add_another_button.click()
                    time.sleep(0.1)
                    print(18)
                else:
                    WebDriverWait(self.browser, 20, 2).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "actions"))
                    )
                    WebDriverWait(self.browser, 20, 0.1).until(EC.element_to_be_clickable((By.CLASS_NAME, "actions")))
                    find_matches_button = self.browser.find_element_by_class_name("actions").find_element_by_tag_name(
                        "button"
                    )
                    find_matches_button.click()
                    print(19)
                    WebDriverWait(self.browser, 20, 0.1).until(EC.url_contains("searches"))
                    WebDriverWait(self.browser, 20, 0.1).until(
                        EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[4]/div[3]/div"))
                    )
                    print("Done")
                    for match in self.browser.find_elements_by_class_name("match-meta"):
                        lines = match.text.splitlines()
                        match_product = {}
                        match_product["brand"] = lines[0]
                        match_product["name"] = lines[1]
                        match_product["shade"] = lines[2].replace("Your shade: ", "").replace(" (Natural)", "")
                        match_product["thumbnail"] = match.find_element_by_class_name("micro").get_attribute("src")
                        results.append(match_product)
            self.browser.delete_all_cookies()
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
