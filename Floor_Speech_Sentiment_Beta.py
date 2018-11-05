#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 10:35:15 2018

@author: vogebr01
"""

#import os
#import nltk
#import nltk.data
#from nltk.corpus import stopwords
#import numpy as np
#import pandas as pd
#import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

new_files = []

path = '/Users/brodyvogel/Box Sync/UNSpeeches'

for path_, subdirs, files in os.walk(path):
    for name in files:
        new_files.append(os.path.join(path_, name))

new_files = [f for f in new_files if '.txt' in f]

sid = SentimentIntensityAnalyzer()

def sentiment_avg(doc, word_list):
    word_indexes = []
    for word in word_list:
        if word in doc:
            word_indexes = word_indexes + [w.start() for w in re.finditer(word, doc)]
    sent = 0
    for w_i in word_indexes:
        if w_i < 300:
            sent = sent + sid.polarity_scores(doc[:(w_i + 300)])['compound']
        else:
            sent = sent + sid.polarity_scores(doc[(w_i - 300):(w_i + 300)])['compound']
    return(sent / len(word_indexes))
        

word_counts = pd.DataFrame({'Session': [], 'Year': [], 'Country Code': [], 'Length': [],
                        'IFIs': [], 'IFIs Sent.': [], 'NIEO': [], 'NIEO Sent.': [], 'IMF': [], 'IMF Sent.': [],
                        'World Bank': [], 'World Bank Sent.': [], 'WTO/GATT':[], 'WTO/GATT Sent.': [],
                        'Investment Arbitration': [], 'Investment Arbitration Sent.': [], 
                        'UNCITRAL':[],'UNCITRAL Sent.': [], 'ICSID': [], 'ICSID Sent.': [],
                        'ICCT': [], 'ICCT Sent.': [], 'UN Human Rights System': [], 'UN Human Rights System Sent.': []})

where_are_we = 1
for file in new_files:
    session = file[46:48]
    year = file[51:55]
    countryCode = file[56:59]
    doc_text = open(file).read().lower()
    doc_text = doc_text.translate(doc_text.maketrans('','','.!;,?'))
    length = len(doc_text.split(' '))
    IFIs_words = ['international financial institution',
               'bretton', 'development bank', 'international economic order']
    IFIs = sum(doc_text.count(word) for word in IFIs_words)
    if IFIs > 0:
        IFIsSent = sentiment_avg(doc_text, IFIs_words)
    else:
        IFIsSent = None
    NIEO_words = ['neoliberal', 'neo-liberal', 'structural adjustment',
               'washington consensus', 'structural reform', 'conditionality', 'debt management',
               'hipc', 'indebted poor countries', 'highly indebted', 'highly-indebted', 'algiers conference',
               'heavily indebted', 'heavily-indebted']
    NIEO = sum(doc_text.count(word) for word in NIEO_words)
    if NIEO > 0:
        NIEOSent = sentiment_avg(doc_text, NIEO_words)
    else:
        NIEOSent = None
    IMF_words = ['international monetary fund', ' imf ', 'special drawing rights']
    IMF = sum(doc_text.count(word) for word in IMF_words)
    if IMF > 0:
        IMFSent = sentiment_avg(doc_text, IMF_words)
    else:
        IMFSent = None
    WB_words = ['world bank', 'international bank for reconstruction',
             'international development association', 'international finance corporation', 'ibrd', ' ida ', 'ifc']
    WB = sum(doc_text.count(word) for word in WB_words)
    if WB > 0:
        WBSent = sentiment_avg(doc_text, WB_words)
    else:
        WBSent = None
    WTO_words = ['world trade organization', 'world trade organisation', ' wto ', 'agreement on tariffs',
              'gatt', 'doha round', 'uruguay round', 'trade round', 'doha agenda', 'intellectual property rights', 'tariffs', 'tariff',
              'most favored nation', 'most favoured nation']
    WTO = sum(doc_text.count(word) for word in WTO_words)
    if WTO > 0:
        WTOSent = sentiment_avg(doc_text, WTO_words)
    else:
        WTOSent = None
    IA_words = ['arbitration', 'arbitral', 'investment treaty', 'investor-state dispute settlement', 'isds',
             'investor dispute']
    IA = sum(doc_text.count(word) for word in IA_words)
    if IA > 0:
        IASent = sentiment_avg(doc_text, IA_words)
    else:
        IASent = None
    UNC_words = ['hull rule', 'expropriation', 'investor award', 'investment award']
    UNC = sum(doc_text.count(word) for word in UNC_words)
    if UNC > 0:
        UNCSent = sentiment_avg(doc_text, UNC_words)
    else:
        UNCSent = None
    ICSID_words = ['investment ruling', 'bilateral investment treaty', 'international chamber of commerce', 
                'permanent court of arbitration', ' pca ']
    ICSID = sum(doc_text.count(word) for word in ICSID_words)
    if ICSID > 0:
        ICSIDSent = sentiment_avg(doc_text, ICSID_words)
    else:
        ICSIDSent = None
    ICCT_words = ['international criminal court', ' icc ', ' icty ', ' ictr ', 'criminal tribunal',
               'rome treaty', 'special court', 'special tribunal', 'court for sierra leone', 'sierra leone tribunal', 'court for cambodia',
               'tribunal for cambodia', 'tribunal for lebanon', 'lebanon tribunal']
    ICCT = sum(doc_text.count(word) for word in ICCT_words)
    if ICCT > 0:
        ICCTSent = sentiment_avg(doc_text, ICCT_words)
    else:
        ICCTSent = None
    UNHR_words = ['human rights treaty', 'human rights council', 'human rights committee', 'universal periodic review',
               ' upr ', 'iccpr', 'cedaw', 'convention against torture', 'human rights convention', 'cescr', 'ohchr', 'committee on economic social',
               'committee against torture', 'convention against torture', 'prevention of torture', 'rights of the child', 'committee on migrant workers',
               'rights of persons with disabilities', 'committee on enforced disappearances', 'covenant on economic']
    UNHR = sum(doc_text.count(word) for word in UNHR_words)
    if UNHR > 0:
        UNHRSent = sentiment_avg(doc_text, UNHR_words)
    else:
        UNHRSent = None
    to_append = pd.DataFrame([[session, year, countryCode, length, IFIs, IFIsSent, NIEO, NIEOSent, IMF, IMFSent,
                               WB, WBSent, WTO, WTOSent, IA, IASent, UNC, UNCSent, ICSID, ICSIDSent, 
                               ICCT, ICCTSent, UNHR, UNHRSent]], 
                             columns = ['Session', 'Year', 'Country Code', 'Length', 'IFIs', 'IFIs Sent.', 'NIEO', 'NIEO Sent.',
                                        'IMF', 'IMF Sent.', 'World Bank', 'World Bank Sent.', 'WTO/GATT', 'WTO/GATT Sent.',
                                        'Investment Arbitration', 'Investment Arbitration Sent.', 'UNCITRAL', 'UNCITRAL Sent.',
                                        'ICSID', 'ICSID Sent.', 'ICCT', 'ICCT Sent.', 'UN Human Rights System', 'UN Human Rights System Sent.'])
    word_counts = word_counts.append(to_append)
    print(where_are_we)
    where_are_we += 1
 