# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 14:28:06 2022

@author: Leon, Vanessa, Max, Jakob

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
import time
import math

    ### Sinus Generator
def singenerator(samplerate):
    duration = 1
    samples = duration * samplerate
    
    x = np.arange(0, samples)
    t = x / samplerate
    
    sinus = 1 * np.sin(2 * np.pi * 2000 * t)
    return sinus

def ausgabe(title, samplerate, array, s_or_hz):
    ###print(array)
    
    if s_or_hz == 's':
        x = np.linspace(0., array.size/samplerate, array.size)
        plt.xlabel("Zeit, s")
        plt.ylabel("Amplitude, units")
        
        ###     Sound-Ausgabe zum testen bzw. speichern der veränderten Datei
        #sd.play(array, samplerate)
        #sf.write('name.flac', array, samplerate)
        #sekunden = array.size/samplerate
        #time.sleep(sekunden)
        
    elif s_or_hz == 'hz':
        x = samplerate
        plt.xlabel("frequency, Hz")
        plt.ylabel("Amplitude, units")
        
    ###     Plot ausgeben
    plt.title(title)
    plt.plot(x, array)
    plt.show()

def FFT(data, samplerate):
    fft_spectrum = np.fft.rfft(data)
    freq = np.fft.rfftfreq(data.size, d=1./samplerate)
        
    fft_spectrum_abs = np.abs(fft_spectrum)
    
    ausgabe('Signal: Frequenzspektrum', freq, fft_spectrum_abs, 'hz')
    
    return fft_spectrum_abs

def klirrfaktor_berechnen(title, fft_spectrum):
###     Filtern von Werten < 1 aus dem Spektrum
    fft_spectrum_filtered = []
    for i in range(fft_spectrum.size):
        if fft_spectrum[i] > 1:
            fft_spectrum_filtered.append(fft_spectrum[i])
        else:
            pass
            
###     Klirrfaktor berechnen
    fft_spectrum_square = np.square(fft_spectrum_filtered)
    klirrfaktor = math.sqrt((fft_spectrum_square[1]+fft_spectrum_square[2])/(fft_spectrum_square[0]+fft_spectrum_square[1]+fft_spectrum_square[2]))*100

    print('\nKlirrfaktor des Systems ', title,':\t',  round(klirrfaktor),'%')



###############################################################################

def main():
    ### Testsignal einlesen
    testsignal = input("Wollen Sie Testsignal 1, 2 oder 3(Sinus) auswerten?\n")
    
    if testsignal   == '1':
        testsignal  = 'testsignal1.wav'
        samplerate, data    = wavfile.read(testsignal)
        
        if data.ndim == 2:
            y_L = data[:, 0]
            y_R = data[:, 1]
            data = (y_L + y_R) /2
        data = data / samplerate
        
    elif testsignal == '2':
        testsignal  = 'testsignal2.wav'
        samplerate, data    = wavfile.read(testsignal)
        
        if data.ndim == 2:
            y_L = data[:, 0]
            y_R = data[:, 1]
            data = (y_L + y_R) /2
        data = data / samplerate
        
    elif testsignal == '3':
        samplerate = 48000
        data = singenerator(samplerate)
    else:
        print("Fehleingabe. Das Programm wird nun beendet.")
    
    ausgabe('Ausgangs-Signal', samplerate, data, 's')
    
###     FFT
    fft_spectrum = FFT(data, samplerate)
  
###     Bearbeiten mit Kennlinie
    data_bearbeitet_a = np.array(data)
    for i in range(data.size):
        data_bearbeitet_a[i] = -0.5/np.tan(data[i] + np.pi / 2)

    ausgabe('Bearbeitetes-Signal: System A', samplerate, data_bearbeitet_a, 's')     
    
###     FFT-Spektrum
    fft_spectrum = FFT(data_bearbeitet_a, samplerate)
    
###     Klirrfaktor berechnene
    klirrfaktor_berechnen('A', fft_spectrum)



###     System B anwenden       ###############################################
    VarC = 0.5
    VarCn = -0.5
    
    data_bearbeitet_b = np.array(data)
    for i in range(data.size):
        if data[i] >= VarC:
            data_bearbeitet_b[i] = VarC
        
        elif data[i] <= VarCn:
            data_bearbeitet_b[i] = VarCn
    
    else:
        pass
    
    ausgabe('Bearbeitetes-Signal: System B', samplerate, data_bearbeitet_b, 's')

###     FFT-Spektrum
    fft_spectrum_b = FFT(data_bearbeitet_b, samplerate)
    
###     Klirrfaktor berechnen
    klirrfaktor_berechnen('B', fft_spectrum_b)
        
    
    
###     Main        ###########################################################
main()