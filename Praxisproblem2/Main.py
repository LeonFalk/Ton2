#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 08:17:31 2022

@author: VanessaZorn
"""

import numpy as np
from scipy.io.wavfile import read, write
import sounddevice as sd
from time import sleep

###     Audiodateien einlesen

samplerate, data1    = read('Datei_1.wav')
array1 = np.array(data1)

samplerate, data2    = read('Datei_2.wav')
array2 = np.array(data2)


###     a.) Laufzeitdifferenzen zwischen L und R einstellen

def Laufzeitdifferenzen (array, diffinsek, kanal):
    kanal_L = array[:,0]
    kanal_R = array[:,1]
    
    laufzeitdifferenz = int(diffinsek * samplerate)
    
    if   (kanal == "L"):
        kanal_L = np.insert(kanal_L, 0, np.zeros(laufzeitdifferenz))
        #kanal_L = np.delete(kanal_L, np.arange(kanal_L.size - laufzeitdifferenz, kanal_L.size)) 
    elif (kanal == "R"):
        kanal_R = np.insert(kanal_R, 0, np.zeros(laufzeitdifferenz))
        #kanal_R = np.delete(kanal_R, np.arange(kanal_R.size - laufzeitdifferenz, kanal_R.size))
    
    stereo = np.column_stack((kanal_L, kanal_R))
    stereo *= int(32767 / np.max(np.abs(stereo)))
    stereo = stereo.astype(np.int16)
    
    return stereo
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
###############################################################################
  
    def main():
        Laufzeitdifferenzen (array1, 0.5, "L")
    
    
    
###     Main        ###########################################################
    main()  
    