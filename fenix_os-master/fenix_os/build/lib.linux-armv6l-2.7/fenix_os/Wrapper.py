#!/usr/bin/env python
# -*- coding: utf-8 -*-

from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from minitel.ImageMinitel import ImageMinitel
from minitel.constantes import (ENVOI, ANNULATION)

from PIL import Image
from time import sleep

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

class Wrapper: # To get linked with the system that communicate directly with the Minitel
    minitel = None
    
    def __init__(self): # Constructor
        self = self
        
    def Connect(self):  
        self.minitel = Minitel()
        if (self.minitel.deviner_vitesse() == -1):
            if (self.minitel.definir_vitesse(300) == False):
                return (1)
        self.minitel.identifier()
        while (self.minitel.capacite['nom'] == "Minitel inconnu"):
            time.sleep(2)
            self.minitel.identifier()

        self.minitel.definir_mode("VIDEOTEX")
        print("{} - {}".format(self.minitel.capacite['nom'], self.minitel.capacite['vitesse']))
        self.minitel.efface()
        self.minitel.debut_ligne()

    def DisplayImageList(self, file_list):
        largeur = 80
        hauteur = 72
        colonne = 1
        ligne = 1
        self.minitel.efface()
        for fichier in file_list:
                image = Image.open(fichier)
                image = image.resize((largeur, hauteur), Image.ANTIALIAS)

                image_minitel = ImageMinitel(self.minitel)
                image_minitel.importer(image)
                image_minitel.envoyer(colonne, ligne)

                self.minitel.sortie.join()
                sleep(3)
                self.minitel.efface()

    def ReadString(self, end = ENVOI): #TODO: faire un while plus propre while(valeurs != end)
        content = ""

        while True:
            received = self.minitel.recevoir_sequence(True, None)
            if (received.valeurs == end):
                content += '\0'
                break
            if (received.valeurs == ANNULATION): # Delete this condition after VivaTech event
                return None
            if (len(content) + 10) > 140: # Delete this condition after VivaTech event
                continue
            content += chr(received.valeurs[0])
            self.minitel.envoyer(received.valeurs[0]) 
        return content

    def DisplayCursor(self, display = True):
        self.minitel.curseur(display)

    def WaitForAnyInput(self):
        self.minitel.recevoir_sequence(True, None)    

    def WriteString(self, text = "default"):
        nb_column = 40
        nb_line = 24
        if (self.minitel.capacite['80colonnes'] == True):
            if (self.minitel.mode == 'MIXTE'):
                nb_column = 80
        text = text[0:nb_column * nb_line]
        s_send = Sequence()
        s_send.ajoute(text)
        self.minitel.envoyer(s_send)

    def GetModel(self):
        return self.minitel.capacite['nom']

    def WriteLnString(self, text = ""):
        nb_column = 40
        nb_line = 24
        if (self.minitel.capacite['80colonnes'] == True):
            if (self.minitel.mode == 'MIXTE'):
                nb_column = 80
        space_to_add = nb_column - (len(text) % nb_column)
        for i in range(space_to_add):
            text += " "
        text = text[0:nb_column * nb_line]
        s_send = Sequence()
        s_send.ajoute(text)
        self.minitel.envoyer(s_send)

    def ClearScreen(self):
        self.minitel.efface()

    def GetMinitel(self):
        return (self.minitel)

    def Disconnect(self):
        self.minitel.close()
