# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:52:09 2019

@author: Christiaan
"""


import numpy as np
import matplotlib.pyplot as plt





# Calculates the average log-likelihood of 1-second window being speech and labels it accordingly
def loglike(mfccs_test,speech_model,mix_model):
    #print(len(mfccs_test))
    feat_labels = []
    for j in range(len(mfccs_test)):
        test = mfccs_test[j]
        mfcc_label = np.empty((len(test)),dtype=int)
        for i in range(len(test)):
            #print(test[i].shape)
            #print(hzcrr_test[j].shape)
            speech_gmm = speech_model.score(test[i])
            mix_gmm = mix_model.score(test[i])
            if speech_gmm > mix_gmm:
                mfcc_label[i] = 0
            else:
                mfcc_label[i] = 1
        feat_labels.append(mfcc_label)
    feat_labels = np.array(feat_labels)
    return feat_labels
    
    
# Calculates the probability of 25ms being speech from models    
def probs(mfccs_test,speech_model,mix_model):
    all_probs = []
    for j in range(len(mfccs_test)):
        test = mfccs_test[j]
        mfccs_prob = []
        for i in range(len(test)):
            #print(test[i].shape)
            #print(hzcrr_test[j].shape)
            speech_gmm = speech_model.score_samples(test[i])
            mix_gmm = mix_model.score_samples(test[i])
            p = np.exp(speech_gmm)/(np.exp(speech_gmm)+np.exp(mix_gmm))
            #print(p.shape)
            mfccs_prob.append(p)
        mfccs_prob = np.array(mfccs_prob)
    #     print(np.sum(mfccs_prob,axis=1).shape)
        all_probs.append(mfccs_prob)
    all_probs = np.array(all_probs)
    return all_probs

# Calcualte the average probability in 1-second window
def avg_prob(all_probs):
    # sum probabilities over second
    second_probs = []
    for i in range(len(all_probs)):
        p = []
        for j in range(len(all_probs[i])):
            #print(all_probs[i][j].shape)
            tot = np.sum(all_probs[i][j])
            prob = tot/len(all_probs[i][j])
            p.append(prob)
        p = np.asarray(p)
        #print(p.shape)
        second_probs.append(p)
    second_probs = np.asarray(second_probs)
    return second_probs


# Select threshold and determine which windwows to disregard
def thershold(second_probs,segmented_clips):
    probs_thershold = []
    t = 0
    c = 0
    th = 0.15
#    plt.figure(figsize=(12,4))
#    plt.scatter(np.linspace(0,len(second_probs[0])-1,len(second_probs[0])),second_probs[0])
#    plt.plot(np.full((len(second_probs[0])),0.6))
#    plt.plot(np.full((len(second_probs[0])),0.4))
#    plt.show()
    
    save_all = []
    for i in range(len(second_probs)):
        x = second_probs[i]
        #print(x.shape)
        z = []
        save = []
        for j in range(len(x)):
            k = x[j]
            #print(k)
           
            if k < (0.5+th) and k > (0.5-th):
                #print(k)
                c +=1
                #save = np.append(save,0)

            else:
                z = np.append(z, k)
                #if k > 0.6:
                    #save = np.append(save,1)
                save.append(segmented_clips[i][j])

                #else:
                    #save = np.append(save,0)

            t+=1
        z = np.asarray(z)
        save_all.append(save)

        #print(y.shape)

        probs_thershold.append(z)
    probs_thershold = np.asarray(probs_thershold)
    #print(probs_thershold.shape)
#    print(c) #total seconds ignored
#    print(t) #total seconds
#
#    plt.figure(figsize=(12,4))
#    plt.scatter(np.linspace(0,len(probs_thershold[0])-1,len(probs_thershold[0])),probs_thershold[0])
#    plt.plot(np.full((len(probs_thershold[0])),0.6))
#    plt.plot(np.full((len(probs_thershold[0])),0.4))
#    plt.show()
    
    return probs_thershold, save_all

# Apply post processing on 1-second windows. If window labelled as speecch has non-speech neighbourng frames, change windoe to non-speech.
def median_filter(mfccs_labeled):
    from scipy.signal import medfilt
    filtered = []
    #t = 0
    
    
    for i in range(len(mfccs_labeled)):
    #     print(len(mfccs_labeled[i]))
        for j in range(len(mfccs_labeled[i])):
            if mfccs_labeled[i][j] == 0 and j<(len(mfccs_labeled[i])-1):
    #             print(j)
                if mfccs_labeled[i][j-1] == 1 and mfccs_labeled[i][j+1] == 1:
                    mfccs_labeled[i][j] = 1

    
#    for i in range(len(probs_thershold)):
#        filtered.append(medfilt(probs_thershold[i],kernel_size=5))
#        #print(1-np.sum(filtered[i])/len(filtered[i]))
#        #c+=np.sum(filtered[i])
#        #t+= len(filtered[i])
#    #print(filtered)
#    filtered = np.asarray(filtered)
#    #print(filtered[0])
    
    
    
    return filtered

# Use probabiliteis to label 1-second windows accordingly
def label(probs_thershold):
    # Hard label probabilities
    mfccs_labeled = []
    for i in range(len(probs_thershold)):
        x = []
        for j in range(len(probs_thershold[i])):
            if probs_thershold[i][j] > 0.5:
                x.append(0)
            else:
                x.append(1)
        x = np.asarray(x)
        mfccs_labeled.append(x)
    mfccs_labeled = np.asarray(mfccs_labeled)
    #print(mfccs_labeled[0])    

#     import array_to_latex as a2l
#     text = a2l.to_ltx(mfccs_labeled[0],arraytype='array',frmt='{:.0f}')
#     print(text)
    return mfccs_labeled
