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

def main():
    ser = serial.Serial(port="COM3", timeout=1)
    ser.flush()



    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
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

    with open("senders.json", "r") as file:
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
    
    ser.write(serial_message.encode('utf-8'))

    with open("senders.json", "w") as file:
        json.dump(courses, file, indent=4)


if __name__ == '__main__':
    main()
