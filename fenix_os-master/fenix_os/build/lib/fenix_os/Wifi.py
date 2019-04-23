#!/usr/bin/python
# -*- coding: utf-8 -*-

# System dependencies
import threading
import time
import sys
import urllib.request, urllib.error, urllib.parse
import os
import json
import pexpect

from PIL import Image
from time import sleep
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from minitel.ImageMinitel import ImageMinitel
from minitel.constantes import (ENVOI, ANNULATION)
from multiprocessing import Process
from threading import Thread, Condition
from stat import S_ISREG, ST_CTIME, ST_MODE

class Wifi:
    def __init__(self):
        self.ssid = ''
        self.ssids = list()
        self.pesskey = ''
        self.connected = False
        return
    def IsConnected(self):
        try:
            r = urllib.request.urlopen('http://216.58.208.238', timeout=10)
            return True
        except:
            return False

    def GetSsids(self, m):
        m.WriteLnString("Searching network...")
        child = pexpect.run('wifi')
        child = child.split('\n')
        first = list()
        for elem in child:
            elem = elem.split(' ')
            elem = [ e for e in elem if e != ''][1:-1]
            if len(elem) != 0 and elem not in first:
                first.append(elem)
        second = list()
        for elem in first:
            second.append(''.join(str(e) + ' ' for e in elem))
        self.ssids = second

    def PrintSsids(self, m):
        ssidFound = False
        tr = 0
        while not ssidFound and tr < 10:
            try:
                self.GetSsids(m)
                ssidFound = True
                print('[+] SSIDs found : ' + str(len(self.ssids)))
            except Exception as e:
                print(str(e))
                pass
            tr = tr + 1
        if not ssidFound:
            print('[-] Any networks found')
            return
        y = 5
        for ssid in self.ssids:
            print('[*] ' + ssid)
            m.WriteLnString(str(y - 4) +' ' + ssid)
            y = y + 1
            if y > 15:
                break
        m.WriteLnString("Choose your network number")

    def SelectSsid(self, m):
        networkChoose = False
        while not networkChoose:
            num = m.ReadString()
            try:
                if int(num) == 0:
                    raise 
                self.ssid = self.ssids[int(num) - 1]
                print('[+] Network choose : ' + self.ssid)
                networkChoose = True
            except Exception as e:
                print('[-] Error : ' + str(e))
                m.WriteLnString("The network " + num + " is not in list.")

    def getPasskey(self, m):
        header(m)
        m.WriteLnString("Enter passkey for " + self.ssid + " :")
        m.WriteLnString("Passkey: ")
        self.passkey = m.ReadString()
        print('[+] Passkey : ' + self.passkey)

    def Connexion(self, m):
        tr = 0
        m.WriteLnString("Waiting connexion in process...")
        pexpect.run('sudo ifdown wlan0')
        pexpect.run('sudo ifup wlan0')
        while not self.connected and tr < 5:
            child = pexpect.spawn('sudo wifi connect -a ' + self.ssid, timeout=100)
            ret = child.expect([pexpect.TIMEOUT, 'passkey>', pexpect.EOF])
            if ret == 1:
                self.connected = True
            else:
                error = child.after if type(child.after) == str else child.before
                error = ' : ' + error if type(error) == str else ''
                print('[-] Error no' + str(tr + 1) + error[:-1])
            tr = tr + 1
            time.sleep(1)
        if not self.connected:
            print('[-] Connexion failed')
            m.ClearScreen()
            m.WriteLnString("Connexion failed")
            return False
        child.sendline(self.passkey)
        ret = child.expect([pexpect.TIMEOUT, r'\s*$', pexpect.EOF])
        if ret == 1:
            print('[+] Connexion successed')
            return True
        else:
            print('[-] Error : ' + str(child.after))
        return False


