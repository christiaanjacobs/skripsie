# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:12:18 2019

@author: Christiaan
"""
import numpy as np
from librosa.output import write_wav
import os

def write(mfccs_labeled, segmented_clips):
    #print(segmented_clips.shape)
#save_medfilt = []
#for i in range(len(save_all)):
#    save_medfilt.append(medfilt(save_all[i],kernel_size=3))
# print(len(save_medfilt))
    #print(mfccs_labeled.shape)
    
    files = os.listdir("speech")    
    N = len(files)
    
    for n in range(len(mfccs_labeled)):
        rem_audio = []
        for i in range(len(mfccs_labeled[n])):
            if mfccs_labeled[n][i] == 0:
                rem_audio = np.append(rem_audio,segmented_clips[n][i][:])
    
    
        rem_audio = np.array(rem_audio)
       # print(rem_audio[100:200])
        #wav.write("D:\Own set\Remaining\%d.wav"%n,rate=16000, data=rem_audio)
        print(os.getcwd())
        write_wav("speech\%d.wav"%(N+1), y=rem_audio, sr=16000, norm=False)