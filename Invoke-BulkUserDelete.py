#https://developers.google.com/admin-sdk/directory/v1/quickstart/python
#https://developers.google.com/admin-sdk/directory/reference/rest#rest-resource:-users
#https://developers.google.com/admin-sdk/directory/v1/guides/authorizing
from __future__ import print_function
import json

import os.path
import csv
import datetime
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    # Open the CSV file
    with open("users2.csv", "r") as file:
    # Create a CSV reader object
        reader = csv.reader(file)

    # Skip the header row
        next(reader)
    # Open the CSV file for writing
        with open("http_calls.csv", "w", newline="") as csvfile:
        # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(["timestamp", "user", "outcome", "details"])

            # Iterate over the rows in the file using a for loop
            for row in reader:
                email = row[0]
            # Print the row
                #print(email)
                try:
                    response = service.users().delete(userKey=email).execute()
                    writer.writerow([datetime.datetime.now(), email, "Deleted", None])
                except Exception as e:
                    # Write the HTTP call event to the CSV file with an error
                    writer.writerow([datetime.datetime.now(), email, "error", str(e)])
          
    
if __name__ == '__main__':
    main()
