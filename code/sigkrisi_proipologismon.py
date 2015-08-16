# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 19:00:55 2015

@author: urban

Το αρχείο περιέχει συναρτήσεις που χρησιμοποιώ για το 
sigkrisi_proipologismon.ipynb. Το αρχείο λειτουργεί σε συνδυασμό με τα αρχεία
definitions.py -> Ορισμοί και μεταβλητές
dataframes.py -> Το αντικείμενο DataframesBuilder που είναι και βασικό για τη 
                διαχείριση των αρχείων προϋπολογισμών
"""

import pandas as pd
import numpy as np


def make_foreis(df):
    '''
    Εσωτερική ρουτίνα για να μπορέσουμε να πάρουμε τα δεδομένα όπως τα θέλουμε
    '''
    #group the data
    df = df.groupby(by='foreas', as_index=False).sum()
    df['pct_diam'] = np.round((df.diamorfomenos / df.eggekrimenos - 1) * 100,decimals=2)
    return df[['foreas','pct_diam']]
    
def compute_pivot_tameiakon(df, agg_column):
    tam = df[(df.kae.str[:1]==u'Τ') & (df.kae.str[1:]=='000')]
    return tam.pivot_table(agg_column, index='foreas', columns='enotita', aggfunc='sum')

def compute_tameiako_enotitas_xronia(df, enotita):
    '''Υπολογισμός του ταμειακού υπολοίπου ενότητας'''
    ret = None
    try:
        ret = compute_pivot_tameiakon(df, 'diamorfomenos')[enotita].sum()
    except KeyError:
        pass
    return ret
    
def add_year_field(df, year):
    '''
    Προσθήκη πεδίου έτους στο dataframe και επιστροφή αντιγράφου του dataframe
    '''
    t = df.copy()
    t['year'] = year
    return t