from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import path
import time

driver_path = path.join(path.dirname(path.abspath(__file__)), "chromedriver")
driver = webdriver.Chrome(driver_path)

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

property_list = []
property_table = driver.find_element_by_css_selector("tbody")
for row_num, row in enumerate(property_table.find_elements_by_tag_name("tr")):
    property_list.append(row.find_elements_by_tag_name("td")[1].text)

print(property_list)

driver.close()
