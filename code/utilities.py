#-*- coding:utf-8 -*-

import fileinput #Added for removing blank or empty lines

def delete_blank_lines(flname):
    '''Delete all blank lines of a file'''
    for line in fileinput.FileInput(flname,inplace=1,backup='.bak'):
        #replace all \r
        line = line.replace('\r','')
        line = line.strip()
        if len(line) > 0:
            print line

def format_clean_file(in_name,out_name):
    #open file for reading
    fin = open(in_name,mode='r')
    #read all the lines
    lines = fin.readlines()
    #open file for writting
    fout = open(out_name,mode='w')
    #set the buffer
    buf = ''
    #loop through the lines
    for line in lines:
        if (line[:4].isdigit()) & (line[4:5]==';'):
            buf = line
            fout.write(buf)
            buf = ''
            continue
        line = line.strip()
        if line[:4].isdigit():
            if buf=='':
                buf = (line + ';')
                print buf
            else:
                fout.write(buf + '\n')
                buf = ''
        else:
            buf = buf + line
    
    
    