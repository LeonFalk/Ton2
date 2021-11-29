# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:58:02 2021

@author: Leon
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx

def master_of_integration(start_value, stop_value, data):
    y = 0
    array_integr = np.zeros((stop_value))
    
    for i in range((start_value)*-1, (stop_value)*-1, -1):
         y = y + np.square(data[i])
         array_integr[i] = y
    return array_integr

def berechnen_T60(array, samplerate):
    value_5 = find_nearest(array, -5)
    value_15 = find_nearest(array, -15) 
    print("Nachhallzeit T60: ", (value_15 - value_5)/samplerate *6, " Sekunden")

def ausgabe_plot(array):
#Anzeige in Sekunden fehlt noch -> der Plot sollte noch angepasst werden und beides anzeigen + die x-Achse angepasst werden und beide Beschriftet werden
#   Energieabfall
#   plt.plot(array_integr)
#   Energieabfall Logarithmiert [Dezibel]
    plt.plot(array)
    plt.show()
    
   
'''     ###     C50
stop_value = data.size - 0.05*samplerate
array_integr = master_of_integration(data, int(stop_value))
'''

'''     ###     C80
stop_value = data.size - 0.08*samplerate
array_integr = master_of_integration(data, int(stop_value))
'''

def main():
###     Einlesen des Wavefiles
    samplerate, data = wavfile.read('Datei_1.wav')

###     Aufruf Integration
    array_integr = master_of_integration(1, int(data.size), data)
     
###     Normieren und Logarithmieren
    array_integr = array_integr/samplerate
    array_log_integr = np.zeros(data.size)
    array_log_integr = 10 * (np.log10(array_integr) - np.log10(np.max(array_integr)))

###     Plot ausgeben
    ausgabe_plot(array_integr)
    ausgabe_plot(array_log_integr)

###     Nachhallzeit ausrechnen
    berechnen_T60(array_log_integr, samplerate)
#    ausgabe_plot(-> T60 Gerade)

###     C50 berechnen
#   0 bis 50
#    c50_zaehler = np.max(master_of_integration(0, int(0.05*samplerate), data))
#   50 bis inf
#    c50_nenner = np.max(master_of_integration(int(0.05*samplerate), int(data.size), data))
#   ausrechnen
#    print(10 * np.log10(c50_zaehler/c50_nenner))

###     C80 berechnen
#   0 bis 80
#    c80_zaehler = np.max(master_of_integration(0, int(0.08*samplerate), data))
#   80 bis inf
#    c80_nenner = np.max(master_of_integration(int(0.08*samplerate), int(data.size), data))
#   ausrechnen
#    print(10 * np.log10(c80_zaehler/c80_nenner))
    
    
    
    
    
    
    
    
    
    
main()