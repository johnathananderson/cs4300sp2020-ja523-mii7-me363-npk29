import json
import urllib
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ingredients import IngredientsBrowser
from webdriver_manager.chrome import ChromeDriverManager


class FindationBrowser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false"); 
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_SHIM", None)
        self.browser = webdriver.Chrome(options=chrome_options, executable_path="chromedriver")
        self.browser.implicitly_wait(2)
        self.browser.get("https://www.findation.com/")

    def close_out(self):
        self.browser.close()

    def process_matches(self, products):
        # i = IngredientsBrowser()
        with open("ingredients.json", encoding="utf8") as data:
            try:
                ingredients = json.load(data)
            except:
                print("Couldn't open ingredients")
                ingredients = {}
        with open("prices.json", encoding="utf8") as p:
            try:
                prices = json.load(p)
            except:
                print("Couldn't open prices")
                prices = {}
        with open("matches.json", encoding="utf8") as m:
            try:
                matches_json = json.load(m)
            except:
                print("Couldn't open matches")
                matches_json = {}
        try:
            count = 0
            time.sleep(1)
            while count < 11:
                found = False
                count = 0
                while not found and count < 11:
                    try:
                        get_started_button = self.browser.find_element_by_xpath("//*[@id='hide-splash']")
                        get_started_button.click()
                        found = True
                    except:
                        time.sleep(0.1)
                        count += 0.1
                n_products = len(products)
                results = []
                for p in range(n_products):
                    product = products[p]
                    brand = product[0]
                    product_name = product[1]
                    shade = product[2]
                    found = False
                    count = 0
                    while not found and count < 11:
                        try:
                            brand_input = self.browser.find_element_by_id("brand-search")
                            found = True
                        except:
                            time.sleep(0.1)
                            count += 0.1
                    brand_input.send_keys(brand)
                    brand_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    found = False
                    count = 0
                    while not found and count < 11:
                        try:
                            product_input = self.browser.find_element_by_xpath(
                                "/html/body/div[2]/div/div/div[3]/div[2]/div/div[2]/div[1]/input"
                            )
                            found = True
                        except:
                            time.sleep(0.1)
                            count += 0.1
                    product_input.send_keys(product_name)
                    product_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    found = False
                    count = 0
                    while not found and count < 11:
                        try:
                            shade_input = self.browser.find_element_by_xpath(
                                "/html/body/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/input"
                            )
                            found = True
                        except:
                            time.sleep(0.1)
                            count += 0.1
                    shade_input.send_keys(shade)
                    shade_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    if p < n_products - 1:
                        found = False
                        count = 0
                        while not found and count < 11:
                            try:
                                add_another_button = self.browser.find_element_by_xpath(
                                    "/html/body/div[2]/div/div/div[3]/div[1]/form/div/div/div/a"
                                )
                                add_another_button.click()
                                found = True
                            except:
                                time.sleep(0.1)
                                count += 0.1
                        time.sleep(2)
                    else:
                        found = False
                        count = 0
                        while not found and count < 11:
                            try:
                                find_matches_button = self.browser.find_element_by_class_name(
                                    "actions"
                                ).find_element_by_tag_name("button")
                                find_matches_button.click()
                                found = True
                            except:
                                time.sleep(0.1)
                                count += 0.1
                        time.sleep(2)
                        found = False
                        count = 0
                        while not found and count < 11:
                            try:
                                matches = self.browser.find_elements_by_class_name("match-meta")
                                found = True
                            except:
                                time.sleep(0.1)
                                count += 0.1
                        print("Found " + str(len(matches)) + " matches")
                        for match in matches:
                            lines = match.text.splitlines()
                            match_brand = lines[0]
                            match_name = lines[1]
                            match_shade = lines[2].replace("Your shade: ", "").replace(" (Natural)", "")
                            if match_brand in matches_json and match_name in matches_json[match_brand] and match_shade in matches_json[match_brand][match_name]:
                                results.append(matches_json[match_brand][match_name][match_shade])
                            else:
                                match_product = {}
                                match_product["brand"] = match_brand
                                match_product["name"] = match_name
                                match_product["shade"] = match_shade
                                match_product["thumbnail"] = match.find_element_by_class_name("micro").get_attribute("src")
                                match_product["url"] = match.find_element_by_class_name("media").get_attribute("href")

                                if match_brand in prices and match_name in prices[match_brand]:
                                    match_product["prices"] = prices[match_brand][match_name]
                                else:
                                    prices[match_brand] = prices.get(match_brand, {})
                                    prices[match_brand][match_name] = "Prices not found"
                                    match_product["prices"] = "Prices not found"
                                
                                if match_brand in ingredients and match_name in ingredients[match_brand]:
                                    match_product["ingredients"] = ingredients[match_brand][match_name]
                                else:
                                    # print("Not found in ingredients.json: " + match_brand + " " + match_name)
                                    # try:
                                    #     found_ingredients = i.find_ingredients(
                                    #         urllib.parse.quote(match_brand), urllib.parse.quote(match_name)
                                    #     )
                                    #     ingredients[match_brand] = ingredients.get(match_brand, {})
                                    #     ingredients[match_brand][match_name] = found_ingredients
                                    #     # match_product["ingredients"] = "Ingredients not found"
                                    # except Exception as e:
                                    ingredients[match_brand] = ingredients.get(match_brand, {})
                                    ingredients[match_brand][match_name] = "Ingredients not found"
                                    match_product["ingredients"] = "Ingredients not found"
                                        # print(e)
                                results.append(match_product)
                                matches_json[match_brand] = matches_json.get(match_brand, {})
                                matches_json[match_brand][match_name] = matches_json[match_brand].get(match_name, {})
                                matches_json[match_brand][match_name][match_shade] = match_product
                with open("ingredients.json", "w") as outfile:
                    json.dump(ingredients, outfile, indent=4)
                with open("prices.json", "w") as outfile:
                    json.dump(prices, outfile, indent=4)
                with open("matches.json", "w") as outfile:
                    json.dump(matches_json, outfile, indent=4)
                return results
        except Exception as e:
            print("Failed: " + products[0][0] + " " + products[0][1])
            print(e)


# f = FindationBrowser()
# with open("products.json", encoding="utf8") as j:
#     products = json.load(j)

# with open("major-brands.json", encoding="utf8") as j:
#     major_brands = json.load(j)

# i = IngredientsBrowser()
# for brand in products:
#     if brand in major_brands:
#         for product_name in products[brand]["products"]:
#             c = 0
#             for shade in products[brand]["products"][product_name]["shades"]:
#                 product = [[brand, product_name, shade], [brand, product_name, shade]]
#                 print(product[0])
#                 f.process_matches(product, i)
# i.close_out()
# f.close_out()

# print("DONE")
