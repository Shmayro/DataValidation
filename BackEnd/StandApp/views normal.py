import string
import csv
import os
import time
import cProfile
from typing import Any
from django import template
import requests
import unicodedata
import numpy as np
import re
import json
import pandas as pd
import webbrowser
from pathlib import Path
from pymongo import MongoClient
from django.template import Context, loader
from django.shortcuts import render, redirect
import dask.dataframe as dd
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
#from pandas_profiling import ProfileReport
import asyncio
import multiprocessing
from pyspark import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.functions import array
from joblib import Parallel, delayed
import matplotlib

matplotlib.use('agg')

# input file
# df = pd.read_csv(r'Input.csv')

# liste des villes
dfcity = pd.read_csv(r'city_list.csv')

# fichier contenant la liste des abbreviations des mots cles d'adresses
json_data = open(r'abbreviation.json',encoding='utf-8')

# récupérer la liste des villes


def get_list_city(df):
    cityL = []
    for i in range(0, len(df)):
        cityL.insert(i, df['CITY'][i])
    return cityL


############## Gestion des abbreviations ###################

data = json.load(json_data)
streetabbrev = data['Abbreviation']['StreetAbbrev'][2]['Abbrev']
abb = []
comp = []
for i in range(0, len(streetabbrev)):
    abb.insert(i, streetabbrev[i]['abbreviation'].upper())

for i in range(0, len(streetabbrev)):
    comp.insert(i, streetabbrev[i]['name'].upper())

# récupérer le nom complet d'une abbréviation passée en paramètre


def nomcomplet(word):
    if word in abb:
        k = 0
        T = False
        while k < len(abb) and T == False:
            if word == abb[k]:
                complet = comp[k]
                T = True
                return complet
            else:
                k = k + 1
    else:
        return word


# récupérer le nombre d'abbréviation trouvée dans une adresse passé en paramètre


def abbreviation(Address):
    nb = 0
    Address = Address.replace(',', ' ')
    Address = re.sub("\s\s+", " ", Address)
    Address = Address.strip()
    Add = Address
    tab = Add.split()
    for j in range(0, len(tab)):
        N = nomcomplet(tab[j])
        if N != tab[j]:
            nb = nb + 1
            tab[j] = N
    addr = ' '.join(str(x) for x in tab)
    Address = addr.strip()
    Address = re.sub('\s+', ' ', Address)
    LL = []
    LL.insert(0, Address)
    LL.insert(1, nb)
    return LL


################ Gestion des Erreurs Typographique ##################

keywordlist = [
    'ESPLANADE', 'AVENUE', 'CHEMIN', 'BOULEVARD', 'RUE', 'BLVD', 'BLD',
    'ROUTES', 'IMPASSE', 'PASSAGE', 'PLACE', 'COURS', 'CHAUSSEE', 'TRAVERSE',
    'LIEUDIT', 'PROMENADE', 'RPT', 'CENTRE', 'IMMEUBLE', 'RESIDENCE',
    'VILLAGE', 'CTRE', 'BATIMENT', 'TERMINAL', 'ZONE', 'ETAGE', 'BUILDING',
    'QUAI', 'CEDEX', 'PARC', 'AEROGARE', 'EUROAIRPORT', 'Z.I.', 'B.P.',
    'EUROFRET', 'MOLE', 'TECHNOPARC', 'HOTEL', 'PARC', 'LOTISSEMENT', 'BAT.',
    'ECOPOLE', 'DOMAINE', 'CARGOPORT', 'ATRIUM', 'PARIS', 'CIDEX', 'NUMBER',
    'B.P', 'RSIDENCE', 'BP', 'CS', 'CEDEX', 'CD'
]

#


def checkstickword(tab):
    LL = []
    tab1 = tab
    for j in range(0, len(tab)):
        if tab[j].isdigit() == False and len(tab[j]) > 2:
            f = 0
            T = False
            while f < len(keywordlist) and T == False:
                if tab[j] != 'RUEIL':
                    ind = tab[j].find(keywordlist[f])
                    ll = len(tab[j])
                    lkey = len(keywordlist[f])
                    if ind == 0:
                        T = True
                        x = tab[j]
                        y = x[0:lkey] + ' ' + x[lkey:]
                        tab[j] = y
                    elif ind > 0 and ind == ll - lkey:
                        T = True
                        x = tab[j]
                        y = x[0:ind] + ' ' + x[ind:]
                        tab[j] = y
                    else:
                        f = f + 1
                else:
                    f = f + 1
        else:
            pass
        ad = ' '.join(str(x) for x in tab)
        tab2 = ad.split()
        Diff = len(tab2) - len(tab1)
        LL.insert(0, ad)
        LL.insert(1, Diff)
        return LL


#


def separateNum(tab):
    LL = []
    tab1 = tab
    for j in range(0, len(tab)):
        if tab[j].isdigit() == False and len(tab[j]) > 2:
            F = str(filter(str.isdigit, tab[j]))
            S = tab[j].replace(F, ' ')
            S = re.sub("\s\s+", " ", S)
            S = S.strip()
            lnum = len(F)
            ll = len(tab[j])
            x = tab[j]
            if x != F and S not in [
                    'BIS', 'TER', 'QUATER', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                    'Q', 'T'
            ]:
                ind = x.find(F)
                if ind == 0:
                    tab[j] = x[0:lnum] + ' ' + x[lnum:]
                elif ind > 0 and ind == ll - lnum:
                    tab[j] = x[0:ind] + ' ' + x[ind:]
                elif ind > 0 and ind != ll - lnum:
                    tab[j] = x[0:ind] + ' ' + F + ' ' + x[ind + lnum:]
    ad = ' '.join(str(x) for x in tab)
    tab2 = ad.split()
    Diff = len(tab2) - len(tab1)
    LL.insert(0, ad)
    LL.insert(1, Diff)
    return LL


def bdrules(tab):
    TT = False
    j = 0
    tab1 = tab
    LL = []
    while j < len(tab) and TT == False:
        if tab[j].isdigit() == False and len(tab[j]) > 1:
            ll = len(tab[j])
            ind = tab[j].find('BP')
            if ind == 0:
                x = tab[j]
                y = x[0:2] + ' ' + x[2:]
                tab[j] = y
                TT = True
                ad = ' '.join(str(x) for x in tab)
            elif ind == ll - 2:
                x = tab[j]
                y = x[0:ind] + ' ' + x[ind:]
                tab[j] = y
                TT = True
                ad = ' '.join(str(x) for x in tab)
            elif ind > 0 and ind != ll - 2:
                # nb=nb+1
                x = tab[j]
                y = x[0:ind] + ' ' + 'BP' + ' ' + x[ind + 2:]
                tab[j] = y
                TT = True
                ad = ' '.join(str(x) for x in tab)
            else:
                j = j + 1
        else:
            j = j + 1
    ad2 = ' '.join(str(x) for x in tab)
    tab2 = ad2.split()
    Diff = len(tab2) - len(tab1)
    LL.insert(0, ad2)
    LL.insert(1, Diff)
    return LL


def typoerrorcorrection(Address):
    cc = 0
    if "A EROGARE" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            if Ta[k] == 'A':
                T = True
                h = 'AEROGARE'
                Ta[k] = h
                Ta[k + 1] = ''
                ad = ' '.join(str(x) for x in Ta)
                ad2 = re.sub('\s+', ' ', ad)
                Address = ad2
            else:
                k = k + 1
    if "A ROGARE" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            if Ta[k] == 'A':
                T = True
                h = 'AEROGARE'
                Ta[k] = h
                Ta[k + 1] = ''
                ad = ' '.join(str(x) for x in Ta)
                ad2 = re.sub('\s+', ' ', ad)
                Address[i] = ad2
            else:
                k = k + 1
    if "A EROPORT" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            if Ta[k] == 'A':
                T = True
                h = 'AEROPORT'
                Ta[k] = h
                Ta[k + 1] = ''
                ad = ' '.join(str(x) for x in Ta)
                ad2 = re.sub('\s+', ' ', ad)
                Address = ad2
            else:
                k = k + 1
    if "A ROPORT" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            try:
                if Ta[k] == 'A':
                    T = True
                    h = 'AEROPORT'
                    Ta[k] = h
                    Ta[k + 1] = ''
                    ad = ' '.join(str(x) for x in Ta)
                    ad2 = re.sub('\s+', ' ', ad)
                    Address = ad2
                else:
                    k = k + 1
            except:
                k = k + 1
    if "B ATIMENT" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            if Ta[k] == 'B':
                T = True
                h = 'BATIMENT'
                Ta[k] = h
                Ta[k + 1] = ''
                ad = ' '.join(str(x) for x in Ta)
                ad2 = re.sub('\s+', ' ', ad)
                Address = ad2
            else:
                k = k + 1
    if "B TIMENT" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            try:
                if Ta[k] == 'B':
                    T = True
                    h = 'BATIMENT'
                    Ta[k] = h
                    Ta[k + 1] = ''
                    ad = ' '.join(str(x) for x in Ta)
                    ad2 = re.sub('\s+', ' ', ad)
                    Address = ad2
                else:
                    k = k + 1
            except:
                k = k + 1
    if "Z I" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            try:
                if Ta[k] == 'Z':
                    T = True
                    h = 'ZI'
                    Ta[k] = h
                    Ta[k + 1] = ''
                    ad = ' '.join(str(x) for x in Ta)
                    ad2 = re.sub('\s+', ' ', ad)
                    Address = ad2
                else:
                    k = k + 1
            except:
                k = k + 1
    if "Z A" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            try:
                if Ta[k] == 'Z':
                    T = True
                    h = 'ZA'
                    Ta[k] = h
                    Ta[k + 1] = ''
                    ad = ' '.join(str(x) for x in Ta)
                    ad2 = re.sub('\s+', ' ', ad)
                    Address = ad2
                else:
                    k = k + 1
            except:
                k = k + 1
    if "C O" in Address:
        cc = cc + 1
        V1 = Address
        Ta = V1.split()
        k = 0
        T = False
        while k < len(V1) and T == False:
            try:
                if Ta[k] == 'C':
                    T = True
                    h = 'CO'
                    Ta[k] = h
                    Ta[k + 1] = ''
                    ad = ' '.join(str(x) for x in Ta)
                    ad2 = re.sub('\s+', ' ', ad)
                    Address = ad2
                else:
                    k = k + 1
            except:
                k = k + 1

    street2 = []
    V = Address
    tab = V.split()
    final = checkstickword(tab)[0]
    tab2 = final.split()
    final2 = bdrules(tab2)[0]
    tab3 = final2.split()
    final3 = separateNum(tab3)[0]
    final3 = final3.strip()
    final3 = re.sub('\s+', ' ', final3)
    nbtot = checkstickword(tab)[1] + bdrules(tab2)[1] + separateNum(tab3)[1]
    final4 = []
    final4.insert(0, final3)
    final4.insert(1, nbtot)
    return final4


############### Parsing ##############


def numT(s):
    return any(i.isdigit() for i in s)


ROADKEY = [
    'AUTOROUTE', 'D', 'LIEUX-DITS', 'LIEUX-DIT', 'LIEU-DIT', 'RD', 'BL',
    'ALLEES', 'MONTE', 'ALLES', 'AVNUE', 'PASSAGE', 'HAMEAU', 'ESPLANADE',
    'ROAD', 'QUAI', 'BOULEVARD', 'RUE', 'AVENUE', 'CHEMIN', 'IMPASSE', 'PLACE',
    'ROUTE', 'ALLEE', 'COURS', 'VOIE', 'CHAUSSE', 'CHAUSSEE', 'TRAVERSE',
    'LIEUDIT', 'PROMENADE', 'SQUARE', 'COTEAU', 'TERRE', 'CARREFOUR', 'CLOS',
    'BALCON', 'CAVEE', 'BOUCLE', 'ROUTES', 'PARVIS', 'LIEU', 'ALLE', 'CD'
]
HOUSEKEY = [
    'AERODROME', 'ATRIUM', 'EUROFRET', 'MOLE', 'TECHNOPARC', 'HOTEL', 'CS',
    'CASE', 'B.P.', 'AIRPORT', 'ZA', 'ZAC', 'ZONE', 'PARC', 'BATIMENT',
    'IMMEUBLE', 'CITE', 'PARK', 'ZI', 'AEROPORT', 'LOTISSEMENT', 'BP', 'ZL',
    'CE', 'BAT1', 'ENTREPOT', 'CHATEAU', 'TERMINAL', 'RESIDENCE', 'Z.A.C.',
    'CS', 'ZAE', 'PA', 'BAT.', 'ECOPOLE', 'DOMAINE', 'CENTRE', 'CARGOPORT',
    'BP', 'PO', 'BUREAU', 'ETAGE', 'APPARTEMENT', 'RSIDENCE', 'DOMAINE', 'ZAL',
    'QUARTIER', 'P.A.', 'PLATE-FORME'
]

LKEY = [
    'LIEUX-DIT', 'AUTOROUTE', 'FERME', 'LIEUX-DITS', 'LIEU-DIT', 'RD', 'USINE',
    'CS', 'CD', 'ALLE', 'ROUTES', 'AERODROME', 'ESPLANADE', 'ROAD', 'QUAI',
    'BOULEVARD', 'RUE', 'AVENUE', 'CHEMIN', 'IMPASSE', 'PLACE', 'ROUTE',
    'ALLEE', 'COURS', 'VOIE', 'CHAUSSE', 'CHAUSSEE', 'TRAVERSE', 'LIEUDIT',
    'PROMENADE', 'ENTREE', 'GATE', 'PORTE', 'BAT.', 'BATIMENT', 'BUILDING',
    'TOUR', 'IMMEUBLE', 'RESIDENCE', 'MOLE', 'AEROGARE', 'GARE', 'ENTREPOT',
    'CARGOPORT', 'PORT', 'AIRPORT', 'AEROPORT', 'EUROAIRPORT', 'EUROFRET',
    'TECHNOPARC', 'PARK', 'CENTRE', 'PARC', 'DOMAINE', 'ZONE', 'ZL', 'ZIF',
    'ZAE', 'Z.I.P.', 'Z.A.C.', 'ZAC', 'PA', 'Z.A.C', 'ZI', 'Z.I.', 'P.A.'
    'ZA', 'BP', 'PO', 'C/O', 'APPARTEMENT', 'ETAGE', 'BUREAU', 'ATRIUM',
    'RSIDENCE', 'PLA', 'DEPOT', 'HANGAR', 'ACTIPOLE', 'MIN', 'DOMAINE',
    'ALLEES', 'ZAL', 'QUARTIER', 'BL', 'VILLAGE', 'POLE', 'TECHNOPOLE'
]

L0KEY = ['GATE', 'PORTE', 'BUREAU', 'ETAGE', 'APPARTEMENT', 'ATRIUM', 'RDC']
L1KEY = [
    'BT', 'BAT.', 'BATIMENT', 'BUILDING', 'TOUR', 'ENTREE', 'BT.', 'PLA',
    'ILOT'
]
L2KEY = [
    'IMMEUBLE', 'RESIDENCE', 'MOLE', 'LOTISSEMENT', 'RSIDENCE', 'ENTREPOT',
    'DEPOT', 'HANGAR', 'USINE'
]
L3KEY = ['AEROGARE', 'GARE', 'AERODROME', 'EUROGARE', 'ARODROME']
L4KEY = ['CARGOPORT', 'PORT']
L5KEY = ['AIRPORT', 'AEROPORT', 'EUROAIRPORT', 'TERMINAL', 'AROPORT']
L6KEY = [
    'EUROFRET', 'TECHNOPARC', 'PARK', 'CENTRE', 'PARC', 'DOMAINE', 'ZONE',
    'ZL', 'ZIF', 'ZAE', 'Z.I.P.', 'Z.A.C.', 'ZAC', 'PA', 'Z.A.C', 'ZI', 'Z.I.',
    'ZA', 'RVSL', 'FORUM', 'ACTIPOLE', 'MIN', 'ECOPARC', 'MARCHE', 'ZIL',
    'PLATEFORME', 'ZCI', 'DOMAINE', 'ZAL', 'QUARTIER', 'VILLAGE', 'POLE',
    'TECHNOPOLE', 'P.A.', 'FERME', 'PLATE-FORME'
]
L7KEY = ['BP', 'PO', 'B.P.', 'B.P', 'CS', 'C.S', 'TSA']
L8KEY = ['C/O']


def L0Search(L):
    RB = False
    k = 0
    pos = -1
    while k < len(L) and RB == False:
        if L[k] in L0KEY:
            RB = True
            pos = k
        else:
            k = k + 1
    return pos


def L1Search(L):
    RB = False
    k = 0
    pos = -1
    while k < len(L) and RB == False:
        if L[k] in L1KEY:
            RB = True
            pos = k
        else:
            k = k + 1
    return pos


def L2Search(L):
    RB = False
    k = 0
    pos = -1
    while k < len(L) and RB == False:
        if L[k] in L2KEY:
            RB = True
            pos = k
        else:
            k = k + 1
    return pos


def L3Search(L):
    k = 0
    pos = -1
    L2 = []
    for i in range(0, len(L)):
        if L[i] in L3KEY:
            L2.insert(k, i)
            k = k + 1
    if L2 == []:
        return pos
    elif len(L2) == 1:
        return L2[0]
    else:
        return L


def L4Search(L):
    RB = False
    k = 0
    pos = -1
    while k < len(L) and RB == False:
        if L[k] in L4KEY:
            RB = True
            pos = k
        else:
            k = k + 1
    return pos


def L5Search(L):
    RB = False
    k = 0
    pos = -1
    while k < len(L) and RB == False:
        if L[k] in L5KEY:
            RB = True
            pos = k
        else:
            k = k + 1
    return pos


def L6Search(L):
    k = 0
    pos = -1
    L2 = []
    for i in range(0, len(L)):
        if L[i] in L6KEY:
            L2.insert(k, i)
            k = k + 1
    if L2 == []:
        return pos
    elif len(L2) == 1:
        return L2[0]
    else:
        return L2


def L7Search(L):
    RB = False
    k = 0
    pos = -1
    while k < len(L) and RB == False:
        if L[k] in L7KEY:
            RB = True
            pos = k
        else:
            k = k + 1
    return pos


def poselement(Lpos, elem):
    try:
        pos = Lpos.index(elem)
    except:
        pos = -1
    return pos


def ROADSearch(L):
    RB = False
    k = 0
    pos = -1
    while k < len(L) and RB == False:
        if L[k] in ROADKEY:
            RB = True
            pos = k
        else:
            k = k + 1
    return pos


def HouseSearch(L):
    HB = False
    k = 0
    pos = -1
    LI = []
    for i in range(0, len(L)):
        if L[i] in HOUSEKEY:
            LI.insert(k, i)
    return LI


def ExtractLocality(Addr, dfcity):
    Addr = Addr.upper()
    Lfinal = []
    TT = False
    L = Addr.split()
    FF = False
    TOTO = False
    pos = []
    t = 0
    ZipCode = 'NONE'
    CITY = 'NONE'
    Country = 'NONE'
    cityL = get_list_city(dfcity)
    if len(Addr.split()) == 1:
        if Addr in cityL:

            Lfinal.insert(0, 'NONE')
            Lfinal.insert(1, Addr)
            Lfinal.insert(2, 'NONE')
            Lfinal.insert(3, Addr)
            return Lfinal
    else:
        for j in range(0, len(L)):
            if L[j].isdigit():
                if len(L[j]) == 5 and L[j - 1] != 'BP' and L[
                        j - 1] != 'PO' and L[j - 1] != 'BOX':

                    ZipCode = L[j]
                    TOTO = True
                    pos.insert(t, j)
                    t = t + 1
                    try:
                        C = L[j + 1] + ' ' + L[j + 2]+' ' + \
                            L[j + 3] + ' ' + L[j + 4] + ' ' + L[j + 5]
                        FF = False
                        k = 0
                        while k < len(cityL) and FF == False:
                            if C == cityL[k]:
                                FF = True
                                D = L[j + 1] + ' ' + L[j + 2] + ' ' + \
                                    L[j + 3] + ' ' + L[j + 4] + ' ' + L[j + 5]
                                CITY = D
                            else:
                                k = k + 1
                    except:
                        pass

                    if FF == False:
                        try:
                            C = L[j + 1] + ' ' + L[j + 2] + \
                                ' ' + L[j + 3] + ' ' + L[j + 4]
                            FF = False
                            k = 0
                            while k < len(cityL) and FF == False:
                                if C == cityL[k]:
                                    FF = True
                                    D = L[j + 1] + ' ' + L[j + 2] + \
                                        ' ' + L[j + 3] + ' ' + L[j + 4]
                                    CITY = D
                                else:
                                    k = k + 1
                        except:
                            pass

                    if FF == False:
                        try:
                            C = L[j + 1] + ' ' + L[j + 2] + ' ' + L[j + 3]
                            FF = False
                            k = 0
                            while k < len(cityL) and FF == False:
                                if C == cityL[k]:
                                    FF = True
                                    D = L[j + 1] + ' ' + \
                                        L[j + 2] + ' ' + L[j + 3]
                                    CITY = D
                                else:
                                    k = k + 1
                        except:
                            pass

                    if FF == False:
                        try:
                            C = L[j + 1] + ' ' + L[j + 2]
                            FF = False
                            k = 0
                            while k < len(cityL) and FF == False:
                                if C == cityL[k]:
                                    FF = True
                                    D = L[j + 1] + ' ' + L[j + 2]
                                    CITY = D
                                else:
                                    k = k + 1
                        except:
                            pass
                    if FF == False:
                        try:
                            C = L[j + 1]
                            FF = False
                            k = 0
                            while k < len(cityL) and FF == False:
                                if C == cityL[k]:
                                    FF = True
                                    CITY = L[j + 1]
                                else:
                                    k = k + 1
                        except:
                            pass
        if FF == False:
            CITY = 'NONE'

        leng = len(L)
        C = leng - 1
        C1 = leng - 2
        if L[C] == 'FRANCE':
            Country = 'FRANCE'
            pos.insert(t, leng - 1)
            t = t + 1
        elif L[C1] == 'FRANCE':
            Country = 'FRANCE'
            pos.insert(t, leng - 2)
            t = t + 1
        else:
            Country = 'NONE'
        if ZipCode != 'NONE' and CITY != 'NONE' and Country != 'NONE':
            C = ZipCode + ' ' + CITY + ' ' + Country
            Addr = Addr.replace(C, ' ')
        elif CITY != 'NONE' and Country != 'NONE':
            C = CITY + ' ' + Country
            Addr = Addr.replace(C, ' ')
        elif ZipCode != 'NONE' and Country != 'NONE':
            C = ZipCode + ' ' + Country
            Addr = Addr.replace(C, ' ')
        elif ZipCode != 'NONE' and CITY != 'NONE' and Country == 'NONE':
            C = ZipCode + ' ' + CITY
            Addr = Addr.replace(C, ' ')
        elif ZipCode == 'NONE' and CITY != 'NONE' and Country == 'NONE':
            C = CITY
            Addr = Addr.replace(C, ' ')
    Addr = re.sub("\s\s+", " ", Addr)
    Addr = Addr.strip()
    Lfinal.insert(0, ZipCode)
    Lfinal.insert(1, CITY)
    Lfinal.insert(2, Country)
    Lfinal.insert(3, Addr)
    return Lfinal


def ParsingROAD(Addr):
    Laddress = []
    R = ExtractLocality(Addr, dfcity)
    Address = R[3]
    Address = Address.replace(',', ' ')
    Address = re.sub("\s\s+", " ", Address)
    Address = Address.strip()
    L = Address.split()
    PR = ROADSearch(L)
    PH = HouseSearch(L)
    L2 = []
    y = 0
    ROAD = 'NONE'
    if PR != -1:
        if PR == 0:

            if PH == []:
                ROAD = Address
            else:
                PH2 = sorted(PH)
                for j in range(0, PH2[0]):
                    L2.insert(y, L[j])
                    y = y + 1
                ROAD = " ".join(str(x) for x in L2)
        ######################################################
        elif PR > 0 and L[PR - 1].isdigit() == False and filter(
                str.isdigit, L[PR - 1]) != '':
            if PH == []:
                for j in range(PR - 1, len(L)):
                    L2.insert(y, L[j])
                    y = y + 1
                ROAD = " ".join(str(x) for x in L2)
            else:
                PH2 = sorted(PH)
                PH2.insert(len(PH2), PR - 1)
                PH2.insert(len(PH2), len(L))
                PH3 = sorted(PH2)
                IND = PH3.index(PR - 1)
                for j in range(PH3[IND], PH3[IND + 1]):
                    L2.insert(y, L[j])
                    y = y + 1
                ROAD = " ".join(str(x) for x in L2)
        ########################################################
        elif (PR > 0 and L[PR - 1] in [
                'BIS', 'TER', 'QUATER', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'Q',
                'T'
        ] and (L[PR - 2].isdigit() == True)):
            if PH == []:
                for j in range(PR - 2, len(L)):
                    L2.insert(y, L[j])
                    y = y + 1
                ROAD = " ".join(str(x) for x in L2)
            else:
                PH2 = sorted(PH)
                PH2.insert(len(PH2), PR - 2)
                PH2.insert(len(PH2), len(L))
                PH3 = sorted(PH2)
                IND = PH3.index(PR - 2)
                for j in range(PH3[IND], PH3[IND + 1]):
                    L2.insert(y, L[j])
                    y = y + 1
                ROAD = " ".join(str(x) for x in L2)

        elif (PR > 0 and L[PR - 1].isdigit() == False and L[PR - 1] != 'EME'):
            if PH == []:
                for j in range(PR, len(L)):
                    L2.insert(y, L[j])
                    y = y + 1
                ROAD = " ".join(str(x) for x in L2)
            else:
                PH2 = sorted(PH)
                if PR > PH2[len(PH2) - 1]:
                    for j in range(PR, len(L)):
                        L2.insert(y, L[j])
                        y = y + 1
                    ROAD = " ".join(str(x) for x in L2)
                elif PR < PH2[len(PH2) - 1] and PR > PH2[0]:
                    PH.insert(len(PH), PR)
                    PH6 = sorted(PH)
                    II = PH6.index(PR) + 1
                    for j in range(PR, PH6[II]):
                        L2.insert(y, L[j])
                        y = y + 1
                    ROAD = " ".join(str(x) for x in L2)
                elif PR < PH2[0]:
                    for j in range(PR, PH2[0]):
                        L2.insert(y, L[j])
                        y = y + 1
                    ROAD = " ".join(str(x) for x in L2)
        elif PR > 0 and L[PR - 1] == 'EME' and L[PR - 2].isdigit() == True:
            ROAD = L[PR - 2] + ' ' + L[PR - 1] + ' ' + L[PR]
        else:

            if (L[PR - 1].isdigit() == True):
                if PH == []:
                    for j in range(PR - 1, len(L)):
                        L2.insert(y, L[j])
                        y = y + 1
                    ROAD = " ".join(str(x) for x in L2)
                else:
                    PH2 = sorted(PH)
                    PH2.insert(len(PH2), PR - 1)
                    PH2.insert(len(PH2), len(L))
                    PH3 = sorted(PH2)
                    IND = PH3.index(PR - 1)
                    for j in range(PH3[IND], PH3[IND + 1]):
                        L2.insert(y, L[j])
                        y = y + 1
                    ROAD = " ".join(str(x) for x in L2)
            elif (re.sub(r'[^\w\s]', '', L[PR - 1])).isdigit() == True:
                if PH == []:
                    for j in range(PR - 1, len(L)):
                        L2.insert(y, L[j])
                        y = y + 1
                    ROAD = " ".join(str(x) for x in L2)
                else:
                    PH2 = sorted(PH)
                    PH2.insert(len(PH2), PR - 1)
                    PH2.insert(len(PH2), len(L))
                    PH3 = sorted(PH2)
                    IND = PH3.index(PR - 1)
                    for j in range(PH3[IND], PH3[IND + 1]):
                        L2.insert(y, L[j])
                        y = y + 1
                    ROAD = " ".join(str(x) for x in L2)
        HOUSE = Address.replace(ROAD, ' ')
        HOUSE = re.sub("\s\s+", " ", HOUSE)
        HOUSE = HOUSE.strip()
    else:
        ROAD = 'NONE'
        HOUSE = Address
    Laddress.insert(0, ROAD)
    Laddress.insert(1, HOUSE)
    return Laddress


def ParsingHOUSE(Laddress):
    Lprov = []
    L0 = []
    L1 = []
    L2 = []
    L3 = []
    L4 = []
    L5 = []
    L6 = []
    L7 = []
    Lpos = []
    d = 0
    Li = []
    Lpos2 = []
    L0p = []
    L1p = []
    L2p = []
    L3p = []
    L4p = []
    L5p = []
    L6p = []
    L7p = []
    HOUSE = Laddress[1]
    if HOUSE != 'NONE':
        LH = HOUSE.split()
        Lpos.insert(0, L0Search(LH))
        Lpos.insert(1, L1Search(LH))
        Lpos.insert(2, L2Search(LH))
        Lpos.insert(3, L3Search(LH))
        Lpos.insert(4, L4Search(LH))
        Lpos.insert(5, L5Search(LH))
        Lpos.insert(6, L6Search(LH))
        Lpos.insert(7, L7Search(LH))
        for q in range(0, len(Lpos)):
            Lpos2.insert(q, Lpos[q])
            q = q + 1
        if type(Lpos2[3]) == list:
            C = Lpos2[3]
            d = len(Lpos2)
            Li = Lpos2[3]
            Lpos2[3] = C[0]
            for g in range(1, len(Li)):
                Lpos2.insert(d, Li[g])
                d = d + 1
        elif type(Lpos2[6]) == list:
            C = Lpos2[6]
            d = len(Lpos2)
            Li = Lpos2[6]
            Lpos2[6] = C[0]
            for g in range(1, len(Li)):
                Lpos2.insert(d, Li[g])
                d = d + 1
        Lpos2sort = sorted(Lpos2)
        Lpos2sort2 = []
        u = 0
        for t in range(0, len(Lpos2sort)):
            if Lpos2sort[t] != -1:
                Lpos2sort2.insert(u, Lpos2sort[t])
                u = u + 1
        Lpos2sort2.insert(len(Lpos2sort2), len(LH))
        T = False
        T1 = False
        nb = 0
        nb1 = 0
        LL3 = []
        LL6 = []
        for y in range(0, len(Lpos2sort2) - 1):
            E = Lpos2sort2[y]
            P = poselement(Lpos, E)
            if P != -1:
                Lf = []
                w = 0
                for h in range(Lpos2sort2[y], Lpos2sort2[y + 1]):
                    Lf.insert(w, LH[h])
                    w = w + 1
                S = " ".join(str(x) for x in Lf)
                if P == 0:
                    L0.insert(0, S)
                    L0p.insert(0, S)
                if P == 1:
                    L1.insert(0, S)
                    L1p.insert(0, S)
                if P == 2:
                    L2.insert(0, S)
                    L2p.insert(0, S)
                if P == 3:
                    L3.insert(0, S)
                    L3p.insert(0, S)
                if P == 4:
                    L4.insert(0, S)
                    L4p.insert(0, S)
                if P == 5:
                    L5.insert(0, S)
                    L5p.insert(0, S)
                if P == 6:
                    L6.insert(0, S)
                    L6p.insert(0, S)
                if P == 7:
                    L7.insert(0, S)
                    L7p.insert(0, S)
            if P == -1 and type(Lpos[3]) != list:
                T = True
                Lf = []
                w = 0
                for h in range(Lpos2sort2[y], Lpos2sort2[y + 1]):
                    Lf.insert(w, LH[h])
                    w = w + 1
                S = " ".join(str(x) for x in Lf)
                LL6.insert(nb, S)
                nb = nb + 1
            if P == -1 and type(Lpos[6]) != list:
                T1 = True
                Lf = []
                w = 0
                for h in range(Lpos2sort2[y], Lpos2sort2[y + 1]):
                    Lf.insert(w, LH[h])
                    w = w + 1
                S = " ".join(str(x) for x in Lf)
                LL3.insert(nb1, S)
                nb1 = nb1 + 1
        if T1 == True:
            S = " ".join(str(x) for x in LL3)
            L3.insert(0, S)
            L3p.insert(0, S)
        if T == True:
            S = " ".join(str(x) for x in LL6)
            L6.insert(0, S)
            L6p.insert(0, S)
        Autre = HOUSE
        if L0p == []:
            L0.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L0p[0], ' ')
        if L1p == []:
            L1.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L1p[0], ' ')
        if L2p == []:
            L2.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L2p[0], ' ')
        if L3p == []:
            L3.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L3p[0], ' ')
        if L4p == []:
            L4.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L4p[0], ' ')
        if L5p == []:
            L5.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L5p[0], ' ')
        if L6p == []:
            L6.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L6p[0], ' ')
        if L7p == []:
            L7.insert(0, 'NONE')
        else:
            Autre = Autre.replace(L7p[0], ' ')
        Autre = re.sub("\s\s+", " ", Autre)
        Autre = Autre.strip()
        Lprov.insert(0, Autre)
    else:
        L0.insert(0, 'NONE')
        L1.insert(0, 'NONE')
        L2.insert(0, 'NONE')
        L3.insert(0, 'NONE')
        L4.insert(0, 'NONE')
        L5.insert(0, 'NONE')
        L6.insert(0, 'NONE')
        L7.insert(0, 'NONE')
        Lprov.insert(0, 'NONE')
    I0 = " "
    I1 = " "
    I2 = " "
    I3 = " "
    I4 = " "
    I5 = " "
    I6 = " "
    I7 = " "
    Iprov = " "
    for i in range(0, len(L0)):
        I0 = I0 + ' ' + L0[i]
        I0 = re.sub(r'\bNONE\b', '', I0)
        I0 = I0.strip()
    for i in range(0, len(L1)):
        I1 = I1 + ' ' + L1[i]
        I1 = re.sub(r'\bNONE\b', '', I1)
        I1 = I1.strip()
    for i in range(0, len(L2)):
        I2 = I2 + ' ' + L2[i]
        I2 = re.sub(r'\bNONE\b', '', I2)
        I2 = I2.strip()
    for i in range(0, len(L3)):
        I3 = I3 + ' ' + L3[i]
        I3 = re.sub(r'\bNONE\b', '', I3)
        I3 = I3.strip()
    for i in range(0, len(L4)):
        I4 = I4 + ' ' + L4[i]
        I4 = re.sub(r'\bNONE\b', '', I4)
        I4 = I4.strip()
    for i in range(0, len(L5)):
        I5 = I5 + ' ' + L5[i]
        I5 = re.sub(r'\bNONE\b', '', I5)
        I5 = I5.strip()
    for i in range(0, len(L6)):
        I6 = I6 + ' ' + L6[i]
        I6 = re.sub(r'\bNONE\b', '', I6)
        I6 = I6.strip()
    for i in range(0, len(L7)):
        I7 = I7 + ' ' + L7[i]
        I7 = re.sub(r'\bNONE\b', '', I7)
        I7 = I7.strip()
    for i in range(0, len(Lprov)):
        Iprov = Iprov + ' ' + Lprov[i]
        Iprov = re.sub(r'\bNONE\b', '', Iprov)
        Iprov = Iprov.strip()

    IB = I0
    EB = I1 + ' ' + I2
    EB = re.sub(r'\bNONE\b', '', EB)
    EB = EB.strip()
    EB = re.sub('\s+', ' ', EB)

    EB2 = I2 + ' ' + I1
    EB2 = re.sub(r'\bNONE\b', '', EB2)
    EB2 = EB2.strip()
    EB2 = re.sub('\s+', ' ', EB2)

    PL = I3 + ' ' + I4 + ' ' + I5
    PL = re.sub(r'\bNONE\b', '', PL)
    PL = PL.strip()
    PL = re.sub('\s+', ' ', PL)
    ZN = I6
    PO = I7
    AU = Iprov
    if IB == '':
        IB = 'NONE'
    if EB == '':
        EB = 'NONE'
    if PL == '':
        PL = 'NONE'
    if ZN == '':
        ZN = 'NONE'
    if PO == '':
        PO = 'NONE'
    if AU == '':
        AU = 'NONE'
    if EB2 == '':
        EB2 = 'NONE'
    LTOT = []
    LTOT.insert(0, IB)
    LTOT.insert(1, EB)
    LTOT.insert(2, PL)
    LTOT.insert(3, ZN)
    LTOT.insert(4, PO)
    LTOT.insert(5, AU)
    LTOT.insert(6, EB2)
    return LTOT


def ParsingROAD2(RES, RES2):
    Lroad = []
    S = RES[0]
    L = S.split()
    k = 0
    T = False
    L2 = []
    while k < len(L) and T == False:

        if L[k].isdigit() == True and (len(L[k]) == 5):
            T = True
            for j in range(k, len(L)):
                L2.insert(j, L[j])

        else:
            k = k + 1
    if T == True:
        Extra = " ".join(str(x) for x in L2)
        if RES2[5] != 'NONE':
            RES2[5] = RES2[5] + ' ' + Extra
        else:
            RES2[5] = Extra
        S = S.replace(Extra, ' ')
        S = re.sub('\s+', ' ', S)
        S = S.strip()
    S = str(S)
    if S != 'NONE':
        L = S.split()
        k = 0
        T = False
        if 'EME' not in S:
            while k < len(L) and T == False:
                if L[k].isdigit() == True or numT(L[k]) == True:
                    NUM = L[k]
                    T = True
                else:
                    k = k + 1
            if T == True:
                if L[k + 1] in [
                        'BIS', 'TER', 'QUATER', 'A', 'B', 'C', 'D', 'E', 'F',
                        'G', 'Q', 'T'
                ]:
                    Lroad.insert(0, NUM + ' ' + L[k + 1])
                    road = S.replace(NUM + ' ' + L[k + 1], ' ')
                    road = road.strip()
                    Lroad.insert(1, road)
                else:
                    Lroad.insert(0, NUM)
                    road = S.replace(NUM, ' ')
                    road = road.strip()
                    Lroad.insert(1, road)
            else:
                Lroad.insert(0, 'NONE')
                Lroad.insert(1, S)
        else:
            Lroad.insert(0, 'NONE')
            Lroad.insert(1, S)
    else:
        Lroad.insert(0, 'NONE')
        Lroad.insert(1, 'NONE')
    return Lroad


def strip_accents(ss):
    try:
        ss = unicode(ss, 'utf8')
    except:
        pass
    ss = unicodedata.normalize('NFD', ss)
    ss = ss.encode('ascii', 'ignore')
    ss = ss.decode('utf8')
    return str(ss)


# @sync_to_async


def Address_Standardization(Address):
    Final = []
    #print('###Typographic error correction###')
    Address = Address.replace(",", " ")
    Address = Address.replace("''", "'")
    Address = Address.replace('"', "")
    if Address[0] == "'" and Address[len(Address) - 1] == "'":
        Address = Address[1:]
        Address = Address[:len(Address) - 1]
    Address = str(Address).upper()
    Address = strip_accents(Address)
    Address = Address.replace('CDEX', 'CEDEX')
    Address = re.sub("\s\s+", " ", Address)
    Address = Address.strip()
    if 'CEDEX' in Address:
        pos = Address.find('CEDEX')
        Address2 = Address
        Address = Address[0:pos].strip()
        CE = Address2[pos:len(Address2)]
    else:
        CE = 'NONE'

    TYPOnbr = typoerrorcorrection(Address)[1]
    Address = typoerrorcorrection(Address)[0]

    #print('###Gestion des abbreviations ###')
    ABVnbr = abbreviation(Address)[1]
    Address = abbreviation(Address)[0]

    #print('###Parsing###')
    RES0 = ExtractLocality(Address, dfcity)
    Address = RES0[3]
    ADDL = Address.split()
    for i in range(0, len(ADDL)):
        if ADDL[i] == 'NONE':
            ADDL[i] = ' '
    Address = ' '.join(str(x) for x in ADDL)
    Address = re.sub("\s\s+", " ", Address)
    Address = Address.strip()
    RES = ParsingROAD(Address)
    RES2 = ParsingHOUSE(RES)
    RES3 = ParsingROAD2(RES, RES2)
    INBUILDING = RES2[0]
    EXTBUILDING = RES2[1]
    EXTBUILDINGprime = RES2[6]
    POILOGISTIC = RES2[2]
    ZONE = RES2[3]
    HouseNum = RES3[0]
    RoadName = RES3[1]
    POBOX = RES2[4]
    ZIPCODE = RES0[0]
    CITY = RES0[1]
    COUNTRY = RES0[2]
    if HouseNum == 'NONE':
        p1 = EXTBUILDING.find('-')
        p2 = POILOGISTIC.find('-')
        p3 = ZONE.find('-')

        if p1 != -1 and EXTBUILDING[p1 - 1].isdigit() == True and EXTBUILDING[
                p1 + 1].isdigit() == True and p1 == len(EXTBUILDING) - 2:
            NUM = EXTBUILDING[p1 - 1] + EXTBUILDING[p1] + EXTBUILDING[p1 + 1]
            HouseNum = NUM
            EXTBUILDING = EXTBUILDING.replace(NUM, ' ')
            EXTBUILDING = re.sub("\s\s+", " ", EXTBUILDING)
            EXTBUILDING = EXTBUILDING.strip()

        elif p2 != -1 and POILOGISTIC[
                p2 - 1].isdigit() == True and POILOGISTIC[
                    p2 + 1].isdigit() == True and p2 == len(POILOGISTIC) - 2:
            NUM = POILOGISTIC[p2 - 1] + POILOGISTIC[p2] + POILOGISTIC[p2 + 1]
            HouseNum = NUM
            POILOGISTIC = POILOGISTIC.replace(NUM, ' ')
            POILOGISTIC = re.sub("\s\s+", " ", POILOGISTIC)
            POILOGISTIC = POILOGISTIC.strip()

        elif p3 != -1 and ZONE[p3 - 1].isdigit() == True and ZONE[
                p3 + 1].isdigit() == True and p3 == len(ZONE) - 2:
            NUM = ZONE[p3 - 1] + ZONE[p3] + ZONE[p3 + 1]
            HouseNum = NUM
            ZONE = ZONE.replace(NUM, ' ')
            ZONE = re.sub("\s\s+", " ", ZONE)
            ZONE = ZONE.strip()
    Extra = Address
    if ZIPCODE != 'NONE' and CITY != 'NONE' and COUNTRY != 'NONE':
        C = str(ZIPCODE) + ' ' + CITY + ' ' + COUNTRY
        Extra = Extra.replace(C, ' ')
    elif CITY != 'NONE' and COUNTRY != 'NONE':
        C = CITY + ' ' + COUNTRY
        Extra = Extra.replace(C, ' ')
    elif ZIPCODE != 'NONE' and COUNTRY != 'NONE':
        C = str(ZIPCODE) + ' ' + COUNTRY
        Extra = Extra.replace(C, ' ')
    elif ZIPCODE != 'NONE' and CITY != 'NONE' and COUNTRY == 'NONE':
        C = str(ZIPCODE) + ' ' + CITY
        Extra = Extra.replace(C, ' ')
    elif ZIPCODE == 'NONE' and CITY != 'NONE' and COUNTRY == 'NONE':
        C = CITY
        Extra = Extra.replace(C, ' ')
    elif ZIPCODE != 'NONE' and CITY == 'NONE' and COUNTRY == 'NONE':
        C = str(ZIPCODE)
        Extra = Extra.replace(C, ' ')

    if POBOX != 'NONE':
        Extra = Extra.replace(POBOX, ' ')
    if INBUILDING != 'NONE':
        Extra = Extra.replace(INBUILDING, ' ')
    if EXTBUILDING != 'NONE' and EXTBUILDING not in Extra:
        Extra = Extra.replace(EXTBUILDINGprime, ' ')
    if EXTBUILDING != 'NONE' and EXTBUILDING in Extra:
        Extra = Extra.replace(EXTBUILDING, ' ')
    if POILOGISTIC != 'NONE':
        Extra = Extra.replace(POILOGISTIC, ' ')
    if ZONE != 'NONE':
        Extra = Extra.replace(ZONE, ' ')
    if HouseNum != 'NONE':
        Extra = Extra.replace(HouseNum, ' ')
    if RoadName != 'NONE':
        Extra = Extra.replace(RoadName, ' ')
    Extra = re.sub("\s\s+", " ", Extra)
    Extra = Extra.strip()
    if Extra == '':
        Extra = 'NONE'
    AddFinal0 = INBUILDING + ' ' + EXTBUILDING + \
        ' ' + Extra+' '+POILOGISTIC + ' ' + ZONE
    AddFinal00 = AddFinal0 + ' ' + HouseNum + ' ' + RoadName + ' ' + POBOX
    AddFinal = AddFinal00 + ' ' + str(ZIPCODE) + ' ' + CITY + ' ' + COUNTRY
    AddFinal = re.sub(r'\bNONE\b', '', AddFinal)
    AddFinal = AddFinal.strip()
    AddFinal = re.sub('\s+', ' ', AddFinal)
    if CE != 'NONE' and POBOX != 'NONE':
        POBOX = POBOX + ' ' + CE
    elif CE != 'NONE' and POBOX == 'NONE':
        POBOX = CE
    Final.insert(0, AddFinal)
    Final.insert(1, INBUILDING)
    Final.insert(2, EXTBUILDING)
    Final.insert(3, Extra)
    Final.insert(4, POILOGISTIC)
    Final.insert(5, ZONE)
    Final.insert(6, HouseNum)
    Final.insert(7, RoadName)
    Final.insert(8, POBOX)
    Final.insert(9, ZIPCODE)
    Final.insert(10, CITY)
    Final.insert(11, COUNTRY)
    Final.insert(12, CE)
    Final.insert(13, ABVnbr)
    Final.insert(14, TYPOnbr)
    return Final


# Unit standardization with Django


def StandUnit(request):
    start_time = time.time()
    if request.method == 'GET':
        Address = request.GET.get('Address')
        Address = Address.upper()
        # Standardization
        cv = Address_Standardization(Address)
        company = []
        Add = []
        INBUILDINGL = []
        EXTBUILDINGL = []
        POILOGISTICL = []
        ZONEL = []
        HouseNumL = []
        RoadNameL = []
        POBOXL = []
        zipcodeL = []
        cityL = []
        countryL = []
        extraL = []
        confidenceL = []
        IND = []
        nbArr = []
        nbCorr = []
        j = 0
        Add.insert(j, cv[0])
        INBUILDINGL.insert(j, cv[1])
        EXTBUILDINGL.insert(j, cv[2])
        extraL.insert(j, cv[3])
        POILOGISTICL.insert(j, cv[4])
        ZONEL.insert(j, cv[5])
        HouseNumL.insert(j, cv[6])
        RoadNameL.insert(j, cv[7])
        POBOXL.insert(j, cv[8])
        zipcodeL.insert(j, cv[9])
        cityL.insert(j, cv[10])
        countryL.insert(j, cv[11])
        nbArr.insert(j, cv[13])
        nbCorr.insert(j, cv[14])
        j = j + 1
        df = pd.DataFrame()
        se30 = pd.Series(company)
        df['SOCIETY_NAME'] = se30.values
        # se31 = pd.Series(Add)
        # df['Address'] = se31.values
        se32 = pd.Series(INBUILDINGL)
        df['INBUILDING'] = se32.values
        se33 = pd.Series(EXTBUILDINGL)
        df['EXTBUILDING'] = se33.values
        se34 = pd.Series(POILOGISTICL)
        df['POI_LOGISTIC'] = se34.values
        se35 = pd.Series(ZONEL)
        df['ZONE'] = se35.values
        se36 = pd.Series(HouseNumL)
        df['HOUSENUM'] = se36.values
        se37 = pd.Series(RoadNameL)
        df['ROADNAME'] = se37.values
        se38 = pd.Series(POBOXL)
        df['POBOX'] = se38.values
        se39 = pd.Series(zipcodeL)
        df['ZIPCODE'] = se39.values
        se40 = pd.Series(cityL)
        df['CITY'] = se40.values
        se41 = pd.Series(countryL)
        df['COUNTRY'] = se41.values
        se42 = pd.Series(extraL)
        df['ADDITIONAL'] = se42.values
        se43 = pd.Series(nbArr)
        df['nbArr'] = se43.values
        se44 = pd.Series(nbCorr)
        df['nbCorr'] = se44.values
        # t = df.to_dict('records')
        # print(t)
        total = time.time() - start_time
        print(total)
    return HttpResponse(df.to_json(orient='records'))


# Statistiques avec pandas profiling
def pandasProfiling(request):
    start_time = time.time()
    if request.method == 'POST':
        File = JSONParser().parse(request)
        newdf1 = pd.DataFrame(File)
        # print("3333", newdf1)
        del newdf1['nbArr']
        del newdf1['nbCorr']
        newdf1.columns = [
            'company', 'ADDRESS', 'INBUILDING', 'EXTBUILDING', 'POI_LOGISTIC',
            'ZONE', 'HOUSENUM', 'ROADNAME', 'POBOX', 'ZIPCODE', 'CITY',
            'COUNTRY', 'ADDITIONAL'
        ]
        print(newdf1)
        # get html profile
        # profile = ProfileReport(newdf1, title="Pandas Profiling Report", minimal=True)
        profile = ProfileReport(newdf1, title="Data Standardization Report")
        # profile
        profile.to_file(output_file="./templates/profiling.html")
        html = open('./templates/profiling.html', 'r')
        mystr = html.read()
        #webbrowser.open_new_tab("www.google.fr")
        # print(mystr)
        template = loader.get_template('../templates/profiling.html')
        template.render()
        response = HttpResponse()
        # construct the file's path
        url = os.path.join('./templates/profiling.html')
        #print("url :",url)
        #print("responnnns : ",response)
        # test if path is ok and file exists
        if os.path.isfile(url):
            # let nginx determine the correct content type in this case
            #print("test")
            response['Content-Type'] = "application/xhtml+xml"
            #response['X-Accel-Redirect'] = url
            response['X-Sendfile'] = url
        # other webservers may accept X-Sendfile and not X-Accel-Redirect
        # print(template.read())
    # return redirect('profiling.html')
    # return render(request, 'profiling.html', content_type='application/xhtml+xml')
    # return HttpResponse(template.render(t), content_type='application/xhtml+xml')
    # return HttpResponse(template)
    # , content_type='application/xhtml+xml'
    total = time.time() - start_time
    print(total)
    #return response
    #return render(None, response)
    #print(os.path.realpath("./templates/profiling.html"))
    # return HttpResponse(template, content_type='text/html; charset=utf-8', status=200)
    webbrowser.get('chrome').open(
        "file://" + os.path.realpath("./templates/profiling.html"),
        new=0,
        autoraise=True)
    return HttpResponse(json.dumps(mystr), content_type='text/plain')


# Pour le profilage d'abbreviation


def getAbbreviation(request):
    start_time = time.time()
    if request.method == 'GET':
        Address = request.GET.get('Address')
        Address = Address.upper()
        # abbreviation
        cv = abbreviation(Address)
        print(cv)
        adresse = []
        nb = []
        j = 0
        adresse.insert(j, cv[0])
        nb.insert(j, cv[1])
        j = j + 1
        df = pd.DataFrame()
        se30 = pd.Series(adresse)
        df['adresse'] = se30.values
        se32 = pd.Series(nb)
        df['nb'] = se32.values
        total = time.time() - start_time
        print(total)
    return HttpResponse(df.to_json(orient='records'))


# Pour le profilage de TypoErrorCorrection


def getTypoErrorCorrection(request):
    start_time = time.time()
    if request.method == 'GET':
        Address = request.GET.get('Address')
        print("adress : ", Address)
        Address = Address.upper()
        # typoerrorcorrection
        cv = typoerrorcorrection(Address)
        adresse = []
        nbtot = []
        j = 0
        adresse.insert(j, cv[0])
        nbtot.insert(j, cv[1])
        j = j + 1
        df = pd.DataFrame()
        se30 = pd.Series(adresse)
        df['adresse'] = se30.values
        se32 = pd.Series(nbtot)
        df['nbtot'] = se32.values
        total = time.time() - start_time
        print(total)
    return HttpResponse(df.to_json(orient='records'))


# Pour le profilage de TypoErrorCorrection


def getNbStand(request):
    if request.method == 'GET':
        Address = request.GET.get('Address')
        Address = Address.upper()
        # Standardization
        df = pd.DataFrame()
        se30 = pd.Series(Address)
        df['adresse'] = se30.values
        '''
        se32 = pd.Series(nbtot)
        df['nbtot'] = se32.values
        '''

    return HttpResponse(df.to_json(orient='records'))


def file_Standardization(df):
    INBUILDINGL = []
    EXTBUILDINGL = []
    ExtraL = []
    POILOGISTICL = []
    ZONEL = []
    HouseNumL = []
    RoadNameL = []
    POBOXL = []
    ZIPCODEL = []
    CITYL = []
    COUNTRYL = []
    nbArr = []
    nbCorr = []
    print("************", df)
    # for i in range(0, len(df)):
    # print(i)
    '''
    task=asyncio.ensure_future(Address_Standardization(df['ADDRESS'][i]))
    print(task)
    R = await asyncio.wait([task])
    '''
    num_cores = multiprocessing.cpu_count()
    print('process name :', multiprocessing.current_process().name)
    print('process number :', num_cores)
    #R = Parallel(n_jobs=num_cores)(delayed(Address_Standardization)(df['ADDRESS'][i]) for i in range(0, len(df)))
    #print('résultats : ', R)

    #R = Address_Standardization(df['ADDRESS'][i])
    # print(R)
    for i in range(0, len(df)):
        try:
            R = Address_Standardization(df['ADDRESS'][i])
            #print(R)
            INBUILDINGL.insert(i, R[1])
            EXTBUILDINGL.insert(i, R[2])
            POILOGISTICL.insert(i, R[4])
            ZONEL.insert(i, R[5])
            HouseNumL.insert(i, R[6])
            RoadNameL.insert(i, R[7])
            POBOXL.insert(i, R[8])
            ZIPCODEL.insert(i, R[9])
            CITYL.insert(i, R[10])
            COUNTRYL.insert(i, R[11])
            ExtraL.insert(i, R[3])
            nbArr.insert(i, R[13])
            nbCorr.insert(i, R[14])

        except:
            # print('eeeeeeeeeeeeeeeeeeeeeeeeeee')
            INBUILDINGL.insert(i, 'NONE')
            EXTBUILDINGL.insert(i, 'NONE')
            POILOGISTICL.insert(i, 'NONE')
            ZONEL.insert(i, 'NONE')
            HouseNumL.insert(i, 'NONE')
            RoadNameL.insert(i, 'NONE')
            POBOXL.insert(i, 'NONE')
            ZIPCODEL.insert(i, 'NONE')
            CITYL.insert(i, 'NONE')
            COUNTRYL.insert(i, 'NONE')
            ExtraL.insert(i, 'NONE')
            nbArr.insert(i, 0)
            nbCorr.insert(i, 0)
    # data = pd.DataFrame()
    se21 = pd.Series(INBUILDINGL)
    df['INBUILDING'] = se21.values
    se22 = pd.Series(EXTBUILDINGL)
    df['EXTBUILDING'] = se22.values
    se23 = pd.Series(POILOGISTICL)
    df['POI_LOGISTIC'] = se23.values
    se24 = pd.Series(ZONEL)
    df['ZONE'] = se24.values
    se25 = pd.Series(HouseNumL)
    df['HOUSENUM'] = se25.values
    se26 = pd.Series(RoadNameL)
    df['ROADNAME'] = se26.values
    se27 = pd.Series(POBOXL)
    df['POBOX'] = se27.values
    se28 = pd.Series(ZIPCODEL)
    df['ZIPCODE'] = se28.values
    se29 = pd.Series(CITYL)
    df['CITY'] = se29.values
    se30 = pd.Series(COUNTRYL)
    df['COUNTRY'] = se30.values
    se31 = pd.Series(ExtraL)
    df['ADDITIONAL'] = se31.values
    se32 = pd.Series(nbArr)
    df['nbArr'] = se32.values
    se33 = pd.Series(nbCorr)
    df['nbCorr'] = se33.values
    return df


# File standardization with Django

def StandFile(request):
    start_time = time.time()
    if request.method == 'POST':
        File = request.FILES["file"]
        df = pd.read_csv(File)

        #print(df)

        # Standardization
        data = file_Standardization(df)
        print('data : ', data)
        #data = data.select("*").toPandas()
        #spark.stop()
    total = time.time() - start_time
    print(total)
    return HttpResponse(data.to_json(orient='records'))


############################## Verification unitaire ################

# REFERENCE DATABASE CONNECTION

client = MongoClient('localhost', 27017)

# Nom de la base = TransportRefDB92
# Nom de la collection = Companies92
db = client['TransportRefDB93']
collection = db['companies93']


# MAtching avec la base de reference
def RefDBMatching(CompanyName, Addr, INBUILDING, EXTBUILDING, POILOGISTIC,
                  ZONE, HouseNum, RoadName, POBOX, city, country, ADDITIONAL):
    #R = ExtractLocality(Addr,dfcity)
    #city = R[1]
    #country = R[2]
    print("test", db)
    print(collection.find({'company.Name': {'$regex': CompanyName}}).count())
    z = collection.find({
        'company.Name': {
            '$regex': CompanyName
        },
        'company.Address.INBUILDING': INBUILDING,
        'company.Address.EXTBUILDING': EXTBUILDING,
        'company.Address.POILOGISTIC': POILOGISTIC,
        'company.Address.ZONE': ZONE,
        'company.Address.HouseNum': HouseNum,
        'company.Address.RoadName': RoadName,
        'company.Address.POBOX': POBOX,
        'company.Address.city': city,
        'company.Address.country': country
    })
    # 2
    if (INBUILDING != 'NONE' and EXTBUILDING != 'NONE'
            and POILOGISTIC != 'NONE' and ZONE != 'NONE' and HouseNum != 'NONE'
            and RoadName != 'NONE' and POBOX != 'NONE'
            and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.INBUILDING': INBUILDING,
            'company.Address.EXTBUILDING': EXTBUILDING,
            'company.Address.POILOGISTIC': POILOGISTIC,
            'company.Address.ZONE': ZONE,
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.POBOX': POBOX,
            'company.Address.city': city,
            'company.Address.country': country
        })
    # 3
    if (INBUILDING != 'NONE' and EXTBUILDING != 'NONE'
            and POILOGISTIC != 'NONE' and ZONE != 'NONE' and HouseNum != 'NONE'
            and RoadName != 'NONE' and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.INBUILDING': INBUILDING,
            'company.Address.EXTBUILDING': EXTBUILDING,
            'company.Address.POILOGISTIC': POILOGISTIC,
            'company.Address.ZONE': ZONE,
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })
    # 4
    if (INBUILDING != 'NONE' and EXTBUILDING != 'NONE'
            and POILOGISTIC != 'NONE' and HouseNum != 'NONE'
            and RoadName != 'NONE' and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.INBUILDING': INBUILDING,
            'company.Address.EXTBUILDING': EXTBUILDING,
            'company.Address.POILOGISTIC': POILOGISTIC,
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })
    # 5
    if (INBUILDING != 'NONE' and EXTBUILDING != 'NONE' and HouseNum != 'NONE'
            and RoadName != 'NONE' and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.INBUILDING': INBUILDING,
            'company.Address.EXTBUILDING': EXTBUILDING,
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })
    # 6
    if (EXTBUILDING != 'NONE' and HouseNum != 'NONE' and RoadName != 'NONE'
            and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.EXTBUILDING': EXTBUILDING,
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })

    # 7
    if (INBUILDING != 'NONE' and HouseNum != 'NONE' and RoadName != 'NONE'
            and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.INBUILDING': INBUILDING,
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })
    # 8
    if (ZONE != 'NONE' and HouseNum != 'NONE' and RoadName != 'NONE'
            and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.ZONE': ZONE,
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })

    # 9
    if (ZONE != 'NONE' and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.ZONE': ZONE,
            'company.Address.city': city,
            'company.Address.country': country
        })

    # 10
    if (HouseNum != 'NONE' and RoadName != 'NONE'
            and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.HouseNum': HouseNum,
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })

    # 11
    if (RoadName != 'NONE' and city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.RoadName': RoadName,
            'company.Address.city': city,
            'company.Address.country': country
        })
    # 12
    if (city != 'NONE') or (z.count() == 0):
        z = collection.find({
            'company.Name': {
                '$regex': CompanyName
            },
            'company.Address.city': city
        })
    # if (z.count()==0):
    #	z = collection.find({'company.Name': {'$regex': CompanyName}})
    D = 'NONE'
    Nbr = z.count()
    LLIST = []
    if Nbr > 0:
        for k in range(0, Nbr):
            D = {
                'CompanyName': z[k]['company']['Name'],
                'INBUILDING': z[k]['company']['Address']['INBUILDING'],
                'EXTBUILDING': z[k]['company']['Address']['EXTBUILDING'],
                'POILOGISTIC': z[k]['company']['Address']['POILOGISTIC'],
                'ZONE': z[k]['company']['Address']['ZONE'],
                'HouseNum': z[k]['company']['Address']['HouseNum'],
                'RoadName': z[k]['company']['Address']['RoadName'],
                'POBOX': z[k]['company']['Address']['POBOX'],
                'zipcode': z[k]['company']['Address']['zipcode'],
                'city': z[k]['company']['Address']['city'],
                'country': z[k]['company']['Address']['country'],
                'ADDITIONAL': z[k]['company']['Address']['ADDITIONAL']
            }
            LLIST.insert(k, D)
    return LLIST


# verification unitaire
def UNITSEARCH(CompanyName, Address):
    print("company : ", CompanyName)
    print("adress : ", Address)
    AddL = []
    RES = Address_Standardization(Address)
    ADDRESS_ST = RES[0]
    INBUILDING = RES[1]
    EXTBUILDING = RES[2]
    POILOGISTIC = RES[4]
    ZONE = RES[5]
    HouseNum = RES[6]
    RoadName = RES[7]
    POBOX = RES[8]
    ZIPCODE = RES[9]
    city = RES[10]
    country = RES[11]
    ADDITIONAL = RES[3]
    print('###MAtching with Reference DB###')
    RESDB = RefDBMatching(CompanyName, Address, INBUILDING, EXTBUILDING,
                          POILOGISTIC, ZONE, HouseNum, RoadName, POBOX, city,
                          country, ADDITIONAL)
    for i in range(0, len(RESDB)):
        OUTINBUILDING = RESDB[i]['INBUILDING']
        OUTEXTBUILDING = RESDB[i]['EXTBUILDING']
        OUTPOILOGISTIC = RESDB[i]['POILOGISTIC']
        OUTZONE = RESDB[i]['ZONE']
        OUTHouseNum = RESDB[i]['HouseNum']
        OUTRoadName = RESDB[i]['RoadName']
        OUTPOBOX = RESDB[i]['POBOX']
        OUTZIPCODE = RESDB[i]['zipcode']
        OUTCITY = RESDB[i]['city']
        OUTCOUNTRY = RESDB[i]['country']
        OUTADDITIONAL = RESDB[i]['ADDITIONAL']
        AddFinal0 = OUTADDITIONAL+' '+OUTINBUILDING + ' ' + \
            OUTEXTBUILDING + ' ' + OUTPOILOGISTIC + ' ' + OUTZONE
        AddFinal00 = AddFinal0 + ' ' + OUTHouseNum + ' ' + OUTRoadName + ' ' + OUTPOBOX
        AddFinal = AddFinal00 + ' ' + \
            str(OUTZIPCODE) + ' ' + OUTCITY + ' ' + OUTCOUNTRY
        AddFinal = re.sub(r'\bNONE\b', '', AddFinal)
        AddFinal = AddFinal.strip()
        AddFinal = re.sub('\s+', ' ', AddFinal)
        AddL.insert(i, AddFinal)
    Tab = []
    Tab.insert(0, RESDB)
    Tab.insert(1, AddL)
    Tab.insert(2, ADDRESS_ST)
    return Tab


def verifUnit(request):
    start_time = time.time()
    if request.method == 'GET':
        Address = request.GET.get('Address')
        Address = Address.upper()
        CompanyName = request.GET.get('Company')
        CompanyName = CompanyName.upper()
        # Vérification
        cv = UNITSEARCH(CompanyName, Address)
        company = []
        Add = []
        INBUILDINGL = []
        EXTBUILDINGL = []
        POILOGISTICL = []
        ZONEL = []
        HouseNumL = []
        RoadNameL = []
        POBOXL = []
        zipcodeL = []
        cityL = []
        countryL = []
        additionnalL = []
        companyI = []
        AddressI = []
        j = 0
        print("len cv : ", cv)
        if len(cv[0]) > 0:

            NBR = len(cv[0])
            for i in range(0, len(cv[0])):
                companyI.insert(j, CompanyName)
                AddressI.insert(j, cv[2])
                company.insert(j, cv[0][i]['CompanyName'])
                Add.insert(j, cv[1][i])
                INBUILDINGL.insert(j, cv[0][i]['INBUILDING'])
                EXTBUILDINGL.insert(j, cv[0][i]['EXTBUILDING'])
                POILOGISTICL.insert(j, cv[0][i]['POILOGISTIC'])
                ZONEL.insert(j, cv[0][i]['ZONE'])
                HouseNumL.insert(j, cv[0][i]['HouseNum'])
                RoadNameL.insert(j, cv[0][i]['RoadName'])
                POBOXL.insert(j, cv[0][i]['POBOX'])
                zipcodeL.insert(j, cv[0][i]['zipcode'])
                cityL.insert(j, cv[0][i]['city'])
                countryL.insert(j, cv[0][i]['country'])
                additionnalL.insert(j, cv[0][i]['ADDITIONAL'])
                j = j + 1

        else:
            companyI.insert(j, CompanyName)
            AddressI.insert(j, cv[2])
            company.insert(0, 'NO MATCHING COMPANY')
            Add.insert(0, 'NO MATCHING ADDRESS')
            INBUILDINGL.insert(0, 'NONE')
            EXTBUILDINGL.insert(0, 'NONE')
            POILOGISTICL.insert(0, 'NONE')
            ZONEL.insert(0, 'NONE')
            HouseNumL.insert(0, 'NONE')
            RoadNameL.insert(0, 'NONE')
            POBOXL.insert(0, 'NONE')
            zipcodeL.insert(0, 'NONE')
            cityL.insert(0, 'NONE')
            countryL.insert(0, 'NONE')
            additionnalL.insert(0, 'NONE')

        df6 = pd.DataFrame()
        se28 = pd.Series(companyI)
        df6['companyINPUT'] = se28.values
        se29 = pd.Series(AddressI)
        df6['AddressINPUT'] = se29.values

        se30 = pd.Series(company)
        df6['companyOUTPUT'] = se30.values
        se31 = pd.Series(Add)
        df6['AddressOUTPUT'] = se31.values
        se32 = pd.Series(INBUILDINGL)
        df6['INBUILDINGOUTPUT'] = se32.values
        se33 = pd.Series(EXTBUILDINGL)
        df6['EXTBUILDINGOUTPUT'] = se33.values
        se34 = pd.Series(POILOGISTICL)
        df6['POILOGISTICOUTPUT'] = se34.values
        se35 = pd.Series(ZONEL)
        df6['ZONEOUTPUT'] = se35.values
        se36 = pd.Series(HouseNumL)
        df6['HouseNumOUTPUT'] = se36.values
        se37 = pd.Series(RoadNameL)
        df6['RoadNameOUTPUT'] = se37.values
        se38 = pd.Series(POBOXL)
        df6['POBOXOUTPUT'] = se38.values
        se39 = pd.Series(zipcodeL)
        df6['zipcodeOUTPUT'] = se39.values
        se40 = pd.Series(cityL)
        df6['cityOUTPUT'] = se40.values
        se41 = pd.Series(countryL)
        df6['countryOUTPUT'] = se41.values
        se42 = pd.Series(additionnalL)
        df6['ADDITIONALOUTPUT'] = se42.values
        total = time.time() - start_time
        print(total)
    return HttpResponse(df6.to_json(orient='records'))


################################# verification d'un fichier ##############


def verif_file(df):
    company = []
    Add = []
    INBUILDINGL = []
    EXTBUILDINGL = []
    POILOGISTICL = []
    ZONEL = []
    HouseNumL = []
    RoadNameL = []
    POBOXL = []
    zipcodeL = []
    cityL = []
    countryL = []
    additionnalL = []
    companyI = []
    AddressI = []
    CompanyName = []
    j = 0
    for i in range(0, len(df)):
        print('i=', i)

        CompanyName0 = df['Input_company'][i]
        CompanyName0 = CompanyName0.upper()
        CompanyName.insert(i, CompanyName0)
        Address = df['Input_Address'][i]
        print('address=', Address)
        Address = Address.upper()
        cv = UNITSEARCH(CompanyName0, Address)
        AddressI.insert(i, Address)
        if len(cv[0]) > 0:

            company.insert(i, cv[0][0]['CompanyName'])
            Add.insert(i, cv[1][0])
            INBUILDINGL.insert(i, cv[0][0]['INBUILDING'])
            EXTBUILDINGL.insert(i, cv[0][0]['EXTBUILDING'])
            POILOGISTICL.insert(i, cv[0][0]['POILOGISTIC'])
            ZONEL.insert(i, cv[0][0]['ZONE'])
            HouseNumL.insert(i, cv[0][0]['HouseNum'])
            RoadNameL.insert(i, cv[0][0]['RoadName'])
            POBOXL.insert(i, cv[0][0]['POBOX'])
            zipcodeL.insert(i, cv[0][0]['zipcode'])
            cityL.insert(i, cv[0][0]['city'])
            countryL.insert(i, cv[0][0]['country'])
            additionnalL.insert(i, cv[0][0]['ADDITIONAL'])

        else:
            company.insert(i, 'NO MATCHING COMPANY')
            Add.insert(i, 'NO MATCHING ADDRESS')
            INBUILDINGL.insert(i, 'NONE')
            EXTBUILDINGL.insert(i, 'NONE')
            POILOGISTICL.insert(i, 'NONE')
            ZONEL.insert(i, 'NONE')
            HouseNumL.insert(i, 'NONE')
            RoadNameL.insert(i, 'NONE')
            POBOXL.insert(i, 'NONE')
            zipcodeL.insert(i, 'NONE')
            cityL.insert(i, 'NONE')
            countryL.insert(i, 'NONE')
            additionnalL.insert(i, 'NONE')

    df6 = pd.DataFrame()

    se28 = pd.Series(CompanyName)
    df6['companyINPUT'] = se28.values
    se29 = pd.Series(AddressI)
    df6['AddressINPUT'] = se29.values
    se30 = pd.Series(company)
    df6['companyOUTPUT'] = se30.values
    se31 = pd.Series(Add)
    df6['AddressOUTPUT'] = se31.values
    se32 = pd.Series(INBUILDINGL)
    df6['INBUILDINGOUTPUT'] = se32.values
    se33 = pd.Series(EXTBUILDINGL)
    df6['EXTBUILDINGOUTPUT'] = se33.values
    se34 = pd.Series(POILOGISTICL)
    df6['POILOGISTICOUTPUT'] = se34.values
    se35 = pd.Series(ZONEL)
    df6['ZONEOUTPUT'] = se35.values
    se36 = pd.Series(HouseNumL)
    df6['HouseNumOUTPUT'] = se36.values
    se37 = pd.Series(RoadNameL)
    df6['RoadNameOUTPUT'] = se37.values
    se38 = pd.Series(POBOXL)
    df6['POBOXOUTPUT'] = se38.values
    se39 = pd.Series(zipcodeL)
    df6['zipcodeOUTPUT'] = se39.values
    se40 = pd.Series(cityL)
    df6['cityOUTPUT'] = se40.values
    se41 = pd.Series(countryL)
    df6['countryOUTPUT'] = se41.values
    se42 = pd.Series(additionnalL)
    df6['ADDITIONALOUTPUT'] = se42.values
    return df6


def fileVerif(request):
    start_time = time.time()
    if request.method == 'POST':
        File = request.FILES["file"]
        df = pd.read_csv(File)
        # Verification
        data = verif_file(df)
    total = time.time() - start_time
    print(total)
    return HttpResponse(data.to_json(orient='records'))


# df6.to_csv('testV.csv')

#cProfile.run(file_Standardization(pd.read_csv(r'Input copie.csv')))
# File Standardization

# df = file_Standardization(df)
# df.to_csv('Input_Stand.csv')

# Unit Address Standardization
# address=''
# Result=Address_Standardization(address)
# print('Standard address=',Result)
