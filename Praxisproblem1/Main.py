# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:58:02 2021

@author: Leon
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

samplerate, data = wavfile.read('Datei_1.wav')
y = 0

#Ausgabe der Array-Länge, Samplerate und dem Array
print(data.size, samplerate, data)

array_integr = np.zeros((data.size))

for i in range(-1, (data.size)*-1, -1):
     y = y + np.square(data[i])             #-> diese ist richtig, da sie nur die neuen Daten quadriert
     array_integr[i] = y

#   rausrechnen der Samplerate -> Normierung...
array_integr = array_integr/samplerate

array_log_integr = np.zeros(data.size)
array_log_integr = 10 * (np.log10(array_integr) - np.log10(np.max(array_integr)))   #-> Dezibel

#Anzeige in Sekunden fehlt noch -> der Plot sollte noch angepasst werden und beides anzeigen + die x-Achse angepasst werden und beide Beschriftet werden
#   Energieabfall
#plt.plot(array_integr)
#   Energieabfall Logarithmiert [Dezibel]
plt.plot(array_log_integr)
plt.show()

