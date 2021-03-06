from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import path
import json
import time

driver_path = "/usr/bin/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(driver_path)

houses_json = "/home/pi/Documents/MyCodeFolder/PythonFolder/Scrapers/HouseScraper/houses.json"

driver.get("https://www.redfin.com")
print(driver.title)

search_bar = driver.find_element_by_id("search-box-input")

search_bar.send_keys("93955")
search_bar.send_keys(Keys.RETURN)

time.sleep(5)

max_input = driver.find_element_by_xpath("/html/body/div[1]/div[6]/div[2]/div[1]/div/div[2]/div/div[1]/form/div/div[2]/span[3]/span/span")
max_input.send_keys(Keys.RETURN)

time.sleep(1)

six_k = driver.find_element_by_xpath("/html/body/div[1]/div[6]/div[2]/div[1]/div/div[2]/div/div[1]/form/div/div[2]/span[3]/span/span/div/div[1]/div/div[22]").click()

time.sleep(1)

table_mode = driver.find_element_by_xpath("/html/body/div[1]/div[6]/div[2]/div[1]/div/div[2]/div/div[3]/button[2]").click()

time.sleep(1)

info_format = ["price", "beds", "baths"]
property_dict = {}
property_table = driver.find_element_by_css_selector("tbody")
for row_num, row in enumerate(property_table.find_elements_by_tag_name("tr")):
    data = row.find_elements_by_tag_name("td")
    key = data[1].text
    property_dict[key] = {}
    for element_num, element in enumerate(data[3:6]):
        property_dict[key][info_format[element_num]] = element.text
    print(property_dict[key])

with open(houses_json, 'r') as file:
    listed_props = json.load(file)

for property in property_dict:
    if property in listed_props["houses"]:
        print("House already in property_dict!")
        if property_dict[property] != listed_props["houses"][property]:
            print(f"Updated {property}!")
            listed_props["houses"][property] = property_dict[property]
        continue

    print(f"New Property: {property}!")
    listed_props["houses"][property] = property_dict[property]
    listed_props["led"] = True
    
listed_props["counter"] += 1
counter = listed_props["counter"]
print(f"Number of times script has been run: {counter}!")

with open(houses_json, 'w') as file:
    json.dump(listed_props, file, indent=4)

driver.close()
