#-*-coding:utf8-*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Define global variables for names
ex_names = ['LOGARIASMOS','PERIGRAFI','EGGEKRIMENOS','ANAMORFOSEIS','DIAMORFOMENOS','DESMEFTHENTA', \
            'IPOL_DESME_PROS_DIAMOR','TIMOLOGITHENTA','IPOL_TIMOL_PROS_DIAMOR','ENTALTHENTA', \
            'IPOL_ENTAL_PROS_DIAMOR','PLIROTHENTA','IPOL_PLIRO_PROS_DIAMOR','ENTAL_MEION_PLIRO', \
            'DIATHESEIS','IPOL_TIMOL_PROS_DIATH','IPOL_DIATH_PROS_DIAMOR','IPOL_DIATH_PROS_DESME']
            
es_names =  ['LOGARIASMOS','PERIGRAFI','EGGEKRIMENOS','ANAMORFOSEIS','DIAMORFOMENOS','PARASTATIKA_ESODON', \
            'IPOL_PAR_ES_PROS_DIAMOR','BEBEOTHENTA','DIAGRAFES_PARAGRAFES','TELIKA_BEBEOTHENTA', \
            'IPOL_BEBE_PROS_DIAMOR','EISPRAXTHENTA','IPOL_EISPRA,PROS_DIAMOR','BEBE_MEION_EISPRA', \
            'DIATHESEIS','IPOL_TIMOL_PROS_DIATH','IPOL_DIATH_PROS_DIAMOR']
            
enotites = {'EDRA':'00', 
            'IMATHIA':'02', 
            'THESSALONIKI':'01', 
            'KILKIS':'03', 
            'PELLA':'05', 
            'PIERIA':'04', 
            'SERRES':'06', 
            'CHALKIDIKI':'07'}
            
def read_es_ex(year, data_type='ex'):
    fname = data_type + str(year) + '.csv'
    dnames = data_type + 'names'
    f = pd.read_csv(fname,sep=';',header=0,names=data_type+'names')
    
def read_ex(filename):
    pass
    
def nikos():
    pass