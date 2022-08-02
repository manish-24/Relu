import csv
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
out = open("output.json", "w")

arr = []




def func(url):
    map = {}
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    title = driver.find_element("id", "productTitle").text
    map["title"]=title
    print(title)
    image = driver.find_element("id", "imgBlkFront").get_attribute("src")
    map['image']=image
    print(image)
    price = driver.find_element("xpath", '//*[@id="a-autoid-3-announce"]/span[2]/span').text
    map["price"]=price
    print(price)
    product_detail = driver.find_element("id", "detailBullets_feature_div").text
    map["product_detail"] = product_detail
    print(product_detail)
    arr.append(map)
    driver.close()
# func("https://www.amazon.it/dp/000416198X")
with open('amazon.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for line_count, row in enumerate(csv_reader):
        if line_count > 0:
            url = f'https://www.amazon.{row[3]}/dp/{row[2]}'
            response = requests.get(url)
            if response.status_code == 200:
                func(url)
            else:
                print(f"{url} Not Available")
json.dump(json.dumps(arr), out)
out.close()