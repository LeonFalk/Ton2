# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 16:16:33 2021
Revised on Mon Jun 21

@author: E_Wilk
------------------------------------
"Tontechnik 2", Winter 2021
Prof. Dr. Eva Wilk

Kompressor und Limiter

Vorlage für Praxisproblem 5

------------------------------------
Quellen: 
    Zölzer, DAFX, S. 109 ff
    Mathworks, https://de.mathworks.com/help/audio/ref/limiter-system-object.html 

Threshold	[–50, 0]	linear	dB
KneeWidth	[0, 20]	linear	dB
AttackTime	[0, 4]	linear	seconds
ReleaseTime	[0, 4]	linear	seconds
MakeUpGain (available when you set MakeUpGainMode 
to 'Property')	[–10, 24]	linear	dB
"""

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import time

from scipy.io.wavfile import write
from scipy.io.wavfile import read

    ### Sinus Generator
def singenerator(Fs):
    duration = 1
    samples = duration * Fs
    
    o = np.arange(0, samples)
    t = o / Fs
    
    sinus = 1 * np.sin(2 * np.pi * 1000 * t)
    
    return sinus


def FFT(x, Fs):
    fft_spectrum = np.fft.rfft(x)
    freq = np.fft.rfftfreq(x.size, d=1./Fs)
        
    fft_spectrum_abs = np.abs(fft_spectrum)
    
    
    
    return fft_spectrum_abs

def klirrfaktor_berechnen(title, fft_spectrum):
###     Klirrfaktor berechnen
    sortierung = np.argsort(fft_spectrum)
    
    Gesamtenergie = 0
    Oberschwingung = 0
    Grundschwingung = 0
    
    for n in range (-1, -6, -1):
        
        #print('Schwingung ', n*-1, ': ', sortierung[n], 'Hz, Amplitude: ', fft_spectrum[sortierung[n]])
        Gesamtenergie += fft_spectrum[sortierung[n]]
        if n == -1:
            Grundschwingung += np.square(fft_spectrum[sortierung[n]])
        elif n < -1:
            Oberschwingung += np.square(fft_spectrum[sortierung[n]])
    
    klirrfaktor = 100 * np.sqrt((Oberschwingung/(Grundschwingung + Oberschwingung)))
    
        
    #print('\nGesamtenergie des Systems ', title, ':\t', np.round(Gesamtenergie, 3))
    print('Klirrfaktor des Systems:',np.round(klirrfaktor, 3),'%')
    

def scheitelwert(y_a):

    global y_eff
    
    print('\n\t')
    print('Limiter Einstellungen')
    print('Attack:',tAT)
    print('Release:',tRT)
    print('Threshold:',L_thresh)
    print('\n\t')
    
    y_eff = np.sqrt(np.mean(x ** 2))                        # RMS / Effektivwert berechnen
    print("Der Effektivwert vor dem Limiter beträgt:\n\t",round(y_eff,3))           # RMS / Effektivwert ausgeben

    y_crest = np.max(x) / y_eff                             # Scheitelfaktor berechnen
    print("Der Crestfaktor vor dem Limiter beträgt:\n\t",round(y_crest,3))          # Scheitelfaktor ausgeben

    y_eff = np.sqrt(np.mean(y_a ** 2))                        # RMS / Effektivwert berechnen
    print("Der Effektivwert nach dem Limiter beträgt:\n\t", round(y_eff,3))           # RMS / Effektivwert ausgeben

    y_crest = np.max(y_a) / y_eff                             # Scheitelfaktor berechnen
    print("Der Crestfaktor nach dem Limiter beträgt:\n\t", round(y_crest,3))          # Scheitelfaktor ausgeben




## Schalter für Dynamikverhalten: 
dynamik = 1 #0  # Alternative: dynamik = 0
softknee = 0

####################################
Fs = 44100                      #Abtastrate für Sinus auskommentieren bei Testsignalen !
x = singenerator(Fs)            #Sinus Signal, bei Klirrfaktor Berechnung aktivieren !
#Fs,x= read("Testsignal_1.wav") # Zur Auswahl Testsignal_1 (Aufgabe 2) und Testsignal_2 (Aufgabe 3), Bitte zur Berechnung des Klirrfaktors auskommentieren!
dauer = x.size
dauer_s = x.size/Fs
deltat = 1./(Fs)  #Zeit-Schritt, float
t=np.arange(x.size)/float(Fs)

#umwandeln in float und normieren
x = np.array( x, dtype=np.float64)
x= x/np.abs(np.max(x))   # Normierung, falls erforderlich/gewünscht


### Kompressor-Parameter, Umrechnen in Abtastwerte
tAT = 0.006 # 0.003 # Attack-Time, tAT = 0.02 .. 10 ms nach Zoelzer
tRT = 0.02   #1 # Release-Time, tRT = 1 .. 5000 ms nach Zoelzer

tAT_i = tAT*Fs
tRT_i = tRT*Fs

faktor = np.log10(9)
a_R = np.e **(-faktor/(tAT_i))
a_T = np.e **(-faktor/(tRT_i))

# M = 0     # Make-Up Gain


##Threshold:
x_ref = np.abs(np.max(x))  #falls nicht normiert wurde
L_thresh = -6  # -50 .. 0, in dB. bei - 3 ist statisch gut zu sehen
u_thresh = 10**(L_thresh/20)*x_ref

L_M = -1.0*L_thresh -5    # Make-Up Gain, 
L_M = 0   ## L_M wird momentan nicht verwendet



# Vorbereitung für Softknee:
if softknee:
    KneeWidth = 0 # 0 .. 20, in dB


##################
## Kompressor:
PegelMin = -95   # Pegelgrenze nach unten

# Eingangssingal als Pegel:
Lx = np.zeros(dauer)      
Lx[1:] = 20*np.log10(np.abs(x[1:])/x_ref)    
Lx[0] = Lx[1]             # damit nicht log(0)
# Begrenzung des minimalen Pegels (mathematisch erforderlich)
for i in range(dauer):
    if Lx[i] < PegelMin:
        Lx[i] = PegelMin

# Vorbereitung der arrays:
Lx_c = np.zeros(dauer)      # Pegel(x) nach statischer Kompressor-Kennlinie
Lg_c = np.zeros(dauer)      # Pegel(gain) statisch (um wieviel wurde Lx gedämpft) 
Lg_s = np.zeros(dauer)       # Pegel(gain) dynamisch (smoothed, mit t_attack und t_release)
Lg_M = np.zeros(dauer)       # Pegel(gain) dynamisch (smoothed, mit t_attack und t_release) mit M
g_a = np.zeros(dauer)       # linearer gain dynamisch (smoothed, mit t_attack und t_release)

# Berechnung der momentanen Verstärkung/Dämpfung
for i in range(dauer):
    if softknee == 0:        # --> hard knee; Soft-Knee ist nicht implementiert
        if Lx[i] >= L_thresh:
            Lx_c[i] = L_thresh
        else:
            Lx_c[i] = Lx[i]
    #else:            # Softknee
       # Lx[i] = Lx[i]      # dummy-code, noch ändern    
    
    Lg_c[i] = Lx_c[i] - Lx[i]   # Dämpfung von Lx zum Zeitpunkt i 
    
# dynamische Kennlinie
    Lg_s[0] = 0.0 #20*np.log10(x[0]/x_ref) #!!! Startwert für dynamische Dämpfung
    if dynamik == 1:
        if i > 0:
            if Lg_c[i] > Lg_s[i-1]:     # Release
                Lg_s[i] = a_T*Lg_s[i-1]+ (1-a_T)*Lg_c[i] 
               # print("Release")
            else:                       # Attack
                Lg_s[i] = a_R*Lg_s[i-1]+ (1-a_R)*Lg_c[i]
                #print("Attack")
    else:
        Lg_s[i] = Lx_c[i]
 
# Anwenden der momentanen Verstärkung/Dämpfung
if dynamik == 1:
   Lg_M = Lg_s #+ L_M      # z.Zt. ohne makeup-gain  

   g_a = 10**(Lg_M/20)   #lineare Verstärkung, zeitabhängig   
   y_a = x * g_a             # Ausgangssignal; hier ist das Vorzeichen im x vorhanden
else:
   g_mu = 10**(L_M/20)     # verstärkung ergibt sich aus makeup-gain
   y_a = 10**(Lx_c/20)*x_ref * g_mu     # y ist geclippter Eingang  

   for i in range (dauer):  # Vorzeichen ist verloren durch log, daher hinzufügen
        if x[i] < 0:
            y_a[i] = -y_a[i]


scheitelwert(y_a)           # Ausgabe des Effektivwertes und Crest Faktor vor und nach dem Limiter

fft_spectrum = FFT(y_a, Fs)
klirrfaktor_berechnen("nach dem Limiter",fft_spectrum)      #Ausgabe Klirrfaktor 



"""
#nur testweise: Verstärkung feststellen
verst = np.max(Lx) - np.max(Lx_c)
y_v = y_a*10**(verst/20)
"""

###     Sound-Ausgabe

sd.play(y_a, Fs)                # Sound Ausgabe für die Tonsignale und den Sinus (Klirrfaktor)
sekunden = y_a.size/Fs

###################################
# Plots:
fig, ax = plt.subplots()   
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=0.5)  #Abstand zwischen Subplots

ax.plot(t,y_a)  # Plotten von y über t
ax.plot(t,g_a)  # Plotten von gain über t

# Einrichtung der Achsen:
ax.set_xlim(0, 0.04)#dauer/Fs)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel('$t$ in s')
ax.set_ylabel('$y$($t$),$g$($t$) ')
ax.grid(True)
plt.show()


