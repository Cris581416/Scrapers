from gpiozero import Button
from gpiozero import LED
import json
import time

print("LED Controller starting!")

button = Button(4)
led = LED(17)
led_on = False
houses_json = "/home/pi/Documents/MyCodeFolder/PythonFolder/Scrapers/HouseScraper/houses.json"
time_limit = (5 * 60 + 55) * 60 
start_time = time.time()

with open(houses_json, "r") as file:
    listed_props = json.load(file)

while listed_props["led"]:
    led.on()
    if time.time() - start_time >= time_limit:
        print("Time limit reached!")
        led_on = True
        break
    if button.is_pressed:
        print("Button was pressed!")
        led_on = False
        break

led.off()

listed_props["led"] = led_on

with open(houses_json, "w") as file:
    json.dump(listed_props, file, indent=4)

print("Script ended!")
