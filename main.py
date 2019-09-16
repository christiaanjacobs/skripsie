# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import numpy as np
#from tkinter import *
#window = Tk()
#window.title("Speech Collector")
#window.geometry('350x200')
#lbl = Label(window, text="Time")
#lbl.grid(column=0, row=0)
#
#window.mainloop()

import os
import random
import IPython
import scipy.io.wavfile as wav
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

from python_speech_features import mfcc as MFCC
from python_speech_features import delta as DELTA
from python_speech_features import logfbank

from sklearn.mixture import GaussianMixture as GMM
import pickle

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import IPython.display
import sklearn
import librosa
import librosa.display
import glob

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.utils import shuffle

import audio_processing as ap
import classification as cln
import write_audio as wa

from scipy.signal import medfilt

# Load models
print("Load models...")
n_comp = 128
filename = 'models/mix_model%d_62.sav'%n_comp
mix_model = pickle.load(open(filename, 'rb'))

filename = "models/speech_model%d_62.sav"%n_comp
speech_model = pickle.load(open(filename, 'rb'))
print("Done!")

# Fetch audio from folder
print("Load audio from folder and construct features...")
path =r"D:\Download"
feats, length, segmented_clips = ap.get_features(path)
print("Done!")

#print(len(segmented_clips[0][0]))
#print(segmented_clips)

# label seconds
print("Classifying...")
all_probs = cln.probs(feats,speech_model,mix_model)
second_probs = cln.avg_prob(all_probs)
probs_thershold, save_all = cln.thershold(second_probs,segmented_clips)
filtered = cln.median_filter(probs_thershold)
mfccs_labeled = cln.label(filtered)
print("Done!")
#print(mfccs_labeled)

# Write remaining speech to folder
print("Write speech to folder...")
save_all = np.array(save_all) #contains segmented_clips to write
wa.write(mfccs_labeled,save_all)
print("Done!")



