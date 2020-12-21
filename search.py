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
from selenium.webdriver.remote.command import Command
import pyttsx3
import datetime as dt
import json
import pickle
import pickle
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import random

"""
Gmail API for personal account
"""
class Gmail_Personal:
    def __init__(self):
        self.SCOPES=['https://www.googleapis.com/auth/gmail.readonly']
        self.count = pickle.load(open("personalMail.pkl","rb"))

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
        results = service.users().messages().list(userId='me',labelIds=['UNREAD','INBOX']).execute()
        messages = results.get('messages',[])
        if not messages:
            Assistant().speak("no new message in your personal Account")
            os.remove('C:\college\Github_improvement\Search\personalMail.pkl')
            pickle.dump([0],open("personalMail.pkl","wb"))
        else:
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me',id=message['id']).execute()
                message_count+=1
            if message_count>self.count[0]:
                Assistant().speak("you have a new message in your personal Account sir")
                os.remove('C:\college\Github_improvement\Search\personalMail.pkl')
                pickle.dump([message_count],open("personalMail.pkl","wb"))
            else:
                Assistant().speak("no new message in your personal Account")
                os.remove('C:\college\Github_improvement\Search\personalMail.pkl')
                pickle.dump([message_count],open("personalMail.pkl","wb"))

"""
Gmail API for work account
"""
class Gmail_Work:
    def __init__(self):
        self.SCOPES=['https://www.googleapis.com/auth/gmail.readonly']
        self.count = pickle.load(open("workMail.pkl","rb"))
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

        results = service.users().messages().list(userId='me',labelIds=['UNREAD','INBOX']).execute()
        messages = results.get('messages',[])
        if not messages:
            Assistant().speak("no new message in your work Account")
            os.remove('C:\college\Github_improvement\Search\workMail.pkl')
            pickle.dump([0],open("workMail.pkl","wb"))
        else:
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me',id=message['id']).execute()
                message_count+=1
            if message_count>self.count[0]:
                Assistant().speak("you have a new message in your work Account sir")
                os.remove('C:\college\Github_improvement\Search\workMail.pkl')
                pickle.dump([message_count],open("workMail.pkl","wb"))
            else:
                Assistant().speak("no new message in your work Account")
                os.remove('C:\college\Github_improvement\Search\workMail.pkl')
                pickle.dump([message_count],open("workMail.pkl","wb"))

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

class WebDriver:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.action = ActionChains(self.driver)

    def searchQuery(self,query,Open=False):
        self.driver.maximize_window()
        self.driver.get("https://www.google.com/search?q="+query+"&start0")
        if Open:
            wait = WebDriverWait(self.driver,100)
            wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="wp-tabs-container"]/div[1]/div[2]/div/div/div/div/div/div[2]/h3/a')))
            YtLink = self.driver.find_element_by_xpath('//*[@id="wp-tabs-container"]/div[1]/div[2]/div/div/div/div/div/div[2]/h3/a').get_attribute('href')
            print(YtLink)
            self.action.click(on_element=YtLink)
            self.action.perform()

class Search:
    def __init__(self):
        self.QueryResult = {}
        self.patterns = pickle.load(open("patterns.pkl","rb"))

    def FindTag(self,query):
        if query.lower() in self.patterns:
            return self.patterns[query]
        else:
            return "search"
            
    def FindQuery(self,query):
        tag = self.FindTag(query)
        if tag=="mail":
            self.LaunchEmail()
        elif tag=="search":
            self.LaunchSearch(query)
        elif tag=="entertainment":
            self.LaunchEntertainment()


    def LaunchEntertainment(self):

        def AddMusic():
            music = input("Enter music: ")
            library=pickle.load(open("library.pkl","rb"))
            library.append(music)
            pickle.dump(list(set(library)),open("library.pkl","wb"))
            self.LaunchSearch(music+" song",True)
        try:
            library = pickle.load(open("library.pkl","rb"))
            Assistant().speak("should I play some new music?")
            play_new = input("say something:")
            if play_new.lower()=="yes" or play_new.lower()=="y":
                AddMusic()
            else:
                music = random.choice(library)
                self.LaunchSearch(music+" song",True)
        except Exception:
            Assistant().speak("No music found in the Library, want to add music to the library?")
            if input().lower()=="yes" or input().lower()=='y':
                music = input("Enter music: ")
                pickle.dump([music],open("library.pkl","wb"))
                self.LaunchSearch(music+" song",True)
            
                

    def LaunchSearch(self,query,Open=False):
        Driver = WebDriver()
        Driver.searchQuery(query,Open)
        
    def LaunchEmail(self):
        Gmail_Personal().main()
        Gmail_Work().main()

assistant = Assistant()
assistant.greetings()
while(True):
    userInput = input("Say something: ")
    Search().FindQuery(userInput)
