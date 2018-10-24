#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 22:28:09 2017

@author: vogebr01
"""

from selenium import webdriver
from time import sleep
import os
import glob
import csv
import pandas as pd

path = input("Please enter the path of the location for the output files, like /Users/you/Desktop/ : ")

### This is important - IT MUST MATCH THE FORMAT 71 EXACTLY, so ARES71 will break it
search = input("Please enter the session for which you'd like data, like 71': ")

### As of now, this scraper is only designed to handle [1] - General Assembly Adopted with Vote
answ = 1
string1 = path + 'Resolution_Details' + search + '_' + str(answ) + '/'
string2 = path + 'Detailed_Voting' + search + '_' + str(answ) + '/'

os.makedirs(string1)
os.makedirs(string2)

Resolutions_Directory = path + 'Resolution_Details' + search + '_' + str(answ) + '/'
Voting_Details = path + 'Detailed_Voting' + search + '_' + str(answ) + '/'

def is71(str):
    condition = 'S/RES/' + search
    if len(str) < 20 and condition in str:
        return True
    else:
        return False

### tricky part - you must have selenium downloaded and installed, as well as geckodriver from gitHub
    ### once you've done that, update the executable_path to be wherever you keep geckodriver
driver = webdriver.Chrome(executable_path = '/Users/brodyvogel/Downloads/chromedriver')

driver.implicitly_wait(10)

if answ == 1:
    url = 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=15106908E98DA.5482&menu=search&aspect=power&npp=3000&ipp=20&spp=20&profile=voting&ri=1&matchopt=0%7C0&source=~%21horizon&index=.VM&term=S%2FRES%2F&x=0&y=0&aspect=power'
    #elif answ == 2:
    #url = 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?limitbox_1=VV01+%3D+vv_adp&go_sort_limit.x=5&go_sort_limit.y=5&npp=500&ipp=20&spp=20&profile=voting&aspect=power&term=A%2FRES%2F' + search + '&index=.VM&uindex=&oper=&session=150B87L994I50.5976&menu=search&aspect=power&npp=50&ipp=20&spp=20&profile=voting&ri=1&source=%7E%21horizon&sort='
#elif answ == 3:
    #url = 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?go_sort_limit.x=5&go_sort_limit.y=5&npp=500&ipp=20&spp=20&profile=voting&aspect=power&term=A%2FRES%2F' + search + '&index=.VM&uindex=&oper=&session=150B87L994I50.5976&limitbox_1=VI01+%3D+vi_s&menu=search&aspect=power&npp=50&ipp=20&spp=20&profile=voting&ri=1&source=%7E%21horizon&sort=&'
else:
    print("Something wasn't entered correctly. Run things again.")

    
driver.get(url)

print("If you see this, that's good")

counter = 0

print(len(driver.find_elements_by_class_name('smallAnchor')))

for i in range(len(driver.find_elements_by_class_name('smallAnchor'))):
    linkText = driver.find_elements_by_class_name('smallAnchor')[i].text.strip('\n')
    
    if is71(linkText):
        linkText = linkText.replace('/', '\\')
        counter += 1
        
        
        driver.find_elements_by_class_name('smallAnchor')[i].click()
        sleep(2)
        
        
        r = open(Resolutions_Directory + linkText + '.txt', 'w')
        v = open(Voting_Details + linkText + '.txt', 'w')
        
        elements = driver.find_element_by_name('full').find_elements_by_class_name('normalBlackFont1')
        
        enum = 0
        
        for element in elements:
            enum += 1
            info = element.get_attribute('innerHTML').replace('\t', '')
            if '&nbsp' in info:
                detailedVoting = False
                if 'Detailed Voting' in info:
                    detailedVoting = True
                else:
                    if enum != 1:
                        r.write('\n')
                    r.write(info.replace('\n','').replace('&nbsp','').strip(';'))
                    r.write('\t')
                
                if 'Agenda Information' in info:
                    aInfo = driver.find_element_by_partial_link_text('Agenda Information').find_element_by_xpath('..').find_element_by_xpath('..').find_elements_by_class_name('smallAnchor')
                    
                    for phrase in aInfo:
                        r.write(phrase.text.replace('\t', '').strip('\n'))
                        r.write(';')
            else:
                if detailedVoting:
                    v.write(info.replace('\n', ';'))
                    v.write('\n')
                else:
                    r.write(info.replace('\n', ';'))
                    r.write(';')
                    
        v.close()
        r.close()
        
        driver.back()
        sleep(3)
        ### this is how many files it's made it through
        print(counter)
        
#### start of part 2

os.chdir(Voting_Details)

newString = Voting_Details + 'VotingTabFile' + search + '_' + str(answ) + '.txt'

tabFile = open(newString, 'w')

countryList = ['AFGHANISTAN','ALBANIA','ALGERIA','ANDORRA','ANGOLA','ANTIGUA AND BARBUDA','ARGENTINA','ARMENIA',
                'AUSTRALIA','AUSTRIA','AZERBAIJAN','BAHAMAS','BAHRAIN','BANGLADESH','BARBADOS','BELARUS',
                'BELGIUM','BELIZE','BENIN','BHUTAN','BOLIVIA (PLURINATIONAL STATE OF)','BOSNIA AND HERZEGOVINA',
                'BOTSWANA','BRAZIL','BRUNEI DARUSSALAM','BULGARIA','BURKINA FASO','BURUNDI','CABO VERDE','CAMBODIA',
                'CAMEROON','CANADA','CENTRAL AFRICAN REPUBLIC','CHAD','CHILE','CHINA','COLOMBIA','COMOROS',
                'CONGO','COSTA RICA',"COTE D'IVOIRE",'CROATIA','CUBA','CYPRUS','CZECH REPUBLIC',
                "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",'DEMOCRATIC REPUBLIC OF THE CONGO','DENMARK','DJIBOUTI','DOMINICA',
                'DOMINICAN REPUBLIC','ECUADOR','EGYPT','EL SALVADOR','EQUATORIAL GUINEA','ERITREA','ESTONIA',
                'ETHIOPIA','FIJI','FINLAND','FRANCE','GABON','GAMBIA','GEORGIA','GERMANY','GHANA','GREECE',
                'GRENADA','GUATEMALA','GUINEA','GUINEA-BISSAU','GUYANA','HAITI','HONDURAS','HUNGARY','ICELAND',
                'INDIA','INDONESIA','IRAN (ISLAMIC REPUBLIC OF)','IRAQ','IRELAND','ISRAEL','ITALY','JAMAICA',
                'JAPAN','JORDAN','KAZAKHSTAN','KENYA','KIRIBATI','KUWAIT','KYRGYZSTAN',
                "LAO PEOPLE'S DEMOCRATIC REPUBLIC",'LATVIA','LEBANON','LESOTHO','LIBERIA','LIBYA','LIECHTENSTEIN',
                'LITHUANIA','LUXEMBOURG','MADAGASCAR','MALAWI','MALAYSIA','MALDIVES','MALI','MALTA',
                'MARSHALL ISLANDS','MAURITANIA','MAURITIUS','MEXICO','MICRONESIA (FEDERATED STATES OF)','MONACO',
                'MONGOLIA','MONTENEGRO','MOROCCO','MOZAMBIQUE','MYANMAR','NAMIBIA','NAURU','NEPAL','NETHERLANDS',
                'NEW ZEALAND','NICARAGUA','NIGER','NIGERIA','NORWAY','OMAN','PAKISTAN','PALAU','PANAMA',
                'PAPUA NEW GUINEA','PARAGUAY','PERU','PHILIPPINES','POLAND','PORTUGAL','QATAR','REPUBLIC OF KOREA',
                'REPUBLIC OF MOLDOVA','ROMANIA','RUSSIAN FEDERATION','RWANDA','SAINT KITTS AND NEVIS','SAINT LUCIA',
                'SAINT VINCENT AND THE GRENADINES','SAMOA','SAN MARINO','SAO TOME AND PRINCIPE','SAUDI ARABIA','SENEGAL',
                'SERBIA','SEYCHELLES','SIERRA LEONE','SINGAPORE','SLOVAKIA','SLOVENIA','SOLOMON ISLANDS','SOMALIA',
                'SOUTH AFRICA','SOUTH SUDAN','SPAIN','SRI LANKA','SUDAN','SURINAME','SWAZILAND','SWEDEN',
                'SWITZERLAND','SYRIAN ARAB REPUBLIC','TAJIKISTAN','THAILAND','THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA',
                'TIMOR-LESTE','TOGO','TONGA','TRINIDAD AND TOBAGO','TUNISIA','TURKEY','TURKMENISTAN','TUVALU',
                'UGANDA','UKRAINE','UNITED ARAB EMIRATES','UNITED KINGDOM','UNITED REPUBLIC OF TANZANIA','UNITED STATES',
                'URUGUAY','UZBEKISTAN','VANUATU','VENEZUELA (BOLIVARIAN REPUBLIC OF)','VIET NAM','YEMEN','ZAMBIA','ZIMBABWE']

tabFile.write('UN Resolution Number')

for name in countryList:
    tabFile.write('\t')
    tabFile.write(name)
tabFile.write('\n')

dis = 0
for file in glob.glob('*.txt'):
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
            if line[:2] == 'Y ' or line[:2] == 'y ':
                countryName = line[2:]
                voteCode = '1'
            elif line[:2] == 'N ':
                countryName = line[2:]
                voteCode = '3'
            elif line[:2] == 'A ':
                countryName = line[2:]
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

#### start of part 3

os.chdir(Resolutions_Directory)

newString2 = Resolutions_Directory + 'ResolutionTabFile' + search + '_' + str(answ) + '.txt'

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

for file in glob.glob('*.txt'):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    
    caseReport = {'UN Resolution Symbol:':'', 'Link To:':'', 'Meeting Symbol:':'', 'Title:':'', 'Related Document:':'', 'Vote Notes:':'', 'Voting Summary:':'', 'Vote Date:':'', 'Agenda Information:':''}

    for line in lines:
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
newString3 = path + 'VOTING_DETAILS_OUTPUT' + '_' + search + '_' + str(answ) + '.csv'
in_txt = csv.reader(open(newString, 'r'), delimiter = '\t')
out_csv = csv.writer(open(newString3, 'w'))
out_csv.writerows(in_txt)

ccList = [700,339,615,232,540,58,160,371,900,305,373,31,692,771,53,370,211,80,434,760,145,346,571,140,835,355,439,516,402,811,471,20,482,483,155,710,100,581,484,94,437,344,40,352,316,731,490,390,522,54,42,130,651,92,411,531,366,530,950,375,220,481,420,372,255,452,350,55,90,438,404,110,41,91,310,395,750,850,630,645,205,666,325,51,740,663,705,501,946,690,703,812,367,660,570,450,620,223,368,212,580,553,820,781,432,338,983,435,590,70,987,221,712,341,600,541,775,565,970,790,210,920,93,436,475,385,698,770,986,95,910,150,135,840,290,235,694,732,359,360,365,517,60,56,57,990,331,403,670,433,345,591,451,830,317,349,940,520,560,626,230,780,625,115,572,380,225,652,702,800,342,860,461,955,52,616,640,701,947,500,369,696,200,510,2,165,704,935,101,816,679,551,552]

un = pd.read_csv(newString3, header = None)

un = un.fillna(0)

stringy = open('/Users/brodyvogel/Desktop/Votes2.csv', 'w')

out = csv.writer(stringy)

b = 1
for country in un.iloc[0,:][1:]:
    y = 0
    a = 1
    for x in un.iloc[:, b][1:]:
        countryCode = countryList.index(country)
        countryCode = ccList[countryCode]
        out.writerow([country, countryCode, un.iloc[:,0][y + 1], un.iloc[a, b]])
        y += 1
        a += 1
    b += 1
    
stringy.close()
    
newString4 = path + 'RESOLUTIONS_DETAILS_OUTPUT_' + search + '_' + str(answ) + '.csv'
in_txt2 = csv.reader(open(newString2, 'r'), delimiter = '\t')
out_csv2 = csv.writer(open(newString4, 'w'))
out_csv2.writerow(['UN Resolution Symbol', 'BLANK', 'Meeting Symbol', 'Title', 'Related Documents', 'Vote Notes', 'Results', 'Date', 'Agenda Information'])
for row in in_txt2:
    if row[0] != 'UN Resolution Symbol':
        out_csv2.writerow(row)

### clean up your desktop
#os.remove(Resolutions_Directory)
#os.remove(Voting_Details)
        


