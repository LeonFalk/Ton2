#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PRAXISPROBLEM 2

Platzieren von Mono-Schallquellen innerhalb der Stereobasis bzw. in einer
Stereo-Datei.
"""

__author__ = 'Paul Hofmann'
__created__ = '11.01.21'

import numpy as np
from scipy.io.wavfile import read, write
import sounddevice as sd
from time import sleep

"""
Einlesen der Testsignale
"""

audiofile1 = "s_sinus.wav"
audiofile2 = "s_pluck.wav"

fs, data1 = read(audiofile1)
fs, data2 = read(audiofile2)
data1 = np.array(data1)
data2 = np.array(data2)

"""
Laufzeitdifferenz
"""

def pan_laufzeit(signal, richtung, laufzeitdifferenz):
    
    data_l = signal[:,0]
    data_r = signal[:,1]
    
    laufzeitdifferenz = int(laufzeitdifferenz * fs)
    
    if (richtung == "links"):
        data_r = np.insert(data_r, 0, np.zeros(laufzeitdifferenz))
        data_r = np.delete(data_r, np.arange(data_r.size - laufzeitdifferenz, data_r.size))
    elif (richtung == "rechts"):
        data_l = np.insert(data_l, 0, np.zeros(laufzeitdifferenz))
        data_l = np.delete(data_l, np.arange(data_l.size - laufzeitdifferenz, data_l.size))
    
    stereo = np.column_stack((data_l, data_r))
    stereo *= int(32767 / np.max(np.abs(stereo)))
    stereo = stereo.astype(np.int16)
    
    return stereo

"""
Pegeldifferenz
"""

def pan_pegel(signal, richtung, pegeldifferenz):
    
    data_l = signal[:,0]
    data_r = signal[:,1]
    
    pegeldifferenz  = np.max(np.abs(signal)) / np.exp(pegeldifferenz/20)
    pegeldifferenz  = pegeldifferenz / np.max(np.abs(signal))
    
    if (richtung == "links"):
        data_r = data_r.astype(np.float32)
        data_r *= pegeldifferenz
        data_r = data_r.astype(np.int16)
    elif (richtung == "rechts"):
        data_l = data_l.astype(np.float32)
        data_l *= pegeldifferenz
        data_l = data_l.astype(np.int16)
    
    stereo = np.column_stack((data_l, data_r))
    stereo *= int(32767 / np.max(np.abs(stereo)))
    stereo = stereo.astype(np.int16)
    
    return stereo

"""
Wandernde Schallquelle
"""

def pan_lfo(signal, lfo_f, lfo_a):
    
    t = np.arange(0, len(signal)/fs, 1./fs)
    lfo = lfo_a * np.sin(2 * np.pi * lfo_f * t)
    lfo = lfo.astype(np.float32)
    
    data_l = signal[:,0]
    data_r = signal[:,1]
    data_l = data_l.astype(np.float32)
    data_r = data_r.astype(np.float32)
    
    for i in range(len(signal)):
        data_l[i] *= ((1 + lfo[i]) / 2)
        data_r[i] *= ((1 - lfo[i]) / 2)
    
    stereo = np.column_stack((data_l, data_r))
    stereo *= int(32767 / np.max(np.abs(stereo)))
    stereo = stereo.astype(np.int16)
    
    return stereo

"""
Signale bearbeiten
"""

# Werte für Laufzeitdifferenzen (in s)
laufzeit_25  = 0.00014
laufzeit_50  = 0.00027
laufzeit_100 = 0.00082

# Werte für Pegeldifferenzen (in dB)
pegel_25  = 3.5
pegel_50  = 7.0
pegel_100 = 18.0

# Signal 1
stereo1 = pan_laufzeit(data1, "links", laufzeit_25)
stereo2 = pan_laufzeit(data1, "links", laufzeit_50)
stereo3 = pan_laufzeit(data1, "links", laufzeit_100)
stereo4 = pan_pegel(data1, "links", pegel_25)
stereo5 = pan_pegel(data1, "links", pegel_50)
stereo6 = pan_pegel(data1, "links", pegel_100)

# Signal 2
stereo7 = pan_laufzeit(data2, "links", laufzeit_25)
stereo8 = pan_laufzeit(data2, "links", laufzeit_50)
stereo9 = pan_laufzeit(data2, "links", laufzeit_100)
stereo10 = pan_pegel(data2, "links", pegel_25)
stereo11 = pan_pegel(data2, "links", pegel_50)
stereo12 = pan_pegel(data2, "links", pegel_100)

# Summenlokalisation
stereo13 = pan_laufzeit(data2, "rechts", laufzeit_50)
stereo14 = pan_laufzeit(stereo11, "rechts", laufzeit_50)

# Laufzeitunterschied Signal 2: Trennung in zwei Einzelsignale ab 20 ms
stereo15 = pan_laufzeit(data2, "links", 0.02)

# Wandernde Schallquelle Signal 1
stereo16 = pan_lfo(data1, 1.0, 1.0)

"""
Audiosignale abspielen
"""

p = 1       # Pause in Sekunden

print()
print("Audiosignale werden abgespielt:")
print()

# Testsignal 1

sleep(p)
print("Signal 1: " + audiofile1)
print()
print(" - Laufzeitunterschied Mitte...")
sleep(p/2)
sd.play(data1, fs)
sleep((len(data1) / fs) + p)
print(" - Laufzeitunterschied 25% links...")
sleep(p/2)
sd.play(stereo1, fs)
sleep((len(stereo1) / fs) + p)
print(" - Laufzeitunterschied 50% links...")
sleep(p/2)
sd.play(stereo2, fs)
sleep((len(stereo2) / fs) + p)
print(" - Laufzeitunterschied 100% links...")
sleep(p)
sd.play(stereo3, fs)
sleep((len(stereo3) / fs) + p)
print()
print(" - Pegelunterschied Mitte...")
sleep(p/2)
sd.play(data1, fs)
sleep((len(data1) / fs) + p)
print(" - Pegelunterschied 25% links...")
sleep(p/2)
sd.play(stereo4, fs)
sleep((len(stereo4) / fs) + p)
print(" - Pegelunterschied 50% links...")
sleep(p/2)
sd.play(stereo5, fs)
sleep((len(stereo5) / fs) + p)
print(" - Pegelunterschied 100% links...")
sleep(p/2)
sd.play(stereo6, fs)
sleep((len(stereo6) / fs) + p)

# Testsignal 2

sleep(p/2)
print()
print("Signal 2: " + audiofile2)
print()
print(" - Laufzeitunterschied Mitte...")
sleep(p/2)
sd.play(data2, fs)
sleep((len(data2) / fs) + p)
print(" - Laufzeitunterschied 25% links...")
sleep(p/2)
sd.play(stereo7, fs)
sleep((len(stereo7) / fs) + p)
print(" - Laufzeitunterschied 50% links...")
sleep(p/2)
sd.play(stereo8, fs)
sleep((len(stereo8) / fs) + p)
print(" - Laufzeitunterschied 100% links...")
sleep(p/2)
sd.play(stereo9, fs)
sleep((len(stereo9) / fs) + p)
print()
print(" - Pegelunterschied Mitte...")
sleep(p/2)
sd.play(data2, fs)
sleep((len(data2) / fs) + p)
print(" - Pegelunterschied 25% links...")
sleep(p/2)
sd.play(stereo10, fs)
sleep((len(stereo10) / fs) + p)
print(" - Pegelunterschied 50% links...")
sleep(p/2)
sd.play(stereo11, fs)
sleep((len(stereo11) / fs) + p)
print(" - Pegelunterschied 100% links...")
sleep(p/2)
sd.play(stereo12, fs)
sleep((len(stereo12) / fs) + p)

# Summenlokalisation

print()
print("Summenlokalisation, mit Testsignal 2:")
print()
sleep(p/2)
print(" - Pegelunterschied 50% links...")
sleep(p/2)
sd.play(stereo11, fs)
sleep((len(stereo11) / fs) + p)
print(" - Laufzeitunterschied 50% rechts...")
sleep(p/2)
sd.play(stereo13, fs)
sleep((len(stereo13) / fs) + p)
print(" - zusammen...")
sleep(p/2)
sd.play(stereo14, fs)
sleep((len(stereo14) / fs) + p)

print()
print("Laufzeitdifferenz:")
print(" - Aufteilung in Einzelsignale bei 20 ms...")
sleep(p/2)
sd.play(stereo15, fs)
sleep((len(stereo15) / fs) + p)

print()
print("Wandernde Schallquelle:")
print(" - Testsignal 1 mit zeitabhängiger Pegeldifferenz")
sleep(p/2)
sd.play(stereo16, fs)
sleep((len(stereo16) / fs) + p)

write("t_sinus_l_25.wav", fs, stereo1)
write("t_sinus_l_50.wav", fs, stereo2)
write("t_sinus_l_100.wav", fs, stereo3)
write("t_sinus_p_25.wav", fs, stereo4)
write("t_sinus_p_50.wav", fs, stereo5)
write("t_sinus_p_100.wav", fs, stereo6)
write("t_pluck_l_25.wav", fs, stereo7)
write("t_pluck_l_50.wav", fs, stereo8)
write("t_pluck_l_100.wav", fs, stereo9)
write("t_pluck_p_25.wav", fs, stereo10)
write("t_pluck_p_50.wav", fs, stereo11)
write("t_pluck_p_100.wav", fs, stereo12)
write("t_pluck_summe.wav", fs, stereo14)
write("t_pluck_getrennt.wav", fs, stereo15)
write("t_sinus_lfo.wav", fs, stereo16)