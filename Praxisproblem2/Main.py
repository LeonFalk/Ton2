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

def Laufzeitdifferenzen (array, diffinms, kanal):
    if array.ndim == 2:
        kanal_L = array[:,0]
        kanal_R = array[:,1]
    elif array.ndim == 1:
        kanal_L = array
        kanal_R = array
    
    laufzeitdifferenz = int((diffinms/1000) * samplerate)
    
    if   kanal == "L":
        kanal_L = np.pad(kanal_L, (0, laufzeitdifferenz), 'constant')
        kanal_L[np.arange(kanal_L.size-laufzeitdifferenz)]
    elif kanal == "R":
        kanal_R = np.pad(kanal_R, (0, laufzeitdifferenz), 'constant')
        kanal_R[np.arange(kanal_R.size-laufzeitdifferenz)]
        
    kanal_L_R = np.column_stack((kanal_L, kanal_R))
    sd.play(kanal_L_R, samplerate)
    sd.wait()


###     b.) Pegeldifferenzen zwischen L und R einstellen

def Pegeldifferenzen (array, diffindB, kanal):
    kanal_L = array[:,0]
    kanal_R = array[:,1]
    
    # X dB = 10 log (neuer Wert/alter Wert)
    # neuer Wert = 10^(X/10) * alter Wert
    
    if kanal == "L":
        kanal_L = [i*(10**(diffindB/10)) for i in kanal_L]
    elif kanal == "R":
        kanal_R = [i*(10**(diffindB/10)) for i in kanal_R]
    
    kanal_L_R = np.column_stack((kanal_L, kanal_R))
    sd.play(kanal_L_R, samplerate)
    sd.wait()
    
###     e.) Signal automatisch von links nach rechts wandern lassen

def Wandersignal (array):
    size = len(array)/9
    array1 = array[1:(size-1)]
    array2 = array[size:((2*size)-1)]
    array3 = array[(2*size):((3*size)-1)]
    array4 = array[(3*size):((4*size)-1)]
    array5 = array[(4*size):((5*size)-1)]
    array6 = array[(5*size):((6*size)-1)]
    array7 = array[(6*size):((7*size)-1)]
    array8 = array[(7*size):((8*size)-1)]
    array9 = array[(8*size):(9*size)]
    
    Laufzeitdifferenzen (array1, float(1.2), "L") #100% Links
    Laufzeitdifferenzen (array2, float(0.53), "L") #75% Links
    Laufzeitdifferenzen (array3, float(0.32), "L") #50% Links
    Laufzeitdifferenzen (array4, float(0.15), "L") #25% Links
    sd.play(array5) #Mitte
    Laufzeitdifferenzen (array6, float(0.15), "R") #25% Rechts
    Laufzeitdifferenzen (array7, float(0.32), "R") #50% Rechts
    Laufzeitdifferenzen (array8, float(0.53), "R") #75% Rechts
    Laufzeitdifferenzen (array9, float(1.2), "R") #100% Rechts
    
     
    
    'Länge des Arrays durch 9 teilen und dann wandern lassen'
    
###############################################################################
  
def main():
    
### LAUFZEITDIFFERENZEN
### Werte nach Simonsen (1984)
        
    print("a.) Laufzeitdifferenzen-Test")
        
    ### SIGNAL 1
        
    print("Signal 1 - Linker Kanal - Differenzen in ms:")
        
    print("0,15")   #25%
    Laufzeitdifferenzen (array1, float(0.15), "L")
    print("0,32")   #50%
    Laufzeitdifferenzen (array1, float(0.32), "L")
    print("0,53")   #75%
    Laufzeitdifferenzen (array1, float(0.53), "L")
    print("1,2")    #100%
    Laufzeitdifferenzen (array1, float(1.2), "L")
        
        
    print("Signal 1 - Rechter Kanal - Differenzen in ms:")
        
    print("0,15")   #25%
    Laufzeitdifferenzen (array1, float(0.15), "R")
    print("0,32")   #50%
    Laufzeitdifferenzen (array1, float(0.32), "R")
    print("0,53")   #75%
    Laufzeitdifferenzen (array1, float(0.53), "R")
    print("1,2")    #100%
    Laufzeitdifferenzen (array1, float(1.2), "R")
        
    ### SIGNAL 2
    
    print("Signal 2 - Linker Kanal - Differenzen in ms:")
    
    print("0,15")   #25%
    Laufzeitdifferenzen (array2, float(0.15), "L")
    print("0,32")   #50%
    Laufzeitdifferenzen (array2, float(0.32), "L")
    print("0,53")   #75%
    Laufzeitdifferenzen (array2, float(0.53), "L")
    print("1,2")    #100%
    Laufzeitdifferenzen (array2, float(1.2), "L")
        
    
    print("Signal 2 - Rechter Kanal - Differenzen in ms:")
    
    print("0,15")   #25%
    Laufzeitdifferenzen (array2, float(0.15), "R")
    print("0,32")   #50%
    Laufzeitdifferenzen (array2, float(0.32), "R")
    print("0,53")   #75%
    Laufzeitdifferenzen (array2, float(0.53), "R")
    print("1,2")    #100%
    Laufzeitdifferenzen (array2, float(1.2), "R")
        
        
### PEGELDIFFERENZEN
### Werte nach Simonsen (1984)

    print("b.) Pegeldifferenzen-Test")
        
    ### SIGNAL 1
        
    print("Signal 1 - Linker Kanal - Differenzen in dB:")
      
    print("0,15")   #25%
    Pegeldifferenzen (array1, float(2), "L")
    print("0,32")   #50%
    Pegeldifferenzen (array1, float(4.6), "L")
    print("0,53")   #75%
    Pegeldifferenzen (array1, float(8), "L")
    print("1,2")    #100%
    Pegeldifferenzen (array1, float(18), "L")
    
    
    print("Signal 1 - Rechter Kanal - Differenzen in dB:")
    
    print("0,15")   #25%
    Pegeldifferenzen (array1, float(2), "R")
    print("0,32")   #50%
    Pegeldifferenzen (array1, float(4.6), "R")
    print("0,53")   #75%
    Pegeldifferenzen (array1, float(8), "R")
    print("1,2")    #100%
    Pegeldifferenzen (array1, float(18), "R")
    
    ### SIGNAL 2
    
    print("Signal 2 - Linker Kanal - Differenzen in dB:")
    
    print("0,15")   #25%
    Pegeldifferenzen (array2, float(2), "L")
    print("0,32")   #50%
    Pegeldifferenzen (array2, float(4.6), "L")
    print("0,53")   #75%
    Pegeldifferenzen (array2, float(8), "L")
    print("1,2")    #100%
    Pegeldifferenzen (array2, float(18), "L")
        
        
    print("Signal 2 - Rechter Kanal - Differenzen in dB:")
        
    print("0,15")   #25%
    Pegeldifferenzen (array2, float(2), "R")
    print("0,32")   #50%
    Pegeldifferenzen (array2, float(4.6), "R")
    print("0,53")   #75%
    Pegeldifferenzen (array2, float(8), "R")
    print("1,2")    #100%
    Pegeldifferenzen (array2, float(18), "R")
        
        
### KOMPENSATION
        
    print("c.) Kompensation der Pegeldifferenz durch Laufzeitdifferenz")
    
    ### SIGNAL 1
    
    print("Signal 1")
    print("Pegelerhöhung auf linkem Kanal um 4,6 dB")
    Pegeldifferenzen (array1, float(4.6), "L") #50%
    print("Laufzeitversatz auf linkem Kanal um 0,32 ms")
    Laufzeitdifferenzen (array2, float(0.32), "L") #50%
    
    ### SIGNAL 2
    
    print("Signal 2")
    print("Pegelerhöhung auf rechtem Kanal um 4,6 dB")
    Pegeldifferenzen (array2, float(4.6), "R") #50%
    print("Laufzeitversatz auf rechtemKanal um 0,32 ms")
    Laufzeitdifferenzen (array2, float(0.32), "R") #50%
        
        
### AUFSPALTUNG DER PHANTOMSCHALLQUELLE
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
### AUTOMATISCHES WANDERN DES SIGNALS VON LINKS NACH RECHTS   
 
    print("e.) Wanderndes Signal - Signal 1:")
    Wandersignal (array1)
    
    print("Signal 2:")
    Wandersignal (array1)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
###     Main        ###########################################################
main()  
    