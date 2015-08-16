# -*- coding:utf-8 -*-
__author__ = "urban"

import pandas as pd
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, s=60, clrs=['r','b','g','c','m','y','k','#ffaabb']):
        self.s = s
        self.clrs=clrs
        self.dfraw = pd.read_csv('..\\data\\ex_work_data.txt', sep=';', 
                             encoding='utf8',low_memory=False,index_col=False)
        self.dfclean = self.dfraw[(self.dfraw['diamorfomenos'].notnull())]
        self.dfclean = self.dfclean[self.dfclean['diamorfomenos'] != 0.0]
        self.dfclean = self.dfclean[self.dfclean['etos'].notnull()] 
        self.dfclean = self.dfclean[self.dfclean['enotita'].notnull()]
    def get_raw(self):
        return self.dfraw
        
    def get_clean(self):
        return self.dfclean
        
    def read_raw_data(self):
        '''Read in the file'''
        self.dfraw = pd.read_csv('..\\data\\ex_work_data.txt', sep=';', 
                             encoding='utf8',low_memory=False,index_col=False)
                            
    def read_clean_data(self):
        if self.dfraw is None:
            self.read_raw_data()
        self.dfclean = self.dfraw[(self.dfraw['diamorfomenos'].notnull())]
        self.dfclean = self.dfclean[self.dfclean['diamorfomenos'] != 0.0]
        self.dfclean = self.dfclean[self.dfclean['etos'].notnull()] 
        self.dfclean = self.dfclean[self.dfclean['enotita'].notnull()]
        
    def do_scatter_enotita(self, df=None, x_name='diamorfomenos',
                           y_name='plirothenta', wid=15, hei=30):
        ''' Δημιουργία διαγραμμάτων διασποράς για κάθε ενότητα επί του 
        συνολικού αριθμού των ετών'''
        
        if df is None:
            df = self.dfclean
        clrs = ['r','b','g','c','m','y','k','#ffaabb']
        fig = plt.figure(1,figsize=(wid,hei)) #set the figure
        for i in xrange(0,8):
            #Get pe data
            p_data = df[df.enotita == i].dropna()
            #plt.subplot(4,2,i+1)
            if i==0 :
                ax = fig.add_subplot(8,1,i+1)
            else:
                fig.add_subplot(8,1,i+1,sharex = ax, sharey=ax)
            plt.scatter(p_data[x_name], p_data[y_name], s=60, c=clrs[i], 
                        label=i)
            plt.legend()
            plt.xlabel(x_name)
            plt.ylabel(y_name)
            
    def do_scatter_etos(self, df=None, x_name='diamorfomenos', 
                        y_name='plirothenta', wid=15, hei=30):
        if df is None:
            df = self.dfclean
        clrs = ['r','b','g','c']
        j=1
        fig = plt.figure(1,figsize=(wid,hei)) #set the figure
        for i in [2011,2012,2013,2014]:
            p_data = df[df.etos == i].dropna()
            if j == 1:
                ax = fig.add_subplot(4,1,j)
            else:
                fig.add_subplot(4,1,j,sharex = ax, sharey=ax)
            plt.scatter(p_data[x_name], p_data[y_name], s=60, c=clrs[j-1], 
                        label=i)
            plt.legend()
            plt.xlabel(x_name)
            plt.ylabel(y_name)
            j = j+1
        
    def do_scatter_etos_enotita(self, df=None, x_name='diamorfomenos',
                                y_name='plirothenta', wid=15, hei=30):
        if df is None:
            df = self.dfclean
        clrs = ['r','b','g','c','m','y','k','#ffaabb']
        yrs = [2011,2012,2013,2014]
        fig = plt.figure(figsize=(wid,hei)) #set the figure
        for i in xrange(0,8):
            p_data = df[df.enotita == i].dropna()
            for j in xrange(0,4):
                if j == 0:
                    ax = fig.add_subplot(7,4,i+1+j)
                else:
                    fig.add_subplot(7,4,i+1+j,sharex=ax, sharey=ax)
                plt.scatter(p_data[x_name], p_data[y_name], s=60, c=clrs[i], 
                            label= yrs[j])
                plt.legend()
                
    def get_col_diff(self, df=None, col1='diamorfomenos', col2='plirothenta'):
        if df is None:
            df = self.dfclean
        mydf = df[col1] - df[col2]
        return mydf
    