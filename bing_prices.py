from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import random

options = Options()
options.headless = True
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)

def write_json(data, filename='product_prices.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)
        
with open("./ingredients.json", encoding = 'utf-8') as j:
    data = json.load(j)
    
base_url = "https://www.bing.com/search?q="
retail_price_map = {}
for brand in data:
    retail_price_map[brand] = {}
    for product in data[brand]:
        query_url = base_url + brand + " " + product + " prices"
        driver.get(query_url)
        #Extract list of prices and corresponding retailers
        prices = driver.find_elements_by_xpath('//p[@class="pa_price b_ads1line"]')
        retailers = driver.find_elements_by_xpath('//div[@class="b_attribution b_ads1line"]')
        retail_price_map[brand][product] = []
        ptr_p = 0
        ptr_r = 0
        while(ptr_p < len(prices) and ptr_r < len(retailers)):
            if (not (retailers[ptr_r].text == "" or prices[ptr_p].text == "")):
                retail_price_map[brand][product].append(retailers[ptr_r].text +
                                                        " : " + prices[ptr_p].text)
            ptr_p += 1
            ptr_r += 1
        write_json(retail_price_map)
        driver.delete_all_cookies()
        time.sleep(random.randint(0,3))
driver.close()
