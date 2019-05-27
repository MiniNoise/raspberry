#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import json
import pexpect
import urllib2
from minitel_tools import *

class Wifi:
    def __init__(self):
        self.ssid = ''
        self.ssids = list()
        self.pesskey = ''
        self.connected = False
        return
    def IsConnected(self):
        try:
            r = urllib2.urlopen('http://216.58.208.238', timeout=10)
            return True
        except:
            return False

    def GetSsids(self, m):
        renderText(m, {'x':5,'y':20,'text':'Searching network...'})
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
                self.getSsids(m)
                ssidFound = True
                print '[+] SSIDs found : ' + str(len(self.ssids))
            except Exception as e:
                print str(e)
                pass
            tr = tr + 1
        if not ssidFound:
            print '[-] Any networks found'
            return
        y = 5
        for ssid in self.ssids:
            print '[*] ' + ssid
            renderText(m, {'x':5,'y':y,'text':str(y - 4)+' '+ssid})
            y = y + 1
            if y > 15:
                break
        renderText(m, {'x':5,'y':20,'text':'Choose your network number'})

    def SelectSsid(self, m):
        networkChoose = False
        while not networkChoose:
            while True:
                num = m.recv(1)
                if num:
                    break
            try:
                if int(num) == 0:
                    raise 
                self.ssid = self.ssids[int(num) - 1]
                print '[+] Network choose : ' + self.ssid
                networkChoose = True
            except Exception as e:
                print '[-] Error : ' + str(e)
                renderText(m,{'x':5,'y':20,'text':'The network '+num+' is not in list.'})

    def getPasskey(self, m):
        header(m)
        renderText(m, {'x':5,'y':5,'text':'Enter passkey for '+self.ssid+' :'})
        renderText(m, {'x':5,'y':7,'text':'Passkey: '})
        self.passkey = readUntil(m, 'Envoi')
        print '[+] Passkey : ' + self.passkey

    def Connexion(self, m):
        tr = 0
        renderText(m,{'x':5,'y':20,'text':'Waiting connexion in process...'})
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
                print '[-] Error no' + str(tr + 1) + error[:-1]
            tr = tr + 1
            time.sleep(1)
        if not self.connected:
            print '[-] Connexion failed'
            clearLine(m, 20)
            renderText(m, {'x':5,'y':20,'text':'Connexion failed'})
            return False
        child.sendline(self.passkey)
        ret = child.expect([pexpect.TIMEOUT, r'\s*$', pexpect.EOF])
        if ret == 1:
            print '[+] Connexion successed'
            return True
        else:
            print '[-] Error : ' + str(child.after)
        return False


