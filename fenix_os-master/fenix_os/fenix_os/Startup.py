#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Fenix dependencies
from fenix_os.Wrapper import Wrapper
from fenix_api.FenixTwitter import FenixTwitter

# System dependencies
from multiprocessing import Process
from threading import Thread, Condition
from stat import S_ISREG, ST_CTIME, ST_MODE
import threading
import time
import sys
import urllib2
import os

"""
Class attribute :
    - Minitel minitel
    - string content

Class method :
    - Connect()
    - Disconnect()
    - GetString(char end)
    - SendString(string content)
    - SendString(string content, int line, int column)
"""

class Startup: # To get linked with the system that communicate directly with the Minitel

    w = None
    t = None
    thread_twitter_get = None
    thread_twitter_send = None
    new_tweet = False # Used to refresh stream with the new tweet that the user entered
    lock_input = False
    writing_tweet = False
    
    def __init__(self): # Constructor
        print("coucou")
        self.Launch()
        print("au revoir")


    def TwitterThreadGetStream(self, cond):
        while True:
            self.lock_input = True
            print("loading all tweets")
            tweets = self.t.GetTweets()

            medias = self.t.GetMediaList()
            medias = self.UpdateNewMedias(medias)
            for tmp in medias:
                print(tmp)
            self.GetImages(medias)
            
            self.lock_input = False
            self.w.ClearScreen()
            self.WriteHeader()
            i = 0;
            for tmp in tweets:

                # Lock this Thread() while writing tweet
                cond.acquire()
                if self.writing_tweet == True:
                    cond.wait()
                    i = 0
                cond.release()

                # Sending a new tweet to stream
                if self.new_tweet:
                    self.new_tweet = False
                    self.w.ClearScreen()
                    self.WriteHeader()
                    self.w.WriteLnString("Refreshing Twitter stream...")
                    break

                # Write tweet stream
                self.w.WriteLnString(tmp)
                self.w.WriteLnString()
                self.w.WriteLnString()
                i += 1
                if i >= 12: # No more than 12 latest tweets displayed
                    time.sleep(10)
                    self.lock_input = True
                    self.DisplayTwitterImages()
                    self.lock_input = False
                    break        
                if i % 3 == 0: # 3 tweets per page
                    time.sleep(10)
                    if self.writing_tweet == True:
                        continue
                    self.w.ClearScreen()
                    self.WriteHeader()


    def TwitterThreadSendMessage(self, cond):
        msg = str()
        while (True):
            # Wait for any key input
            self.w.WaitForAnyInput()
            if self.lock_input == True:
                continue
            print("clicked")

            # Pause Twitter Stream to write message
            cond.acquire()
            self.writing_tweet = True
            print("you can write now")

            # Display instructions
            self.w.ClearScreen()
            self.WriteHeader()
            self.w.WriteLnString("1. Write something (140 characters max)")
            self.w.WriteLnString("2. Press 'Envoi' button")
            self.w.WriteLnString("3. There is no 3. step")            
            self.w.WriteLnString()
            self.w.WriteString("#VivaTech ")

            # Get user tweet
            self.w.DisplayCursor(True)
            msg = self.w.ReadString()
            if msg is not None:
                msg = "#VivaTech " + msg
                #answer = self.t.SendTweet(msg) # Send Tweet
                time.sleep(2)
                print("msg: " + msg)

            # Resume Twitter Stream
            self.new_tweet = True
            self.w.DisplayCursor(False)
            cond.notify()
            self.writing_tweet = False
            print("end input")
            cond.release()


    def TestLoop(self):
        self.w.minitel.efface()
        self.w.minitel.definir_vitesse(1200)
        self.w.WriteString("TEST ON MINITEL")
        print(self.w.minitel.appeler("TEST", 4))
        self.w.WaitForAnyInput()
        print("After wait for any input")
        while 1:
            a = 1
            
    
    def Launch(self): # Pour le moment tout ce fait ici, c'est un peu sale mais je vais tout nettoyer après le salon

        # Init wrapper and Twitter API connection
        self.w = Wrapper()
        print("Sortie wrapper")
        self.w.Connect()
        print("Sortie connect")
        self.w.DisplayCursor(False)
        print("Sortie display cursor")
        self.w.WriteLnString(self.w.GetModel()+ " launched successfully")
        print("Sortie write ln string")
        self.t = FenixTwitter()
        print("Sortie fenix twitter")
        self.ClearImagesFolder()
        print("Sortie clear image folder")
        self.TestLoop()
        self.w.Disconnect()
        print("disconnected")

    def DisplayTwitterImages(self):
        image_list = []
        folder = "./twitter_images/"
        i = 0

        try:
            entries = (os.path.join(folder, fn) for fn in os.listdir(folder))
            entries = ((os.stat(path), path) for path in entries)
            entries = ((stat.st_ctime, path) for stat, path in entries if S_ISREG(stat[ST_MODE]))
            for cdate, path in sorted(entries):
                if (i >= 5): # Number of images to display
                    break
                i += 1
                image_list.append(path)        

        except Exception as e:
            print(e)
        self.w.DisplayImageList(image_list)
            
    # Avoid to download an already existing image in the Rasp
    def UpdateNewMedias(self, url_list):
        medias = []
        delete_img = False
        keep_img = False
        folder = "./twitter_images/"
        try:
            for img in os.listdir(folder): # Delete too old image
                keep_img = False
                for url in url_list:
                    if (img == os.path.basename(url)):
                        keep_img = True
                        break
                if (keep_img == False):
                    print("delete file: " + img)
                    self.DeleteImageFile(img)

            for url in url_list: # Avoid re-dl existing image
                for img in os.listdir(folder):
                    if (img == os.path.basename(url)):
                        delete_img = True
                        break
                if (delete_img == True):
                    delete_img = False
                else:
                    medias.append(url)
        except Exception as e:
            print(e)
        return medias

    def GetImages(self, url_list):
        for url in url_list:
            try:
                image = urllib2.urlopen(url)
                local_file = open("./twitter_images/" + os.path.basename(url), 'wb')
                local_file.write(image.read())
                local_file.close()
            except Exception as e:
                print(e)

    def ClearImagesFolder(self):
        folder = "./twitter_images/"
        print("In clear images folder")
        try:
            for img in os.listdir(folder):
                print("in for loop")
                img_path = os.path.join(folder, img)
                try:
                    if os.path.isfile(img_path):
                        os.unlink(img_path)
                except Exception as e:
                    raise(e)
        except Exception as e:
            print(e)
        print("end of for leave function")

    def DeleteImageFile(self, img_name):
        folder = "./twitter_images/"
        img_path = os.path.join(folder, img_name)
        try:
            if os.path.isfile(img_path):
                os.unlink(img_path)
        except Exception as e:
            print(e)

    def WriteHeader(self):
        self.w.WriteLnString("Fenix OS v0.2 - #VivaTech Twitter stream")
        self.w.WriteLnString("----------------------------------------")
        self.w.WriteLnString()

    def TryConnectTwitter(self, attempt = 1):
        if (attempt > 3):
            self.w.WriteLnString("Can't connect to Twitter API")
            return
        self.w.WriteLnString("Connecting to Twitter API. Attempt " + str(attempt))
        answer = self.t.Request()
        if (answer is None):
            self.w.WriteLnString("Status: No internet connection")
            self.TryConnectTwitter(attempt + 1)
        elif (answer.status_code != 200):
            self.w.WriteLnString("Status: " + str(answer.status_code) + ": Error")
            self.TryConnectTwitter(attempt + 1)
        else:
            self.w.WriteLnString("Status: " + str(answer.status_code) + ": Connected")
