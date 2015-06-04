# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 22:08:20 2014

@author: urban
"""

import csv

def string_to_number(instr):
    '''Convert string to numbers. Mainly because of different notation'''
    
    pass


def exFile(inFile, outFile):
    #Read in the file to work with
    in_file = open(inFile,'r',encoding='utf-8')
    freader = csv.reader(in_file,delimiter=';')
    out_file = open(outFile,'w',encoding='utf-8')
    header = True
    counter = 0
    new_parts = [] # the parts to be added in each row
    for row in freader:
        counter = counter + 1
        if not header:
            logar = row[1] #store logariasmo
            parts = logar.split('.') #brake logariasmo into parts
            new_parts = [] #new parts to be added
            vathmos = len(parts) #store vathmo
            new_parts.append(str(vathmos))
            try:
                new_parts.append(parts[1]) #enotita
            except Exception:
                new_parts.append('')
            try:
                new_parts.append(parts[2]) #foreas
            except Exception:
                new_parts.append('')
            try:
                new_parts.append(parts[3]) #kae
            except Exception:
                new_parts.append('')
            if vathmos>2:
                if parts[-1] == '01': #trexon
                    new_parts.append('1') 
                elif parts[-1] == '02':
                    new_parts.append('2')
                else:
                    new_parts.append('0')
            else:
                new_parts.append('0')
            
            for i in range(3,len(row)-3):
                row[i] = row[i].replace('.','')
                row[i] = row[i].replace(',','.')
        else:
            #work with header
            new_parts = ['vathmos','enotita','foreas','kae','trexon']
            header = False
            
        str_parts = ';'.join(new_parts)
        row.append(str_parts)
        print(';'.join(row),file=out_file)
    print(counter)
    in_file.close()
    out_file.close()

def esFile(inFile, outFile):
    #Read in the file to work with
    in_file = open(inFile,'r',encoding='utf-8')
    freader = csv.reader(in_file,delimiter=';')
    out_file = open(outFile,'w',encoding='utf-8')
    header = True
    counter = 0
    new_parts = [] # the parts to be added in each row
    for row in freader:
        counter = counter + 1
        if not header:
            logar = row[1] #store logariasmo
            parts = logar.split('.') #brake logariasmo into parts
            new_parts = [] #new parts to be added
            vathmos = len(parts) #store vathmo
            new_parts.append(str(vathmos))
            try:
                new_parts.append(parts[1]) #enotita
            except Exception:
                new_parts.append('')
            try:
                new_parts.append(parts[2]) #foreas
            except Exception:
                new_parts.append('')
            try:
                new_parts.append(parts[3]) #kae
            except Exception:
                new_parts.append('')
                
            for i in range(3,len(row)-3):
                row[i] = row[i].replace('.','')
                row[i] = row[i].replace(',','.')
            
        else:
            #work with header
            new_parts = ['vathmos','enotita','foreas','kae']
            header = False
            
        str_parts = ';'.join(new_parts)
        row.append(str_parts)
        print(';'.join(row),file=out_file)
    print(counter)
    in_file.close()
    out_file.close()

if __name__ == "__main__":
    exFile('ex2011_2014.csv','final_ex2011_2014.csv')
    esFile('es2011_2014.csv','final_es2011_2014.csv')
