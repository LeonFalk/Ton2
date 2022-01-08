# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 14:28:06 2022

@author: Leon

Ein Distortion-Effekt wird mit Hilfe einer nichtlinearen Kennlinie erzeugt. 
Programmieren Sie die vorgegebenen Kennlinien, verzerren Sie die Test-Signale damit, 
und berechnen Sie den Klirrfaktor der Systeme.

Kennlinie 8:  y = -0.5/tan(x+π/2)  


Fragen:
    Ist unser Tangens korrekt?
    bzw was ist los?
    
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import soundfile as sf

def ausgabe(samplerate, array):
    print(array)
    
    ###     Plot ausgeben
    fig, ax = plt.subplots()
    ax.plot(array)
    ax.grid()
    plt.show()

    ###     Sound-Ausgabe
    sd.play(array, samplerate)
    ###sf.write('name.flac', array, samplerate)


def main():
    
    ### Testsignal auswerten und einlesen
    testsignal = input("Wollen Sie Testsignal 1 oder 2 auswerten?\n")
    
    if testsignal   == '1':
        testsignal  = 'testsignal1.wav'
    elif testsignal == '2':
        testsignal  = 'testsignal2.wav'
    else: 
        print("Fehleingabe -> Testsignal 1 wird genutzt")
        testsignal  	= 'testsignal1.wav'
       
    samplerate, data    = wavfile.read(testsignal)
    
    if data.ndim == 2:
        y_L = data[:, 0]
        y_R = data[:, 1]
        data = (y_L + y_R) /2
    
    ### Normierung -> ?
    data = data / samplerate
    
    ### Testausgabe
    print("Testausgabe data")
    ausgabe(samplerate, data)
    ### Delay Einbauen
    
    ### System A: Distortion Effekt
    ### y = -0.5/np.tan(x + (np.pi / 2))  
    
    array_x = np.arange(data.size)
    array_y = np.zeros(data.size)
    
    ### Neue Vorgehensweise -> Multiplikation
    for i in range(data.size):
        data[i] = -0.5/np.tan(data[i] + np.pi / 2)

    ### Testausgabe
    print("Testausgabe data")
    ausgabe(samplerate, data)        
    
    
    ### Alte Vorgehensweise -> Faltung
    '''
    for i in range(data.size):
        array_y[i] = -0.5/np.tan(array_x[i] + np.pi / 2)
        
        
        ### testweise Beschneidung
        ###c = 1000
        ###if array_y[i] > c:
        ###    array_y[i] = c
        ###elif array_y[i] < c*-1:
        ###   array_y[i] = c*-1
        
    
    ### Testausgabe
    print("Testausgabe array_y")
    ausgabe(samplerate, array_y)
    
    ### Faltung zwischen Distortion Array (array_y) und dem Testsignal (data)
    array_convolve = np.convolve(array_y, data)
    
    ### Testausgabe
    print("Testausgabe Convolve")
    ausgabe(samplerate, array_convolve)
    '''
        
#####################
main()