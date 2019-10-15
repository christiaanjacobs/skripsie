# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:40:25 2019

@author: Christiaan
"""

from bs4 import BeautifulSoup as bs
import requests
import re
import pafy
import os
import numpy as np
import random
import time

import youtube_dl

#TODO: Save links to txt file and do not downlaod again

# max page = 30
def createLinks(n_pages = 30):
    arr=["and","the"] #,"on" ,"in","is","to","of","a","have","it"] #"for" "not" "with" "as" "you" "do" "this" "but" "his" "by" "from" "they" "we" "say" "her" "she" "or" "an" "will"  "my"  "one"  "all" "would"  "there"  "their"  "what"  "up"  "if" "about"  "who"  "which"  "go"  "when" "make" "can" "like" "time"  "just" "him"  "take"  "people" "into" "good"  "some"  "could"  "them" "see" "other" "only"  "then" "come"  "its" "also" "over" "think" "also" "back" "after" "use" "two" "how" "our" "work" "first" "well" "way" "even" "new" "want" "because" "any" "these" "give" "day" "most" "us" "time" "person" "year" "get" "know"]
    #print(len(arr))
    if n_pages <= 30 and n_pages > 0:
        n_pages = n_pages
    else:
        print("Max page is 30, Max set to 30")

    links = [] # contains all page links
    for w in arr:
        for i in range(n_pages):
            url = "https://www.youtube.com/results?search_query=%s&sp=EgYIBBABKAE%%253D&p=%d"%(w,(i+1))
            links.append(url)
            #print(url)
    print(len(links)) #all pages links
    #print(links[0])
    return links

#def getVideoLink(links):
#    #extract href from all pages
#    videolist = [] #contains video links
#    for i in range(len(links)):
#        print(i)
#        time.sleep(2) # wait 2 seconds to prevent blacklisting
#        r = requests.get(links[i])
#        page = r.text
#        soup=bs(page,'html.parser')
#        #message = soup.findAll('yt-formatted-string')
#        #print(message)
#        try:
#            vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
#            for v in vids:
#                videolist = np.append(videolist,'https://www.youtube.com' + v['href'])
#            #print(videolist)
#        except:
#            print("No videos on page")
#    #print(len(videolist))
#    print(videolist[0])
#    #print(len(vids))
#    return videolist


def getVideoLink(link):
    #extract href from all pages
    videolist = [] #contains video links
    time.sleep(2) # wait 2 seconds to prevent blacklisting
    r = requests.get(link)
    page = r.text
    soup=bs(page,'html.parser')
        #message = soup.findAll('yt-formatted-string')
        #print(message)
    try:
        vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
        for v in vids:
            videolist = np.append(videolist,'https://www.youtube.com' + v['href'])
            #print(videolist)
    except:
        print("No videos on page")
    #print(len(videolist))
    print(videolist[0])
    #print(len(vids))
    return videolist



def downloadAudio(url, maxTime = None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav'
            #'preferredquality': '256'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
        'write-description' : True
    }
    print(os.getcwd())    
    os.chdir("downloaded")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            dictMeta = ydl.extract_info(url,download=False)
            
            try:
                file = open('../videolist.txt', 'r')
            except:
                print("unlucky")
            write = True
            print(write)
            for line in file:
                #print(line)
                if line.strip('\n') == dictMeta['title']:
                    print('Video already downloaded')
                    write = False
            
            print(write)        
            if write == True:
                f = open('../videolist.txt', 'a+')
                f. write('%s\n' % dictMeta['title'])
                f.close()
                ydl.download([url])
        except:
            print("Could not connect")
            write = False
    os.chdir("../")

    return write
    
    
def deleteAudio():
    print(os.getcwd())
    folder = 'downloaded'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

#                    f = open('videolist.txt', 'a+')
#                    f. write('%s\n' % dictMeta['title'])
                    
                    
                    
#createLinks()
#links = getVideoLink(createLinks(n_pages=1))
#print(len(links))
#for i in range(len(links)):
#    downloadAudio(links[i])
