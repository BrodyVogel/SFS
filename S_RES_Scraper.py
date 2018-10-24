#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 19:42:55 2017

@author: vogebr01
"""

### Import statements --> all Python standard, I think
from bs4 import BeautifulSoup
import requests
import os
import glob
import pandas as pd
import csv

### This work on Mac --> might need some tuning for Windows
path = input("Where do you want the files? Enter the path.  ")

### Name and create the folders
ResFolder = path + 'S_RES_RESOLUTION_DETAILS' + '/'
VoteFolder = path + 'S_RES_VOTING_DETAILS' + '/'

os.makedirs(ResFolder)
os.makedirs(VoteFolder)

### These won't work --> you'll have to initiate your own session and grab the links
    ### Trust me, this is still faster than using a webdriver
urls = ['http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&menu=search&aspect=power&npp=50&ipp=20&spp=20&profile=voting&ri=67&source=%7E%21horizon&index=.VM&term=S%2FRES%2F&x=17&y=15&aspect=power', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=2&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731809666',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=3&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731836051', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=4&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731847467',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=5&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731856308', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=6&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731865728',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=7&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731874310', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=8&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731882355',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=9&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731890701', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=10&group=0&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731900182',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=11&group=1&term=S/RES/&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&ts=1511731908258&deduping=', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=12&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731916988',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=13&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731926062', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=14&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731933722',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=15&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731942190', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=16&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731950080',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=17&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731957972', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=18&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731966099',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=19&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731973937', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=20&group=1&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511731981915',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=21&group=2&term=S/RES/&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&ts=1511731991956&deduping=', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=22&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732001583',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=23&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732010658', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=24&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732018800',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=25&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732027104', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=26&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732050221',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=27&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732059458', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=28&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732067575',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=29&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732077304', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=30&group=2&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732085767',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=31&group=3&term=S/RES/&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&ts=1511732095878&deduping=', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=32&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732104476',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=33&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732112707', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=34&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732121044',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=35&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732130052', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=36&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732138233',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=37&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732148026', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=38&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732157197',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=39&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732166726', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=40&group=3&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732174670',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=41&group=4&term=S/RES/&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&ts=1511732183321&deduping=', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=42&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732191749',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=43&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732202182', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=44&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732211220',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=45&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732220358', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=46&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732230325',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=47&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732240982', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=48&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732250573',
        'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=49&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732259342', 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=151E73011G387.9965&profile=voting&page=50&group=4&term=S%2FRES%2F&index=.VM&uindex=&aspect=power&menu=search&ri=68&source=~!horizon&1511732267302']

### Timeout buckets
timeouts = []
timeouts1 = []

for page in urls:
    try:
        ### Set timeout limit
        hold = requests.get(page, timeout = 15)

    
        data1 = hold.text
        soup1 = BeautifulSoup(data1, 'lxml')

        links = soup1.find_all('a', href=True)
        res = [x for x in links if 'profile%3Dvoting' in x['href']]

        ### Bucket for resolution links
        clean = []
        
        ### Decode the links
        for link in res:
            link = link['href'][24:]
            link = link.replace('%3A', ':')
            link = link.replace('%2F', '/')
            link = link.replace('%3F', '?')
            link = link.replace('%3D', '=')
            link = link.replace('%26', '&')
            link = link.replace('%21', '!')
            link = link.replace('%7E', '~')
            link = link.replace("'", "")
            link = link.split(',')
            clean.append(link[0])
    
        clean = [x for x in clean if '!horizon' in x and 'term=' not in x]
        ### There are two instances of every link --> trim the extras
        clean = clean[::2]

        ### Make the files
        for url in clean:
    

            try:
                request = requests.get(url, timeout = 10)
    
                if request.status_code == 200:
    
                    data = request.text

                    print('Made it - working on', url[104:111])
                    soup = BeautifulSoup(data, 'lxml')

                    dets = soup.findAll('tr')

                    keeper = [x for x in dets if 'Detailed Voting' in x.text]
                    if keeper != []:
                        Dvote = keeper[1].findAll('td')
                        if len(Dvote[24]) > 30: 
                            Dvote1 = Dvote[25:]
                        else:
                            Dvote1 = Dvote[24:]
    
                        helper = str(Dvote[2].text).replace('/', '\\')
                        helper1 = str(Dvote[2].text).replace('/', '\\')



                        s = open(VoteFolder + helper + '.txt', 'w')

                        for x in Dvote1:
                            s.write(x.text)
                            s.write('\n')
    
                        s.close()
        

                        t = open(ResFolder + helper1 + '.txt', 'w')

                        t.write('\n')
                        t.write('UN Resolution Symbol:\t')
                        t.write(Dvote[2].text)
                        t.write(';\n')
                        t.write('Link To:\t')
                        t.write(url)
                        t.write(';\n')
                        t.write('Meeting Symbol:\t')
                        t.write(Dvote[8].text)
                        t.write(';\n')
                        t.write('Title:\t')
                        t.write(Dvote[11].text)
                        t.write(';\n')
                        if 'Yes:' in Dvote[14].text:
                            t.write('Voting Summary:\t')
                            t.write(Dvote[14].text)
                            t.write(';\n')
                            t.write('Voting Date:\t')
                            t.write(Dvote[17].text)
                            t.write(';\n')
                            t.write('Agenda Information:\t')
                            t.write(Dvote[20].text)
                            t.write(';\n')

                            t.close()
                        else:
                            t.write('Related Document:\t')
                            t.write(Dvote[14].text)
                            t.write(';\n')
                            t.write('Voting Summary:\t')
                            t.write(Dvote[17].text)
                            t.write(';\n')
                            t.write('Voting Date:\t')
                            t.write(Dvote[20].text)
                            t.write(';\n')
                            t.write('Agenda Information:\t')
                            t.write(Dvote[23].text)
                            t.write(';\n')

                            t.close()

            except:
                timeouts.append(url)
                continue
    except:
           timeouts1.append(page)
           continue
    
### If timeouts1 == [], there's no reason to run this section --> skip to part 2
timeouts2 = []
    
while timeouts1 != []:
    try:
        url = timeouts1[0]
        hold = requests.get(page, timeout = 15)

    
        data1 = hold.text
        soup1 = BeautifulSoup(data1, 'lxml')

        links = soup1.find_all('a', href=True)
        res = [x for x in links if 'profile%3Dvoting' in x['href']]

        clean = []
        for link in res:
            link = link['href'][24:]
            link = link.replace('%3A', ':')
            link = link.replace('%2F', '/')
            link = link.replace('%3F', '?')
            link = link.replace('%3D', '=')
            link = link.replace('%26', '&')
            link = link.replace('%21', '!')
            link = link.replace('%7E', '~')
            link = link.replace("'", "")
            link = link.split(',')
            clean.append(link[0])
    
        clean = [x for x in clean if '!horizon' in x and 'term=' not in x]
        clean = clean[::2]

        for url in clean:
    

            try:
                request = requests.get(url, timeout = 10)
    
                if request.status_code == 200:
    
                    data = request.text

                    print('Made it - working on', url[104:111])
                    soup = BeautifulSoup(data, 'lxml')

                    dets = soup.findAll('tr')

                    keeper = [x for x in dets if 'Detailed Voting' in x.text]
                    if keeper != []:
                        Dvote = keeper[1].findAll('td')
                        if len(Dvote[24]) > 30: 
                            Dvote1 = Dvote[25:]
                        else:
                            Dvote1 = Dvote[24:]
    
                        helper = str(Dvote[2].text).replace('/', '\\')
                        helper1 = str(Dvote[2].text).replace('/', '\\')



                        s = open(VoteFolder + helper + '.txt', 'w')

                        for x in Dvote1:
                            s.write(x.text)
                            s.write('\n')
    
                        s.close()
        

                        t = open(ResFolder + helper1 + '.txt', 'w')

                        t.write('\n')
                        t.write('UN Resolution Symbol:\t')
                        t.write(Dvote[2].text)
                        t.write(';\n')
                        t.write('Link To:\t')
                        t.write(url)
                        t.write(';\n')
                        t.write('Meeting Symbol:\t')
                        t.write(Dvote[8].text)
                        t.write(';\n')
                        t.write('Title:\t')
                        t.write(Dvote[11].text)
                        t.write(';\n')
                        if 'Yes:' in Dvote[14].text:
                            t.write('Voting Summary:\t')
                            t.write(Dvote[14].text)
                            t.write(';\n')
                            t.write('Voting Date:\t')
                            t.write(Dvote[17].text)
                            t.write(';\n')
                            t.write('Agenda Information:\t')
                            t.write(Dvote[20].text)
                            t.write(';\n')

                            t.close()
                        else:
                            t.write('Related Document:\t')
                            t.write(Dvote[14].text)
                            t.write(';\n')
                            t.write('Voting Summary:\t')
                            t.write(Dvote[17].text)
                            t.write(';\n')
                            t.write('Voting Date:\t')
                            t.write(Dvote[20].text)
                            t.write(';\n')
                            t.write('Agenda Information:\t')
                            t.write(Dvote[23].text)
                            t.write(';\n')

                            t.close()
            except:
                timeouts.append(url)
                continue
            
        timeouts1.remove(url)
        
    except:
           continue

##### PART 2 #####
### Fill in all the timeouts data
while timeouts != []:    

    try:    
        url = timeouts[0]
            
        request = requests.get(url, timeout = 10)
    
        if request.status_code == 200:
                
    
            data = request.text

            print('Made it - working on', url[104:111])
            
        
            soup = BeautifulSoup(data, 'lxml')

            dets = soup.findAll('tr')

            keeper = [x for x in dets if 'Detailed Voting' in x.text]
            if keeper != []:
                Dvote = keeper[1].findAll('td')
                if len(Dvote[24]) > 30: 
                    Dvote1 = Dvote[25:]
                else:
                    Dvote1 = Dvote[24:]
    
                helper = str(Dvote[2].text).replace('/', '\\')
                helper1 = str(Dvote[2].text).replace('/', '\\')



                s = open(VoteFolder + helper + '.txt', 'w')

                for x in Dvote1:
                    s.write(x.text)
                    s.write('\n')
    
                s.close()
    

                t = open(ResFolder + helper1 + '.txt', 'w')

                t.write('\n')
                t.write('UN Resolution Symbol:\t')
                t.write(Dvote[2].text)
                t.write(';\n')
                t.write('Link To:\t')
                t.write(url)
                t.write(';\n')
                t.write('Meeting Symbol:\t')
                t.write(Dvote[8].text)
                t.write(';\n')
                t.write('Title:\t')
                t.write(Dvote[11].text)
                t.write(';\n')
                if 'Yes:' in Dvote[14].text:
                    t.write('Voting Summary:\t')
                    t.write(Dvote[14].text)
                    t.write(';\n')
                    t.write('Voting Date:\t')
                    t.write(Dvote[17].text)
                    t.write(';\n')
                    t.write('Agenda Information:\t')
                    t.write(Dvote[20].text)
                    t.write(';\n')
                    
                    t.close()
                else:
                    t.write('Related Document:\t')
                    t.write(Dvote[14].text)
                    t.write(';\n')
                    t.write('Voting Summary:\t')
                    t.write(Dvote[17].text)
                    t.write(';\n')
                    t.write('Voting Date:\t')
                    t.write(Dvote[20].text)
                    t.write(';\n')
                    t.write('Agenda Information:\t')
                    t.write(Dvote[23].text)
                    t.write(';\n')

                    t.close()
                    
            timeouts.remove(url)
            print("timeouts left: ", len(timeouts))
                    
    except:
        continue


##### PART 3 #####        
os.chdir(VoteFolder)

### Name and create the tab folder for later
newString = VoteFolder + 'VotingTabFile' + '.txt'

tabFile = open(newString, 'w')

countryList = ['ALGERIA','ANGOLA','ARGENTINA','AUSTRALIA','AUSTRIA','AZERBAIJAN', 'BAHRAIN','BANGLADESH','BELARUS',
                'BELGIUM', 'BENIN','BOSNIA AND HERZEGOVINA', 'BOLIVIA (PLURINATIONAL STATE OF)',
                'BOTSWANA','BRAZIL','BULGARIA','BURKINA FASO','BURUNDI','CABO VERDE',
                'CAMEROON','CANADA', 'CAPE VERDE', 'CHAD','CHILE','CHINA','COLOMBIA',
                'CONGO','COSTA RICA',"COTE D'IVOIRE",'CROATIA','CUBA', 'CZECHOSLOVAKIA', 'CZECH REPUBLIC',
                'DEMOCRATIC REPUBLIC OF THE CONGO','DENMARK','DJIBOUTI','ECUADOR','EGYPT','EQUATORIAL GUINEA',
                'ETHIOPIA', 'FINLAND','FRANCE','GABON','GAMBIA', 'GERMANY','GHANA','GREECE',
                'GUATEMALA','GUINEA','GUINEA-BISSAU','GUYANA','HONDURAS','HUNGARY',
                'INDIA','INDONESIA','IRAN (ISLAMIC REPUBLIC OF)', 'IRAQ', 'IRELAND', 'ITALY','JAMAICA',
                'JAPAN','JORDAN','KAZAKHSTAN','KENYA', 'KUWAIT',
                'LEBANON','LIBERIA','LIBYA',
                'LITHUANIA','LUXEMBOURG','MADAGASCAR','MALAYSIA','MALI','MALTA',
                'MAURITANIA','MAURITIUS','MEXICO','MOROCCO','NAMIBIA','NEPAL','NETHERLANDS',
                'NEW ZEALAND','NICARAGUA','NIGER','NIGERIA','NORWAY','OMAN','PAKISTAN','PANAMA',
                'PARAGUAY','PERU','PHILIPPINES','POLAND','PORTUGAL','QATAR','REPUBLIC OF KOREA',
                'ROMANIA','RUSSIAN FEDERATION','RWANDA','SAUDI ARABIA','SENEGAL',
                'SIERRA LEONE','SINGAPORE','SLOVAKIA','SLOVENIA', 'SOMALIA',
                'SOUTH AFRICA','SPAIN','SRI LANKA','SUDAN', 'SWEDEN',
                'THAILAND','TOGO','TRINIDAD AND TOBAGO','TUNISIA','TURKEY',
                'UGANDA','UKRAINE','UNITED ARAB EMIRATES', 'UNITED ARAB REPUBLIC', 'UNITED KINGDOM','UNITED REPUBLIC OF TANZANIA','UNITED STATES',
                'URUGUAY', 'USSR', 'VENEZUELA (BOLIVARIAN REPUBLIC OF)','VIET NAM','DEMOCRATIC YEMEN','YUGOSLAVIA', 'ZAMBIA','ZIMBABWE']

tabFile.write('UN Resolution Number')

for name in countryList:
    tabFile.write('\t')
    tabFile.write(name)
tabFile.write('\n')

dis = 0
for file in glob.glob('*.txt'):
    
    if 'A\\RES' in file:
        continue
    
    else:

        f = open(file, 'r')
        lines = f.readlines()
        f.close()
    
        tabFile.write(file[:-4].replace('\\', '/'))
    
        voteList = []
    
        for i in range(len(countryList)):
            voteList.append('')
        
        for line in lines:
            line = line.replace('\n','')
            voteCode = ''
            if line != '':
                if line[:4] == 'R Y ' or line[:4] == 'P Y ' or line[:4] == 'P y':
                    countryName = line[4:]
                    voteCode = '1'
                elif line[:4] == 'R N ' or line[:4] == 'P N ':
                    countryName = line[4:]
                    voteCode = '3'
                elif line[:4] == 'R A ' or line[:4] == 'P A ':
                    countryName = line[4:]
                    voteCode = '2'
                else:
                    countryName = line
                    voteCode = '8'
            

                found = False
                index = 0
                for country in countryList:
                    if countryName == country:
                        voteList[index] = voteCode
                        found = True
                    index += 1
                if not found:
                    ### dummy variable
                    r = 1
    
        index = 0
        for country in countryList:
            tabFile.write('\t')
            tabFile.write(voteList[index])
            index += 1
        tabFile.write('\n')
    

tabFile.close()

##### PART 4 #####

### Create the output --> 2 files: every vote and resolution details

os.chdir(ResFolder)

newString2 = ResFolder + 'ResolutionTabFile' + '.txt'

t = open(newString2, 'w')

t.write('UN Resolution Symbol')
t.write('\t')
t.write('Link To')
t.write('\t')
t.write('Meeting Symbol')
t.write('\t')
t.write('Title')
t.write('\t')
t.write('Related Document')
t.write('\t')
t.write('Vote Notes')
t.write('\t')
t.write('Vote Date')
t.write('\t')
t.write('Agenda Information')
t.write('\n')

dates = []

for file in glob.glob('*.txt')[1:]:
    
    if 'A\\RES' in file:
        continue
    
    else:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
    
        caseReport = {'UN Resolution Symbol:':'', 'Link To:':'', 'Meeting Symbol:':'', 'Title:':'', 'Related Document:':'', 'Vote Notes:':'', 'Voting Summary:':'', 'Vote Date:':'', 'Voting Date:':'', 'Agenda Information:':''}

        for line in lines[1:]:
            category = (line.strip('\n').split('\t'))[0]
            information = ((line.strip('\n').split('\t'))[1]).strip(';').replace(';;', ';')
            caseReport[category] = information
   
        t.write(caseReport['UN Resolution Symbol:'])
        t.write('\t')
        t.write(caseReport['Link To:'])
        t.write('\t')
        t.write(caseReport['Meeting Symbol:'])
        t.write('\t')
        t.write(caseReport['Title:'])
        t.write('\t')
        t.write(caseReport['Related Document:'])
        t.write('\t')
        t.write(caseReport['Vote Notes:'])
        t.write('\t')
        t.write(caseReport['Voting Summary:'])
        t.write('\t')

        if caseReport['Vote Date:'] == '':
            t.write(str(caseReport['Voting Date:'])[4:6])
            t.write('/')
            t.write(str(caseReport['Voting Date:'])[6:8])
            t.write('/')
            t.write(str(caseReport['Voting Date:'])[:4])
            dateString = (str(caseReport['Voting Date:']))[4:6] + '/' + str((caseReport['Voting Date:']))[6:8] + '/' + str((caseReport['Voting Date:']))[:4]

        else:
            t.write((caseReport['Vote Date:'])[4:6])
            t.write('/')
            t.write((caseReport['Vote Date:'])[6:8])
            t.write('/')
            t.write((caseReport['Vote Date:'])[:4])
            dateString = (caseReport['Vote Date:'])[4:6] + '/' + (caseReport['Vote Date:'])[6:8] + '/' + (caseReport['Vote Date:'])[:4]
    
        dates.append(dateString)


        t.write('\t')
        t.write(caseReport['Agenda Information:'])
        t.write('\n')

t.close()

### make everything pretty
newString3 = VoteFolder + 'VOTING_DETAILS_OUTPUT' + '.csv'
in_txt = csv.reader(open(newString, 'r'), delimiter = '\t')
out_csv = csv.writer(open(newString3, 'w'))
out_csv.writerows(in_txt)
    
ccList = [615, 540, 160, 900, 305, 373, 692, 771, 370, 211, 434, 346, 145, 571, 140, 355, 439, 516, 402, 471, 20, 402, 483, 155, 710, 100, 484, 94, 437, 344, 40, 315, 316, 490, 390, 522, 130, 651, 411, 530, 375, 220, 481, 420, 255, 452, 350, 90, 438, 404, 110, 91, 310, 750, 850, 630, 645, 205, 325, 51, 740, 663, 705, 501, 690, 660, 450, 620, 368, 212, 580, 820, 432, 338, 435, 590, 70, 600, 565, 790, 210, 920, 93, 436, 475, 385, 698, 770, 95, 150, 135, 840, 290, 235, 694, 732, 360, 365, 517, 670, 433, 451, 830, 317, 349, 520, 560, 230, 780, 625, 380, 800, 461, 52, 616, 640, 500, 369, 696, 696, 200, 510, 2, 165, 000, 101, 816, 679, 345, 551, 552]
un = pd.read_csv(newString3, header = None)

un = un.fillna(0)

string2 = path + 'Final_Votes.csv'

out = csv.writer(open(string2, 'w'))

b = 1
for country in un.iloc[0,:][1:]:
    y = 0
    a = 1
    for x in un.iloc[:, b][1:]:
        countryCode = countryList.index(country)
        countryCode = ccList[countryCode]
        out.writerow([country, countryCode, un.iloc[:,0][y + 1], dates[y - 1], un.iloc[a, b]])
        y += 1
        a += 1
    b += 1
    
newString4 = path + 'RESOLUTIONS_DETAILS_OUTPUT_' + '.csv'
in_txt2 = csv.reader(open(newString2, 'r'), delimiter = '\t')
out_csv2 = csv.writer(open(newString4, 'w'))
out_csv2.writerow(['UN Resolution Symbol', 'Link To', 'Meeting Symbol', 'Title', 'Related Documents', 'Vote Notes', 'Results', 'Date', 'Agenda Information'])
for row in in_txt2:
    if row[0] != 'UN Resolution Symbol':
        out_csv2.writerow(row)

        




