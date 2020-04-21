import json
import time

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found")
    
with open("./products.json", encoding = 'utf-8') as j:
    data = json.load(j)

brandurls = dict()
for brand in data:
    for url in search(brand, tld='com', lang='en', num=1, start=0, stop=1, pause=1.0):
        brandurls[brand] = url
    time.sleep(1)
    
with open("brandurls.json", 'w') as outfile:
    json.dump(brandurls, outfile)
