"""
import 
"""
from __future__ import print_function
import pickle
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyttsx3
import datetime as dt
import json
import pickle
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request




"""
The code starts from here
"""

"""
Gmail API for personal account
"""
class Gmail_Personal:
    def __init__(self):
        self.SCOPES=['https://www.googleapis.com/auth/gmail.readonly']

    def main(self):
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
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    #results = service.users().labels().list(userId='me').execute()
    #labels = results.get('labels', [])

        results = service.users().messages().list(userId='me',labelIds=['UNREAD'], q="is:unread AND after:<time_since_epoch_in_seconds>").execute()
        messages = results.get('messages',[])


        if not messages:
            Assistant().speak('No messages found')
        else:
            message_count = 0
            for message in messages:
                print(message)
                msg = service.users().messages().get(userId='me',id=message['id']).execute()
                message_count+=1
            Assistant().speak('you have '+str(message_count)+" messages")


"""
Gmail API for work account
"""
class Gmail_Work:
    def __init__(self):
        self.SCOPES=['https://www.googleapis.com/auth/gmail.readonly']

    def main(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
        if os.path.exists('token1.pickle'):
            with open('token1.pickle', 'rb') as token:
                creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open('token1.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    #results = service.users().labels().list(userId='me').execute()
    #labels = results.get('labels', [])

        results = service.users().messages().list(userId='me',labelIds=['UNREAD'], q="is:unread AND after:<time_since_epoch_in_seconds>").execute()
        messages = results.get('messages',[])


        if not messages:
            Assistant().speak('No messages found.')
        else:
            message_count = 0
            for message in messages:
                print(message)
                msg = service.users().messages().get(userId='me',id=message['id']).execute()
                message_count+=1
            Assistant().speak('you have '+str(message_count)+" messages")

class Assistant:

    def __init__(self):
        self.engine = pyttsx3.init()
        self.hour = dt.datetime.now().hour
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

    def greetings(self):
        if 0<=self.hour<12:
            self.engine.say("Good morning sir!")
            self.engine.runAndWait()
            self.engine.say("How may i help you?")
            self.engine.runAndWait()
        elif 12<=self.hour<5:
            self.engine.say("Good Afternoon sir!")
            self.engine.runAndWait()
            self.engine.say("How may i help you?")
            self.engine.runAndWait()
        else:
            self.engine.say("Good evening sir!")
            self.engine.runAndWait()
            self.engine.say("How may i help you?")
            self.engine.runAndWait()
    
    def speak(self,query):
        self.engine.say(query)
        self.engine.runAndWait()

    def error(self):
        self.engine.say("sorry, didn't understand your query")
        self.engine.runAndWait()

class Search:
    def __init__(self):
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.QueryResult = {}
        #self.action = ActionChains(self.driver)
        self.patterns = pickle.load(open("patterns.pkl","rb"))

    def FindTag(self,query):
        if query in self.patterns:
            return self.patterns[query]
        else:
            return Assistant().error()
            
    def FindQuery(self,query):
        tag = self.FindTag(query)
        if tag=="mail":
            print("launching")
            self.LaunchEmail()
        
    def LaunchEmail(self):
        Assistant().speak("Personal or work?")
        choice = int(input("your choice: "))
        if choice == 1:
            Gmail_Personal().main()
        else:
            Gmail_Work().main()


assistant = Assistant()
assistant.greetings()
userInput = input("Say something: ")
Search().FindQuery(userInput)