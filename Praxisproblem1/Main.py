# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:58:02 2021

@author: Leon
"""

'''
Probleme:
    inhaltliches Verständnis
    stimmt unsere Logarithmierung und Normierung?
    wie macht man das mit dem Dezibel Abfall?
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
samplerate, data = wavfile.read('Datei_1.wav')
y = 0

#Ausgabe der Array-Länge, Samplerate und dem Array
print(data.size, samplerate, data)

array_integr = np.zeros((data.size))

for i in range(-1, (data.size)*-1, -1):
     y = y + data[i]**2                    #um Positive Teile zu nutzen?
     
     array_integr[i] = y

#rausrechnen der Samplerate -> Normierung...     ??
array_integr = array_integr/samplerate

array_log_integr = np.zeros((data.size))
array_log_integr = np.log(array_integr) / np.log(np.max(array_integr))

#Anzeige in Sekunden fehlt noch 
plt.plot(array_log_integr)
plt.show()

