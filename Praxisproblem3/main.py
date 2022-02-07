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
###import soundfile as sf
import time
import math
def ausgabe(samplerate, array, s_or_hz):
    ###print(array)
    
    if s_or_hz == 's':
        x = np.linspace(0., array.size/samplerate, array.size)
        plt.xlabel("Zeit, s")
        plt.ylabel("Amplitude, units")
        ###     Sound-Ausgabe
        #sd.play(array, samplerate)
        #sf.write('name.flac', array, samplerate)
        #sekunden = array.size/samplerate
        #time.sleep(sekunden)
        
    elif s_or_hz == 'hz':
        x = samplerate
        plt.xlabel("frequency, Hz")
        plt.ylabel("Amplitude, units")
        
    ###     Plot ausgeben
    plt.plot(x, array)
    plt.show()


    
    ### Sinus Generator
def singenerator(samplerate):
    duration = 1
    samples = duration * samplerate
    
    
    x = np.arange(0, samples)
    t = x / samplerate
    
    
    sinus_testsignal = 1 * np.sin(2 * np.pi * 2000 * t)
    return sinus_testsignal


def main():
    ### Testsignal auswerten und einlesen
    
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
        data_b = singenerator(samplerate)
    
    plt.title('Unverfälschtes Signal')
    ausgabe(samplerate, data, 's')
    
    
    fft_spectrum = np.fft.rfft(data)
    freq = np.fft.rfftfreq(data.size, d=1./samplerate)
        
    fft_spectrum_abs = np.abs(fft_spectrum)
    
    plt.title('Unverfälschtes Signal Spektrum')
    ausgabe(freq, fft_spectrum_abs, 'hz')
    
    
    ### Bearbeiten mit Kennlinie
    for i in range(data.size):
        data[i] = -0.5/np.tan(data[i] + np.pi / 2)

    plt.title('Bearbeitetes Signal System A')
    ausgabe(samplerate, data, 's')     
    
    
    fft_spectrum = np.fft.rfft(data)
    freq = np.fft.rfftfreq(data.size, d=1./samplerate)
    
    fft_spectrum_abs = np.abs(fft_spectrum)

    plt.title('Bearbeitetes Signal Spektrum System A')
    ausgabe(freq, fft_spectrum_abs, 'hz')
    
    
    testarray = []
    for i in range(fft_spectrum_abs.size):
        if fft_spectrum_abs[i] > 1:
            testarray.append(fft_spectrum_abs[i])
        else:
            pass
        
    ### Klirrfaktor
    testarray_square = np.square(testarray)
    klirrfaktor = math.sqrt((testarray_square[1]+testarray_square[2])/(testarray_square[0]+testarray_square[1]+testarray_square[2]))*100
    print()
    print('Klirrfaktor System A')
    print(round(klirrfaktor),'%')
    
    ### System B 
    VarC = 0.5
    VarCn = -0.5
    for i in range(data_b.size):
        if data_b[i] >= VarC:
            data_b[i] = VarC
        
        elif data_b[i] <= VarCn:
            data_b[i] = VarCn
    
    else:
        pass
    plt.title('Bearbeitetes Signal System B')
    ausgabe(samplerate, data_b, 's')

    
    fft_spectrum_b = np.fft.rfft(data_b)
    freq_b = np.fft.rfftfreq(data_b.size, d=1./samplerate)
    
    fft_spectrum_abs_b = np.abs(fft_spectrum_b)

    plt.title('Bearbeitetes Signal Spektrum System B')
    ausgabe(freq_b, fft_spectrum_abs_b, 'hz')
    
    testarray = []
    testarray_square = []
    
    for i in range(fft_spectrum_abs_b.size):
        if fft_spectrum_abs_b[i] > 1:
            testarray.append(fft_spectrum_abs_b[i])
        else:
            pass 
    testarray_square = np.square(testarray)
    klirrfaktor = math.sqrt((testarray_square[1]+testarray_square[2])/(testarray_square[0]+testarray_square[1]+testarray_square[2]))*100
    print('Klirrfaktor System B')
    print(round(klirrfaktor),'%')
    print(testarray)
    
    
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