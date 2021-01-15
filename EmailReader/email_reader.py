from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import senders
import serial

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
credentials_path = "/home/pi/Documents/MyCodeFolder/PythonFolder/Scrapers/EmailReader/credentials.json"
token_path = "/home/pi/Documents/MyCodeFolder/PythonFolder/Scrapers/EmailReader/token.pickle"
senders_path = "/home/pi/Documents/MyCodeFolder/PythonFolder/Scrapers/EmailReader/senders.json"

ser = serial.Serial(port="/dev/ttyACM0", timeout=1)
ser.flush()

"""Shows basic usage of the Gmail API.
   Lists the user's Gmail labels.
"""
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(token_path):
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)

# Call the Gmail API
"""results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

if not labels:
    print('No labels found.')
else:
    print('Labels:')
        for label in labels:
            print(label['name'])"""
    
# User properties
messages = service.users().messages()

results = messages.list(userId="me", labelIds=["INBOX"], maxResults=20).execute()["messages"]
message_num = 1

with open(senders_path, "r") as file:
    courses = json.load(file)

for message_obj in results:
    message = messages.get(userId="me", id=message_obj["id"]).execute()
    if "UNREAD" in message["labelIds"]:
        payload = message["payload"]
        for header in payload["headers"]:
            if header["name"] == "From":
                sender = header["value"]
                print(header["name"] + ":", sender, f"- {senders.get_course(sender)} - {message_num}")
                courses[senders.get_course(sender)] += 1
        message_num += 1
        messages.modify(userId="me", id=message_obj["id"], body={"removeLabelIds": ["UNREAD"]}).execute()
        courses["Main_Controller"] = True

serial_message = ""

for course in courses:
    email_num = courses[course]
    if course != "Main_Controller" and email_num > 0:
        serial_message += f"{course[0:2]}:{email_num} "
    
if len(serial_message) > 0:
    ser.write(serial_message.encode('utf-8'))
else:
    ser.write(b" ") # This serves to clear the screen
    ser.write(b"No new emails")

with open(senders_path, "w") as file:
    json.dump(courses, file, indent=4)
