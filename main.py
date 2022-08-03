import json
import sqlite3
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

conn = sqlite3.connect("scrapped.s3db")
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS scrap(id INTEGER primary key, title TEXT, uri TEXT, price TEXT,detail TEXT)")
conn.commit()
arr = []


def scrap_data(i, uri):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(uri)
    title = driver.find_element("id", "productTitle").text
    image = driver.find_element("id", "imgBlkFront").get_attribute("src")
    price = driver.find_element("xpath", '//*[@id="a-autoid-3-announce"]/span[2]/span').text
    product_detail = driver.find_element("id", "detailBullets_feature_div").text
    arr.append({"title": title, "image_uri": image, "Price": price, "Product Details": product_detail})
    cur.execute(f"INSERT INTO scrap (id, title, uri, price, detail) VALUES (?, ?, ?, ?, ?);",
                (i, title, image, price, product_detail))
    driver.close()

with open('amazon.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
for line_count, row in enumerate(csv_reader):
    if line_count > 0:
        url = f'https://www.amazon.{row[3]}/dp/{row[2]}'
        response_code = requests.get(url).status_code
        if response_code == 200:
            scrap_data(line_count, url)
        else:
            print(f"{url} Not Available")
conn.commit()
with open("output.json", "w") as out:
    json.dump(arr, out)
