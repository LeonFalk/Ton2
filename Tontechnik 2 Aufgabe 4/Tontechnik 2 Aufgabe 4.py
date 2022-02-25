# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:59:06 2022

@author: Leon, Vanessa, Max, Jakob
"""

import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read, write
from scipy import signal
from time import perf_counter, sleep

#Einlesen der Audiosignale

Datei1 = "Ton Aufgabe 1.wav"

Datei2 = "H13azi_0,0_ele_0,0.wav"
Datei3 = "H13azi_45,0_ele_0,0.wav"
Datei4 = "H13azi_90,0_ele_0,0.wav"
Datei5 = "H13azi_135,0_ele_0,0.wav"
Datei6 = "H13azi_180,0_ele_0,0.wav"
Datei7 = "H13azi_225,0_ele_0,0.wav"
Datei8 = "H13azi_270,0_ele_0,0.wav"
Datei9 = "H13azi_315,0_ele_0,0.wav"

samplerate, x_t = read(Datei1)
samplerate, h_t1 = read(Datei2)
samplerate, h_t2 = read(Datei3)
samplerate, h_t3 = read(Datei4)
samplerate, h_t4 = read(Datei5)
samplerate, h_t5 = read(Datei6)
samplerate, h_t6 = read(Datei7)
samplerate, h_t7 = read(Datei8)
samplerate, h_t8 = read(Datei9)

x_t = np.array(x_t)
h_t1 = np.array(h_t1)
h_t2 = np.array(h_t2)
h_t3 = np.array(h_t3)
h_t4 = np.array(h_t4)
h_t5 = np.array(h_t5)
h_t6 = np.array(h_t6)
h_t7 = np.array(h_t7)
h_t8 = np.array(h_t8)

# Faltungshall im Zeitbereich 

def Faltungshall(x_t, h_t):
    
    x_t = x_t/np.max(abs(x_t))
    h_t = h_t/np.max(abs(h_t))
    
    # Ausgangssignal
    h_tr = h_t[:,0]
    h_tl = h_t[:,1]
    
    y_tr = signal.convolve(x_t, h_tr, method = "auto")
    y_tl = signal.convolve(x_t, h_tl, method = "auto")
    
    y_t = np.column_stack((y_tr, y_tl))
    
    return y_t

# Faltungshall im Frequenzbereich

def Frequenzhall(x_t, h_t):
    
    x_t = x_t/np.max(abs(x_t))
    h_tn = h_t/np.max(abs(h_t))
    h_tr = h_tn[:,0]
    h_tl = h_tn[:,1]
    
    # Verlängern der Impulsantwort (x_t und h_t benötigen gleiche Längen)
    dt = len(x_t) - len(h_tn)
    zeros = np.zeros(dt)
    h_tr = np.append(h_tr, zeros)
    h_tl = np.append(h_tl, zeros)
    
    # Ausgangssignal aus Rechnung über Frequenzgänge
    X_f = np.fft.rfft(x_t)
    H_fr = np.fft.rfft(h_tr)
    H_fl = np.fft.rfft(h_tl)
    
    Y_fl = X_f * H_fl
    Y_fr = X_f * H_fr
    y_tl = np.fft.irfft(Y_fl)
    y_tr = np.fft.irfft(Y_fr)
    
    y_t = np.column_stack((y_tr, y_tl))
    
    return y_t

"""
Bewegung der Schallquelle um den Kopf mit Methode A.
"""

def Wandernder_Hall (x_t):
    
    y1_t = Faltungshall(x_t, h_t1) #0
    y1_tr = y1_t[:,0]
    y1_tl = y1_t[:,1]
    y2_t = Faltungshall(x_t, h_t2) #45
    y2_tr = y2_t[:,0]
    y2_tl = y2_t[:,1]
    y3_t = Faltungshall(x_t, h_t3) #90
    y3_tr = y3_t[:,0]
    y3_tl = y3_t[:,1]
    y4_t = Faltungshall(x_t, h_t4) #135
    y4_tr = y4_t[:,0]
    y4_tl = y4_t[:,1]
    y5_t = Faltungshall(x_t, h_t5) #180
    y5_tr = y5_t[:,0]
    y5_tl = y5_t[:,1]
    y6_t = Faltungshall(x_t, h_t6) #225
    y6_tr = y6_t[:,0]
    y6_tl = y6_t[:,1]
    y7_t = Faltungshall(x_t, h_t7) #270
    y7_tr = y7_t[:,0]
    y7_tl = y7_t[:,1]
    y8_t = Faltungshall(x_t, h_t8) #315
    y8_tr = y8_t[:,0]
    y8_tl = y8_t[:,1]
    
    # Amplitudenwerte werden zwischen den gegebenen 45° Abständen interpoliert
    y_tr = np.zeros(len(x_t))
    y_tl = np.zeros(len(x_t))
    for i in range(0, len(x_t)-1, 1):
        a = (i/len(x_t))*360
        if (a < 45):
            y_tr[i] = y1_tr[i]*(1-(a/45)) + y2_tr[i]*(a/45)
            y_tl[i] = y1_tl[i]*(1-(a/45)) + y2_tl[i]*(a/45)
        elif (a < 90):
            a -= 45
            y_tr[i] = y2_tr[i]*(1-(a/45)) + y3_tr[i]*(a/45)
            y_tl[i] = y2_tl[i]*(1-(a/45)) + y3_tl[i]*(a/45)
        elif (a < 135):
            a -= 90
            y_tr[i] = y3_tr[i]*(1-(a/45)) + y4_tr[i]*(a/45)
            y_tl[i] = y3_tl[i]*(1-(a/45)) + y4_tl[i]*(a/45)
        elif (a < 180):
            a -= 135
            y_tr[i] = y4_tr[i]*(1-(a/45)) + y5_tr[i]*(a/45)
            y_tl[i] = y4_tl[i]*(1-(a/45)) + y5_tl[i]*(a/45)
        elif (a < 225):
            a -= 180
            y_tr[i] = y5_tr[i]*(1-(a/45)) + y6_tr[i]*(a/45)
            y_tl[i] = y5_tl[i]*(1-(a/45)) + y6_tl[i]*(a/45)
        elif (a < 270):
            a -= 225
            y_tr[i] = y6_tr[i]*(1-(a/45)) + y7_tr[i]*(a/45)
            y_tl[i] = y6_tl[i]*(1-(a/45)) + y7_tl[i]*(a/45)
        elif (a < 315):
            a -= 270
            y_tr[i] = y7_tr[i]*(1-(a/45)) + y8_tr[i]*(a/45)
            y_tl[i] = y7_tl[i]*(1-(a/45)) + y8_tl[i]*(a/45)
        elif (a <= 360):
            a -= 315
            y_tr[i] = y8_tr[i]*(1-(a/45)) + y1_tr[i]*(a/45)
            y_tl[i] = y8_tl[i]*(1-(a/45)) + y1_tl[i]*(a/45)
    
    y_t = np.column_stack((y_tr, y_tl))
    
    return y_t

"""
Bearbeitung der Töne
"""

# A.
zeit1  = perf_counter()
y_t1   = Faltungshall(x_t, h_t1)
zeit2  = perf_counter()
dauer1 = zeit2 - zeit1 # Berechnungszeit A.

# B.
zeit1  = perf_counter()
y_t2 = Frequenzhall(x_t, h_t1)
zeit2  = perf_counter()
dauer2 = zeit2 - zeit1 # Berechnungszeit B.

# wandernd
y_t3 = Wandernder_Hall(x_t)

"""
Plot der bearbeiteten Töne
"""

fig, ax0 = plt.subplots(2)

t_x = np.arange(len(x_t)) / float(samplerate)
t_y1 = np.arange(len(y_t1)) / float(samplerate)

# Plot Eingangssignal
ax0[0].plot(t_x, (x_t/np.max(abs(x_t))))    
ax0[0].set_title("Amplitude")
ax0[0].set_xlabel('t in s')
ax0[0].set_ylabel('x(t)')
ax0[0].set_xlim([0., 5.])

# Plot Ausgangssignal A.
ax0[1].plot(t_y1, y_t1)    
ax0[1].set_title("")
ax0[1].set_xlabel('t in s')
ax0[1].set_ylabel('y(t) [A.]')
ax0[1].set_xlim([0., 5.])

plt.show()

fig, ax1 = plt.subplots(2)

t_y2 = np.arange(len(y_t2)) / float(samplerate)

# Plot Eingangssignal
ax1[0].plot(t_x, (x_t/np.max(abs(x_t))))    
ax1[0].set_title("Amplitude")
ax1[0].set_xlabel('t in s')
ax1[0].set_ylabel('x(t)')
ax1[0].set_xlim([0., 5.])

# Plot Ausgangssignal B.
ax1[1].plot(t_y2, y_t2)    
ax1[1].set_title("")
ax1[1].set_xlabel('t in s')
ax1[1].set_ylabel('y(t) [B.]')
ax1[1].set_xlim([0., 5.])

plt.show()

fig, ax2 = plt.subplots(1)

t_y3 = np.arange(len(y_t3)) / float(samplerate)

# Plot Ausgangssignal wandernd
ax2.plot(t_y3, y_t3)    
ax2.set_title("")
ax2.set_xlabel('t in s')
ax2.set_ylabel('y(t) [wandernd]')
ax2.set_xlim([0., 5.])

plt.show()

"""
Töne abspielen
"""

p = 1       # Pause in s


# TestsignalTon aus Aufgabe 1.
print("Unbearbeiteter Ton aus Aufgabe 1")
sd.play(x_t, samplerate)
sleep((len(x_t) / samplerate) + p)

# Ton mit Hall A.
print("Ton mit Faltungshall. (Berechnungsdauer = " + str(dauer1) + "s)")
sd.play(y_t1, samplerate)
sleep((len(y_t1) / samplerate) + p)

# Ton mit Hall B.
print("Ton mit Frequenzhall (Berechnungsdauer = " + str(dauer2) + "s)")
sd.play(y_t2, samplerate)
sleep((len(y_t2) / samplerate) + p)

# Ton wandernd
print("Ton mit wanderndem Hall.")
sd.play(y_t3, samplerate)
# sleep((len(y_t3) / fs) + p)

write("Ton_Aufgabe_1_A.wav", samplerate, y_t1)
write("Ton_Aufgabe_1_B.wav", samplerate, y_t2)
write("Ton_Aufgabe_1_C.wav", samplerate, y_t3)