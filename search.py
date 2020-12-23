"""
import 
"""
from __future__ import print_function
import pickle
from typing import Text
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
import time
from collections import defaultdict
import re

#####################################################################################################
"""
Gmail API for personal account
"""
class Gmail_Personal:
    def __init__(self):
        self.SCOPES=['https://www.googleapis.com/auth/gmail.readonly']
        self.count = pickle.load(open("C:\college\Github_improvement\Search\Trained Data\personalMail.pkl","rb"))

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
            os.remove('C:\college\Github_improvement\Search\Trained Data\personalMail.pkl')
            pickle.dump([0],open("C:\college\Github_improvement\Search\Trained Data\personalMail.pkl","wb"))
        else:
            message_count = 0
            From=[]
            for message in messages:
                msg = service.users().messages().get(userId='me',id=message['id']).execute()
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']
                    if name== "From":
                        From.append(values['value'])
                message_count+=1

            if message_count>self.count[0]:
                if message_count-self.count[0]==1:
                    Assistant().speak("you have a new message in your personal Account sir")
                else:
                    To_Say = "you have " + str(message_count) + " new messages in your personal Account sir"
                    Assistant().speak(To_Say)
                os.remove('C:\college\Github_improvement\Search\Trained Data\personalMail.pkl')
                pickle.dump([message_count],open("C:\college\Github_improvement\Search\Trained Data\personalMail.pkl","wb"))
                Assistant().speak("Should i read it for you")
                toRead = input("Say something: ")
                if toRead.lower()=="yes" or toRead.lower()=="y":
                    for Name in From:
                        Assistant().speak("you have a message from "+ Name,True,True)
            else:
                Assistant().speak("no new message in your personal Account")
                os.remove('C:\college\Github_improvement\Search\Trained Data\personalMail.pkl')
                pickle.dump([message_count],open("C:\college\Github_improvement\Search\Trained Data\personalMail.pkl","wb"))
            

#####################################################################################################
"""
Gmail API for work account
"""
class Gmail_Work:
    def __init__(self):
        self.SCOPES=['https://www.googleapis.com/auth/gmail.readonly']
        self.count = pickle.load(open("C:\college\Github_improvement\Search\Trained Data\workMail.pkl","rb"))
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
            os.remove('C:\college\Github_improvement\Search\Trained Data\workMail.pkl')
            pickle.dump([0],open("C:\college\Github_improvement\Search\Trained Data\workMail.pkl","wb"))
        else:
            message_count = 0
            From = []
            for message in messages:
                msg = service.users().messages().get(userId='me',id=message['id']).execute()
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']
                    if name== "From":
                        From.append(values['value'])
                message_count+=1
            if message_count>self.count[0]:
                if message_count-self.count[0]==1:
                    Assistant().speak("you have a new message in your work Account sir")
                else:
                    To_Say = "you have " + str(message_count) + " new messages in your work Account sir"
                    Assistant().speak(To_Say)
                os.remove('C:\college\Github_improvement\Search\Trained Data\workMail.pkl')
                pickle.dump([message_count],open("C:\college\Github_improvement\Search\Trained Data\workMail.pkl","wb"))
                Assistant().speak("Should i read it for you")
                toRead = input("Say something: ")
                if toRead.lower()=="yes" or toRead.lower()=="y":
                    for Name in From:
                        Assistant().speak("you have a message from "+ Name,True,True)
            else:
                Assistant().speak("no new message in your work Account")
                os.remove('C:\college\Github_improvement\Search\Trained Data\workMail.pkl')
                pickle.dump([message_count],open("C:\college\Github_improvement\Search\Trained Data\workMail.pkl","wb"))

#####################################################################################################
"""
Assistant class for the voice of Assitant
"""
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

    def speak(self,query,slow=False,verySlow=False):
        if not slow:
            self.engine.say(query)
            self.engine.runAndWait()
        else:
            if not verySlow:
                self.engine.setProperty('rate',155)
                self.engine.say(query)
                self.engine.runAndWait()
            else:
                self.engine.setProperty('rate',140)
                self.engine.say(query)
                self.engine.runAndWait()

    def error(self):
        self.engine.say("sorry, didn't understand your query")
        self.engine.runAndWait()

#####################################################################################################
"""
WebDriver Class for Handling the Browser Control
"""
class WebDriver:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.action = ActionChains(self.driver)
        self.driver.maximize_window()

    def searchQuery(self,query,Open=False):

        def IsAnswer():
            try:
                answer = self.driver.find_element_by_css_selector("div.Z0LcW")
                answer=answer.text
                Assistant().speak(answer,True)
                return True
            except:
                return False

        def FindCite(cite):
            unwanted_prefix = ["en","www","in","us"]
            try:
                cite = cite.strip("https://")
                for i in unwanted_prefix:
                    try:
                        cite=cite.strip(i)
                        cite=cite.strip(".")
                    except:
                        continue
            except:
                for i in unwanted_prefix:
                    try:
                        cite=cite.strip(i)
                        cite=cite.strip(".")
                    except:
                        continue
            cite=cite.strip(".")
            cite=cite.split(".")
            return cite[0]

        self.driver.get("https://www.google.com/search?q="+query+"&start0")
        wait = WebDriverWait(self.driver,100)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,"div.GyAeWb")))
        self.flag=False
        try: 
            self.flag = IsAnswer()
            featured_snippet=self.driver.find_element_by_css_selector('span.hELpae')
            info = self.driver.find_element_by_css_selector('span.hgKElc').text
            Cite = FindCite(self.driver.find_element_by_css_selector("cite.iUh30").text)
            if len(info)<1:
                Text = "These are the top results i found for you"
                Assistant().speak(Text,True)
                return
            Text = "According to " + Cite + info
            Assistant().speak(Text,True)
        except:
            if self.flag:
                return
            try:
                wiki = self.driver.find_element_by_css_selector("div.kp-wholepage")
                info=self.driver.find_element_by_css_selector('div.kno-rdesc span')
                Text = "According to wikipedia " + info.text
                Assistant().speak(Text,True)
            except:
                Text = "These are the top results i found for you"
                Assistant().speak(Text,True)
    
    def Play(self,query):
        query = "+".join(str(text) for text in query.split(" "))
        query=query.strip("+")
        self.driver.get('https://www.youtube.com/results?search_query='+query)
        wait = WebDriverWait(self.driver,100)
        wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR,'ytd-video-renderer.ytd-item-section-renderer a#video-title')))
        linksFound = self.driver.find_elements_by_css_selector('ytd-video-renderer.ytd-item-section-renderer a#video-title')
        linkToOpen = min(1,len(linksFound))
        for i in range(linkToOpen):
            toOpen = linksFound[i].get_attribute('href')
            self.driver.get(toOpen)
    
    def Quit(self):
        self.driver.quit()
               
#####################################################################################################
"""
Class for the main working of Assistant
"""
class Search:
    def __init__(self):
        self.QueryResult = {}
        self.patterns = pickle.load(open("C:\college\Github_improvement\Search\Trained Data\patterns.pkl","rb"))

    def FindTag(self,query):
        if query.lower() in self.patterns:
            return self.patterns[query]
        elif re.search("what is my",query) or re.search("who is my",query) or re.search("tell me my",query) or re.search("my",query):
            return "AboutOwner"
        else:
            return "search"
            
    def FindQuery(self,query):
        tag = self.FindTag(query)
        if tag=="mail":
            return self.LaunchEmail()
        elif tag=="search":
            return self.LaunchSearch(query)
        elif tag=="entertainment":
            return self.LaunchEntertainment()
        elif tag=="aboutYou":
            return self.LaunchAbout(query)
        elif tag=="AboutOwner":
            return self.LaunchAboutMe(query)
        elif tag=="close":
            return self.LaunchShutdown()
    
    def LaunchShutdown(self):
        Text = "Have a nice day"
        Assistant().speak(Text)
        return 1
        
    def LaunchAbout(self,query):
        SelfInfo = pickle.load(open("C:\college\Github_improvement\Search\Trained Data\SelfInfo.pkl","rb"))
        def differentiate(query):
            age = ["age","old"]
            for var in age:
                if var in query:
                    return True
            return False
        if differentiate(query):
            Text = random.choice(SelfInfo["age"])
            Assistant().speak(Text)
        else:
            Text = random.choice(SelfInfo["name"])
            Assistant().speak(Text)
        return None

    def LaunchEntertainment(self):
        def AddMusic(library):
            music = input("Enter music: ")
            library.append(music)
            pickle.dump(list(set(library)),open("C:\college\Github_improvement\Search\Trained Data\library.pkl","wb"))
            Driver = WebDriver()
            Driver.Play(music)
        try:
            library = pickle.load(open("C:\college\Github_improvement\Search\Trained Data\library.pkl","rb"))
            time.sleep(1)
            Assistant().speak("should I play some new music?")
            play_new = input("choice: ")
            if play_new.lower()=="yes" or play_new.lower()=="y":
                AddMusic(library)
            else:
                music = random.choice(library)
                Driver = WebDriver()
                Driver.Play(music)
        except Exception:
            Assistant().speak("No music found in the Library, want to add music to the library?")
            ch = input("choice: ")
            if ch.lower()=="yes" or ch.lower()=="y":
                music = input("Enter music: ")
                pickle.dump([music],open("C:\college\Github_improvement\Search\Trained Data\library.pkl","wb"))
                Driver = WebDriver()
                Driver.Play(music)
        return None

    def LaunchAboutMe(self,query,exact=False):
        def return_Person_And_Query(query):
            ignore_char = ['.',"'",","]
            req_query_list = query.split(" ")

            if len(req_query_list)>1:
                req_person = req_query_list[0]
                req_query = req_query_list[1]
                for char in ignore_char:
                    if char in req_query:
                        idx = req_query.index(char)
                        req_query = req_query[:idx]
                    if char in req_person:
                        idx = req_person.index(char)
                        req_person = req_person[:idx]
                try:
                    req_query=req_query.rstrip("s")
                except:
                    pass
                return (req_person,req_query)

            else:
                req_query = req_query_list[0]

                for char in ignore_char:
                    if char in req_query:
                        idx = req_query.index(char)
                        req_query = req_query[:idx]
                return ("me",req_query)

        def Find_Exact_Query(query):
            query=query.lower()
            e=0
            if re.search("what is my",query):
                for match in re.finditer("what is my",query):
                    e=match.end()
                req_query = query[e+1:]
                req_query = req_query.strip(" ")
                return return_Person_And_Query(req_query)
            if re.search("who is my",query):
                for match in re.finditer("who is my",query):
                    e=match.end()
                req_query = query[e+1:]
                req_query = req_query.strip(" ")
                return return_Person_And_Query(req_query)
            if re.search("my",query):
                for match in re.finditer("my",query):
                    e=match.end()
                req_query = query[e+1:]
                req_query = req_query.strip(" ")
                return return_Person_And_Query(req_query)
            if re.search("tell me my",query):
                for match in re.finditer("tell me my",query):
                    e=match.end()
                req_query = query[e+1:]
                req_query = req_query.strip(" ")
                return return_Person_And_Query(req_query)

        person,query = Find_Exact_Query(query)    
        try:
            my_info = pickle.load(open("C:\college\Github_improvement\Search\Trained Data\My_Info.pkl","rb"))
            if person in my_info:
                req_person = my_info[person]
                if query in req_person:
                    Assistant().speak(req_person[query])
                else:
                    Text = "I dont know but i will remember if you tell me"
                    Assistant().speak(Text,True)
                    ch = input("choice: ")
                    if ch.lower()=="yes" or ch.lower()=="y":
                        To_be_saved_query = input("Say Something: ")
                        req_person[query]=To_be_saved_query
                        pickle.dump(my_info,open("C:\college\Github_improvement\Search\Trained Data\My_Info.pkl","wb"))
                    else:
                        return None
            else:
                Text = "I dont know but i will remember if you tell me"
                Assistant().speak(Text,True)
                ch = input("choice: ")
                if ch.lower()=="yes" or ch.lower()=="y":
                    new_dict_to_be_saved = {}
                    To_be_saved_query = input("Say Something: ")
                    new_dict_to_be_saved[query]=To_be_saved_query
                    my_info[person] = new_dict_to_be_saved
                    pickle.dump(my_info,open("C:\college\Github_improvement\Search\Trained Data\My_Info.pkl","wb"))
                else:
                    return None
        except:
            Text = "I dont know but i will remember if you tell me"
            Assistant().speak(Text,True)
            ch = input("choice: ")
            if ch.lower()=="yes" or ch.lower()=="y":
                dict_to_be_saved={}
                final_dict={}
                To_be_saved_query = input("Say Something: ")
                dict_to_be_saved[query]=To_be_saved_query
                final_dict[person] = dict_to_be_saved
                pickle.dump(final_dict,open("C:\college\Github_improvement\Search\Trained Data\My_Info.pkl","wb"))
            else:
                return None
        return None

    def LaunchSearch(self,query,Open=False):
        Driver = WebDriver()
        Driver.searchQuery(query,Open)
        return None
        
    def LaunchEmail(self):
        Gmail_Personal().main()
        Gmail_Work().main()
        return None

if __name__ == "__main__":
    assistant = Assistant()
    assistant.greetings()
    while(True):
        userInput = input("Say something: ")
        val = Search().FindQuery(userInput)
        if val!=None:
            break
    