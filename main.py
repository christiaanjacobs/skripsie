# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from tkinter import *
from tkinter import scrolledtext
from tkinter import END, INSERT, DISABLED, NORMAL


 
import numpy as np
import pickle
import audio_processing as ap
import classification as cln
import write_audio as wa
import crawler

import os
import threading

start = False 
get_url = False
get_audio = False

def btnStart():
    global start
    start = True
    btn_start.config(state=DISABLED)
    t = threading.Thread(target=main)
    t.start()

def getUrl():
    global get_url
    get_url = True
       
def getAudio():
    global get_audio
    get_audio = True

def log(msg):
    txt.config(state=NORMAL)
    txt.insert(INSERT, chars="%s\n"%msg)
    txt.see("end")
    txt.config(state=DISABLED)

def main():
    global start
    global get_url
    global get_audio
    
    while True:
        
        if start == True:
           #txt.delete(1.0,END)
           links = crawler.createLinks()
           log("%d links created"%len(links))
           #txt.insert(INSERT, chars="%d links created\n"%len(links))
           getUrl()
           link_index = 0
           start = False
           
        if get_url == True:
            #txt.insert(INSERT, chars="Extracting urls\n")
            log("Extracting urls")

            videos = crawler.getVideoLink(links[link_index])
            getAudio()
            link_index += 1
            get_url = False
            
        if get_audio == True:
    
            for i in range(len(videos)):
                print(videos[i])
                #txt.insert(INSERT, chars="Extracting audio from video\n")
                log("Extracting audio from video")
                new = crawler.downloadAudio(videos[i]) # new = True = write 
                
                if new == True:
                    # Fetch audio from folder
                    print("Load audio from folder and construct features")
                    #txt.insert(INSERT, chars="Load audio from folder and construct features\n")
                    log("Load audio from folder and construct features")
                    path =r"C:\Users\Christiaan\Documents\repo\skripsie\downloaded"
                    feats, length, segmented_clips = ap.get_features(path)
                    #print(feats)
                    print("Done!")
                    
                    
                    # label seconds
                    print("Classifying...")
                    txt.insert(INSERT, chars="Classifying\n")

                    
                    all_probs = cln.probs(feats,speech_model,mix_model)
                    second_probs = cln.avg_prob(all_probs)
                    probs_thershold, save_all = cln.thershold(second_probs,segmented_clips)
                    filtered = cln.median_filter(probs_thershold)
                    mfccs_labeled = cln.label(filtered)
                    print("Done!")
                    #print(mfccs_labeled)
                    #print(save_all)
                    # Write remaining speech to folder
                    print("Write speech to folder...")
                    txt.insert(INSERT, chars="Write speech segments to folder\n")
    
                    save_all = np.array(save_all) #contains segmented_clips to write
                    wa.write(mfccs_labeled,save_all)
                    print("Done!")
                    
                    print("Deleting original audio")
                    txt.insert(INSERT, chars="Deleting original audio\n")
                   
                    crawler.deleteAudio()
                    print("Done!")
                    txt.insert(INSERT, chars="###############################################\n")
                 
                    
                else:
                    #txt.insert(INSERT, chars="Already exists\n")
                    log("Already exists")
                    log("###############################################")
                    #txt.insert(INSERT, chars="###############################################\n")
                 
             
            getUrl()   
            get_audio = False
            



window = Tk()
window.title("Speech Collector")
window.geometry('800x600')
    
txt = scrolledtext.ScrolledText(window,width=60,height=20, state=DISABLED)
txt.pack(side="left", fill=Y)
txt.insert(INSERT, chars="Press start to begin...")
    
btn_start = Button(window, text='Start', width=20, command=btnStart)
btn_start.place(x=600,y=80)

window.mainloop()

# Load models
print("Load models...")
n_comp = 128
filename = 'models/mix_model%d_62.sav'%n_comp
mix_model = pickle.load(open(filename, 'rb'))

filename = "models/speech_model%d_62.sav"%n_comp
speech_model = pickle.load(open(filename, 'rb'))

os.chdir(r"C:\Users\Christiaan\Documents\repo\skripsie")

    
#main()




## Load models
#print("Load models...")
#n_comp = 128
#filename = 'models/mix_model%d_62.sav'%n_comp
#mix_model = pickle.load(open(filename, 'rb'))
#
#filename = "models/speech_model%d_62.sav"%n_comp
#speech_model = pickle.load(open(filename, 'rb'))
#
#print("Done!")
#
## Fetch audio from folder
#print("Load audio from folder and construct features...")
#path =r"D:\Child Speech\Speech only"
#feats, length, segmented_clips = ap.get_features(path)
#print("Done!")
#
#
## label seconds
#print("Classifying...")
#all_probs = cln.probs(feats,speech_model,mix_model)
#second_probs = cln.avg_prob(all_probs)
#probs_thershold, save_all = cln.thershold(second_probs,segmented_clips)
#filtered = cln.median_filter(probs_thershold)
#mfccs_labeled = cln.label(filtered)
#print("Done!")
#
## Write remaining speech to folder
#print("Write speech to folder...")
#save_all = np.array(save_all) #contains segmented_clips to write
#wa.write(mfccs_labeled,save_all)
#print("Done!")



