# -*- coding:utf-8 -*-
__author__ = 'urban'

"""
This file holds the functions to create all kinds of dataframes that will 
be using.
"""

import pandas as pd
import numpy as np
import definitions as defs

class DataFramesBuilder:
    def __init__(self, indf=None):
        """
        Initialize the class with the source dataframe
        """
        if not (indf is None):
            self.indf = indf.copy()
    
    def read_file(self, filename, es_ex = 'ex'):
        if es_ex == 'es':
            return self.read_esoda(filename)
        else:
            return self.read_exoda(filename)
            
    def read_exoda(self, filename, parse_cols='A:J'):
        """
        Read exoda of a specified file
        :param filename: The filename to read. Must be xls
        :param parse_cols: int or list of columns to parse
        :return: The dataframe
        """
        self.indf = pd.read_excel(filename, sheetname=0, header=None, 
                                  skiprows=1, parse_cols=parse_cols, 
                                  names=defs.exnames)
        return self.indf.copy()
    
    def read_esoda(self, filename, parse_cols='A:F'):
        """
        Read esoda from a specified file
        :param filename: The filename to read. Must be xls
        :param parse_cols: int or list of columns to parse
        :return: The dataframe
        """
        self.indf = pd.read_excel(filename, sheetname=0, header=None, 
                                  skiprows=1, parse_cols=parse_cols, 
                                  names=defs.esnames)
        return self.indf.copy()
    
    def set_inner_dataframe(self, df):
        """
        Sets the inner dataframe to the given as parameter
        :param df: The dataframe to use
        :return: None
        """
        self.indf = df
        return None
        
    def get_degree_logar(self, df=None, logar='logar', sep='.'):
        '''
        Return the degrees of the logar based on the separator
        :param df: The dataframe to use
        :param logar: The name of the field containing logariasmo
        :param sep: The separator to use. Default '.'
        :return :Series with the integer representing degree of logar
        '''
        if df is None:
            df = self.indf.copy()
        return df[logar].str.strip().split(sep).len()
        
    def add_extra_fields(self, df=None):
        '''
        Προσθέτει μερικά επιπλέον πεδία στο dataframe προκειμένου να 
        διευκολύνει την περαιτέρω ομαδοποίηση και επεξεργασία.
        :return: Dataframe with extra fields
        '''
        if df is None:
            df = self.indf.copy()
            
        df['eidos'] = df.logar.str[:2]
        df['enotita'] = df.logar.str[3:5]
        df['foreas'] = df.logar.str[6:9]
        df['kae'] = df.logar.str[10:14]
        df['xilia'] = df.logar.str[10:11]
        df['ekato'] = df.logar.str[11:12]
        df['deka'] = df.logar.str[12:13]
        df['ena'] = df.logar.str[13:14]
        return df

    def get_foreis_df(self, df=None):
        """
        Επιστρέφει τα δεδομένα μόνο για τους φορείς. Συγκεκριμένα όσοι 
        λογατριασμοί είναι με 9 ψηφία.
        :param df:The dataframe to work with
        :return: a copy of the original dataframe with logar of length 9
        """
        if df is None:
            d = self.indf
        else:
            d = df
        return d[d.logar.str.len() == 9].copy()

    def get_xilia_df(self, df=None):
        '''
        Επιστρέφει τους λογαριασμούς σε επίπεδο πρώτου ψηφίου των ΚΑΕ.
        :param df:The dataframe to work with
        :return: a copy of the original dataframe with in thousands level KAE
        analysis
        '''
        if df is None: 
            d = self.indf 
        else: 
            d = df
        return d[d.kae.str[1:]=='000'].copy()
        
    def get_ekato_df(self, df=None):
        '''
        Επιστρέφει τους λογαριασμούς σε επίπεδο εκατοντάδας αποκλείοντας 
        τις χιλιάδες.
        :param df:The dataframe to work with
        :return: a copy of the original dataframe with in hundreds level KAE 
        analysis
        '''
        if df is None: 
            d = self.indf 
        else: 
            d = df
        return d[(d.kae.str[2:]=='00') & (d.kae.str[1:2]!='0')].copy()

    def get_deka_df(self, df=None):
        '''
        Επιστρέφει τους λογαριαμούς σε επίπεδο δεκάδας αποκλείοντας τις 
        εκατοντάδες αλλά και τις χιλιάδες
        :param df:The dataframe to work with
        :return: a copy of the original dataframe with in decimal level KAE 
        analysis
        
        '''
        if df is None: 
            d = self.indf 
        else: 
            d = df
        return d[(d.kae.str[1:]!='000') & 
                (d.kae.str[2:]!='00') & 
                (d.kae.str[3:]=='0')].copy()
    
    def get_previous_years(self, df=None):
        '''
        Επιστρέφει μόνο τους λογαριασμούς που είναι χαρακτηρισμένοι ως .02
        αφορούν δηλαδή ποσά από προηγούμενες χρήσεις.
        :param df: The dataframe to work with
        :return: a copy of the original dataframe with past years
        '''
        if df is None:
            d = self.indf
        else:
            d = df
        return d[(d.logar.str[-3:]=='.02') & (d.logar.str.len()>9)].copy()
        
    def get_current_year(self, df=None):
        '''
        Επιστρέφει μόνο τους λογαριασμούς που είναι χαρακτηρισμένοι ως .01
        αφορούν δηλαδή ποσά τρέχουσας χρήσης.
        :param df: The dataframe to work with
        :return: a copy of the original dataframe with current year
        '''
        if df is None:
            d = self.indf
        else:
            d = df
        return d[(d.logar.str[-3:]=='.01') & (d.logar.str.len()>9)].copy()
        
    def get_data_by_enotites(self, enotites):
        '''
        Επιστρέφει τα δεδομένα συγκεκριμένων ενοτήτων που δίνονται ως λίστα.
        :param enotites: List with codes enotiton
        :return: Dataframe with selected enotites
        '''
        pass
    
if __name__ == '__main__':
    db = DataFramesBuilder()