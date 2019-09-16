# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:34:45 2019

@author: Christiaan
"""
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


def get_features(audio_path):
    path = audio_path
    audio_clips = read_audio(path)
    segmented_clips = []
    length = 0
    for i in range(len(audio_clips)):
        x = split_audio(audio_clips[i,0],audio_clips[i,1], 1)
        length += len(x)
        segmented_clips.append(x)
    segmented_clips = np.asarray(segmented_clips)
    norm_segmented_clips = normalize_audio(segmented_clips)
    
    feat_test  = []
    for i in range(len(norm_segmented_clips)):
        x = mfcc(norm_segmented_clips[i],16000,norm=True)
        y = hzcrr(norm_segmented_clips[i])
        #####LSTER#######
        signal = norm_segmented_clips[i]
        lster_signal = []
        for j in range(len(signal)):
            frames = calcFrames(signal[j],400)
            frames_energy = calcFramesEnergy(frames)
            avg_ste = avg_stEnergy(frames_energy)
            lster_sig = lster(frames_energy)
            lster_signal.append(lster_sig)
        lster_signal = np.array(lster_signal)

        z = np.zeros((len(x),99))
        q = np.zeros((len(x),99))
        for k in range(len(z)):
            z[k] = y[k]
            q[k] = lster_signal[k]

        p = np.dstack((x,z))
        w = np.dstack((p,q))
        feat_test.append(w)
    return feat_test,length
