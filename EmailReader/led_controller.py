from gpiozero import Button
from gpiozero import LED
import json
import time
import serial

print("LED Controller starting!")
senders_json = "/home/pi/Documents/MyCodeFolder/PythonFolder/Scrapers/EmailReader/senders.json"
leds = {"Chem": LED(4),
        "SEHS": LED(17),
        "HOTA": LED(27),
        "TOK": LED(22),
        "Spanish": LED(23),
        "Math": LED(24),
        "English": LED(25),
        "Jap": LED(12),
        "Other": LED(5)}
off_button = Button(6)
time_limit = (60 + 55) * 60
start_time = time.time()

ser = serial.Serial(port="/dev/ttyACM0", timeout=1)
ser.flush()

with open(senders_json, "r") as file:
    senders = json.load(file)
    
for led in leds:
    if senders[led] > 0:
        leds[led].on()
        print(f"{led} is on!")
    else:
        print(f"{led} is off!")

while senders["Main_Controller"] and time.time() - start_time < time_limit:
    if off_button.is_pressed:
        senders["Main_Controller"] = False
        for sender in senders:
            if sender != "Main_Controller":
                senders[sender] = 0
                
for led in leds:
    leds[led].off()

ser.write(b" ")
ser.write(b"No new emails")

print("LEDS turned off!")

with open(senders_json, "w") as file:
    json.dump(senders, file, indent=4)

print("Script ended!")
