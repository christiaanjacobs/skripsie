# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:30:35 2019

@author: Christiaan
"""
import os
import scipy.io.wavfile as wav
import numpy as np
from python_speech_features import mfcc as MFCC
from python_speech_features import delta as DELTA
import librosa
import librosa.display
from sklearn.preprocessing import normalize

# read n amount of audio clips from directory
# return array with shape (nx2) -> [:,0]=signals, [:,1]=sample_rates
def read_audio(path):
    path = path
    files = os.listdir(path)
    
    N = len(files)
  
    audio_clips = []
    for n in range(N):
    #        index = random.randrange(0, len(files))
    #        print(files[index])
    
        try:
                #rate, sig = wav.read(path + "\\" + files[n])
            sig, rate = librosa.load(str(path) + "\\" + str(files[n]),sr=16000)
    #        sig, rate = librosa.load(str(path), sr=16000)
    
            if len(sig) > rate:
                audio_clips.append((sig.astype(float),rate))
            #IPython.display.Audio(data=sig, rate = rate)
        except:
            print("%s could not be read" % files[n])

    audio_clips = np.asarray(audio_clips) # convert to numpy array
    #print(audio_clips.shape)
    
    return audio_clips

def split_audio(audio_clip, rate, time):
    samples = time*rate
    #print(samples)
    time_frames = []
    N = len(audio_clip)//samples
    for n in range(N):
        n1 = n*samples
        n2 = n1 + samples
        if n2 <= len(audio_clip):
            time_frames.append(audio_clip[n1:n2])
        else:
            print("The last ... seconds coould not fit to %f second frame")
    time_frames = np.asarray(time_frames)  
    return time_frames

def normalize_audio(segmented_clips):
    norm_all = []
    for i in range(len(segmented_clips)):      
        norm = []
        for j in range(len(segmented_clips[i])):
            #segmented_clips[i][j,:] = segmented_clips[i][j,:]/np.max(np.abs(segmented_clips[i][j,:]))
            if np.max(np.abs(segmented_clips[i][j,:])) > 0:
                norm.append(segmented_clips[i][j,:]/np.max(np.abs(segmented_clips[i][j,:])))
           # print(len(segmented_clips[i][j,:]/np.max(np.abs(segmented_clips[i][j,:]))))
        norm_all.append(norm)
        #print(norm_all)
    return norm_all

def mfcc(segments,rate,norm=True):
    #print(segments.shape)
    mfccs_clip = []
    for i in range(len(segments)):
        mfccs = MFCC(segments[i],samplerate=rate, winlen=0.025, winstep=0.01, numcep=20, nfilt=32, nfft=512,
                     lowfreq=0, highfreq=None, preemph=0.95, ceplifter=22, appendEnergy=False, winfunc=np.hamming)
        
        #mfccs = sklearn.preprocessing.scale(mfccs,axis=1)
        deltas = delta(mfccs) #
        delta_deltas = delta_delta(deltas)
        mfccs_clip.append(np.concatenate((mfccs,deltas,delta_deltas),axis=1))
#         mfccs_clip.append(mfccs)
    mfccs_clip = np.asarray(mfccs_clip)
    
    return mfccs_clip

def delta(mfccs):
    deltas = DELTA(mfccs,N=2)
    return deltas

def delta_delta(delta):
    deltas = DELTA(delta, N=2)
    return deltas

def hzcrr(segments):
    zcr_ar = []
    for x in range(len(segments)):
        zcr = librosa.feature.zero_crossing_rate(segments[x]+0.0001)
        zcr = zcr.reshape(-1)
        zcr_ar.append(zcr)
    zcr_ar = np.array(zcr_ar)
    
    
    
    av_zcr_ar = np.average(zcr_ar,axis=1)
    #print(av_zcr_ar.shape)
    N = np.shape(zcr_ar)[1]
    #print(N)

    hzcrr_ar = np.zeros((np.shape(zcr_ar)[0]),dtype=float)
    #print(hzcrr_ar)
    for i in range(np.shape(zcr_ar)[0]):
        #print(zcr_ar[i,:])
        hzcrr_ar[i] = 1/(2*N)*np.sum(np.sign(zcr_ar[i,:]-1.5*av_zcr_ar[i])+1)
    #data = hzcrr_ar   
    return hzcrr_ar
    #print(zcr_ar.shape)
    

def stEnergy(frame):
    """Computes signal energy of frame"""
    #print(len(frame))
    #print(np.sum(np.abs(frame ** 2)) / np.float64(len(frame)))
    return np.sum(np.abs(frame ** 2)) / np.float64(len(frame))

def calcFrames(signal,length):
    #print(len(signal))
    #print(length)
    if len(signal) % length != 0:
        print("Signal length not dividable by frame length")
    else:
        frames = np.zeros((int(len(signal)/length),length),dtype=float)
        #print(frames.shape)
        #print(signal.shape)
        #signal = signal.reshape(-1,1)
        #print(signal.shape)
        for n in range(len(frames)):
            #print(len(signal[n*length:n*length+length]))
            frames[n,:] = signal[n*length:n*length+length]
    return frames

def calcFramesEnergy(frames):
    frame_energy = []
    for n in range(len(frames)):
        frame_energy.append(stEnergy(frames[n]))
    #print(frames_energy[0:10])    
    return np.array(frame_energy,dtype=float)

def avg_stEnergy(frame_energy):
    #print(np.average(frame_energy))
    return np.average(frame_energy)

def lster(frame_energy):
    N = np.shape(frame_energy)[0]
    #lster_ar = np.zeros((N),dtype=float)
    avg_e = avg_stEnergy(frame_energy)
    #print(lster_ar.shape)
    lster = 1/(2*N)*np.sum(np.sign(0.5*avg_e - frame_energy)+1)
    #print(np.sum(np.sign(0.5*avg_e - frame_energy)))
        #print(1/(2*N)*np.sum(np.sign(0.5*avg_e - frame_energy[n])+1))
    return lster

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
            #avg_ste = avg_stEnergy(frames_energy)
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
    return feat_test,length, segmented_clips
