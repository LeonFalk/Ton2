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
    
    array_integr = np.zeros((start_value))
    start_value = start_value - 1
    
    for i in range(start_value, stop_value, -1):
         y = y + np.square(data[i])
         array_integr[i] = y
    return array_integr

###     Nachhallzeit berechnen
def berechnen_T60(array, samplerate):
    value_5 = find_nearest(array, -5)
    value_15 = find_nearest(array, -15) 
    print("Nachhallzeit T60: \t\t\t", np.round((value_15 - value_5)/samplerate *6, 2), " Sekunden")

def main():
###     Einlesen des Wavefiles
    samplerate, data    = wavfile.read('Datei_1.wav')
###     Testdatei von Frau Wilk
#    samplerate, data    = wavfile.read('test_h_von_t.wav')
###     Wavedatei in Mono umwandeln, wenn Stereo    
    if data.ndim == 2:
        y_L = data[:, 0]
        y_R = data[:, 1]
        data = (y_L + y_R) /2

###     Aufruf Integration von NULL bis data.size
    array_integr        = master_of_integration(int(data.size), 0, data)
     
###     Normieren und Logarithmieren
    array_integr        = array_integr/samplerate
    print("Samplerate: \t\t\t\t", samplerate)
    print("Gesamtenergie des Signals:\t", np.round(np.max(array_integr), 2))
    array_log_integr    = np.zeros(data.size)
    array_integr[array_integr == 0] = 0.0000001                     #NULL-Werte auf kleinen Wert setzen, um Divisionsfehler(/0) zu umgehen
    array_log_integr    = 10 * (np.log10(array_integr) - np.log10(np.max(array_integr)))

###     Plot ausgeben
    fig, axs = plt.subplots(2)
    x = np.linspace(0., data.size/samplerate, data.size)
#    ausgabe_plot(array_integr, "array number", "Energie")
    axs[0].set_title("Energieabfall")
    axs[0].set_xlabel("Zeit in Sekunden")
    axs[0].set_ylabel("Energie")
    axs[0].plot(x ,array_integr)

#    ausgabe_plot(array_log_integr, "array number", "dB")
    axs[1].set_title("Energieabfall Logarithmiert")
    axs[1].set_xlabel("Zeit in Sekunden")
    axs[1].set_ylabel("dB")
    axs[1].plot(x, array_log_integr)
    fig.tight_layout()


###     Nachhallzeit ausrechnen
    berechnen_T60(array_log_integr, samplerate)
###     ausgabe_plot(-> T60 Gerade)

###     C50 berechnen
###      0 bis 50ms         ->  data[0.05*samplerate]==2400 bis data[0]==0
    c50_zaehler        = np.max(master_of_integration(int(0.05*samplerate), 0, data))
#    print("C50_zaehler: \t\t", c50_zaehler/samplerate)
###    50ms bis inf         -> data[data.size]== 65631 bis data[0.05*samplerate]==2400
    c50_nenner         = np.max(master_of_integration(int(data.size), int(0.05*samplerate), data))
#    print("C50_nenner: \t\t", c50_nenner/samplerate)
###     ausrechnen
    print("C50: \t\t\t\t\t\t", np.round(10 * np.log10(c50_zaehler/c50_nenner), 2), " dB")

###     C80 berechnen
###      0 bis 80ms         ->  data[0.08*samplerate]==3840 bis data[0]==0
    c80_zaehler        = np.max(master_of_integration(int(0.08*samplerate), 0, data))
#    print("C80_zaehler: \t\t", c80_zaehler/samplerate)
###    80ms bis inf         -> data[data.size]==65631  bis data[0.08*samplerate]==3840
    c80_nenner         = np.max(master_of_integration(int(data.size), int(0.08*samplerate), data))
#    print("C80_nenner: \t\t", c80_nenner/samplerate)
###     ausrechnen
    print("C80: \t\t\t\t\t\t", np.round(10 * np.log10(c80_zaehler/c80_nenner), 2), " dB")
        
    
###     MAIN    
main()