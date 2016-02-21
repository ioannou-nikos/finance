# -*- coding:utf-8 -*-

__author__ = 'urban'

import fileinput  #Added for removing blank or empty lines
import pandas as pd
import numpy as np
import csv

#Ορισμοί Δομών Δεδομένων απαραίτητων για την ανάλυση
#Οι τίτλοι των φορέων ως προς τη σημασία τους
foreis_dict={'071':'PDE',
             '151':'_IDRIMATA,NEFROPATHEIS',
             '153':'_KATASKINOSEIS',
             '191':'_METAFORA MATHITON',
             '192':'_METAFORA MATHITON',
             '291':'_AGROTIKI OIKONOMIA',
             '292':'_KTINIATRIKI',
             '293':'_ALIEIA',
             '294':'_EGGEIES VELTIOSEIS',
             '390':'METAFORON IDIA ESODA',
             '721':'LEITOYRGIKA,IDIOI POROI, EKLOGES, OLATH ',
             '722':'TEO',
             '723':'ANTAPODOTIKA',
             '724':'ERGA KAP',
             '725':'ERGA KAP PKM',
}
#Οι τίτλοι των χιλιάδων από τους ΚΑΕ
xiliades_dict={'0':'PLIROMES GIA YPIRESIES',
        '1':'PROMITHIES AGATHWN KAI KEFALAIAKOY EXOPLISMOU',
        '2':'PLIROMES METABIBASTIKES',
        '3':'PLIROMES POU ANTIKRIZONTAI APO PRAGMATOPOIOUMENA ESODA',
        '4':'DAPANES NATO APO KRATOI MELH',
        '5':'DAPANES POU DEN ENTASSONTAI SE ALLES KATIGORIES',
        '6':'PLIROMES GIA THN EXYPHRETHSH THS DHMOSIAS PISTIS',
        '7':'APALOTRIOSEIS, AGORES, ANEGERSEIS ...',
        '8':'PLIROMES GIA ERGA P.D.E',
        '9':'PLIROMES GIA EPENDISEIS'}

#Set the columns names for exoda
exnames = ['logar','perigrafi','proteinomenos','eggekrimenos','anamorfoseis',
           'diamorfomenos','desmefthenta','entalthenta','proplirothenta','plirothenta']

#Set the columns names for esoda
esnames = ['logar','perigrafi','proteinomenos','eggekrimenos','anamorfoseis',
           'diamorfomenos']
           
enotites = { '00':'EDRA',
            '01':'THESSALONIKI',
            '02':'IMATHIA',
            '03':'KILKIS',
            '04':'PIERIA',
            '05':'PELLA',
            '06':'SERRES',
            '07':'CHALKIDIKI'
            }
def format_dataframe(indf):
    '''Τα δεδομένα είναι από τον προϋπολογισμό.
    Η συνάρτηση παίρνει το αρχείο εσόδων ή εξόδων και δημιουργεί τα παρακάτω νέα πεδία:
    eidos => logar[:2]
    enotita => logar[3:5]
    foreas => logar[6:9]
    kae => logar[10:14]
    xiliada => logar[10:11]
    ekatontada => logar[11:12]
    '''
    df = indf.copy()
    df['eidos'] = df.logar.str[:2]
    df['enotita'] = df.logar.str[3:5]
    df['foreas'] = df.logar.str[6:9]
    df['kae'] = df.logar.str[10:14]
    df['xiliada'] = df.logar.str[10:11]
    df['ekatontada'] = df.logar.str[11:12]
    df['last_three'] = df.logar.str[11:]
    df['last_two'] = df.logar.str[12:]
    df['first_two'] = df.logar.str[10:12]
    df['first_three'] = df.logar.str[10:13]
    return df
    
def build_enotita_year_img(enotita,xronia,dfsrc):
    ''' Τα δεδομένα που χρησιμοποιώ είναι από τον απολογισμό. 
    Δημιουργεί ένα αντίγραφο dataframe για την ενότητα και τη χρονιά,
    υπολογίζοντας παράλληλα τα προοδευτικά αθροίσματα για τα Δεσμευθέντα, Τιμολογηθέντα, 
    Ενταλθέντα και πληρωθέντα καθώς και το ποσοστό στο οποίο
    αυτά αντιστοιχούν επί του συνόλου.
    '''
    df = dfsrc[dfsrc.source == enotita].copy()
    df['cs_desm' + str(xronia)] = df['desm' + str(xronia)].cumsum()
    df['cs_timol' + str(xronia)] = df['timol' + str(xronia)].cumsum()
    df['cs_ental' + str(xronia)] = df['ental' + str(xronia)].cumsum()
    df['cs_plir' + str(xronia)] = df['plir' + str(xronia)].cumsum()
    df['pct_egg_desm' + str(xronia)] = 100 * df['cs_desm'+str(xronia)] / df['egg'+str(xronia)]
    df['pct_egg_timol' + str(xronia)] = 100 * df['cs_timol'+str(xronia)] / df['egg'+str(xronia)]
    df['pct_egg_ental' + str(xronia)] = 100 * df['cs_ental'+str(xronia)] / df['egg'+str(xronia)]
    df['pct_egg_plir' + str(xronia)] = 100 * df['cs_plir'+str(xronia)] / df['egg'+str(xronia)]
    return df
    
def build_dataframe_forea(dfsrc):
    ''' Τα δεδομένα που χρησιμοποιώ είναι από τον προϋπολογισμό. 
    Η συνάρτηση παίρνει ένα dataframe εσόδων ή εξόδων δημιουργεί αντίγραφο, 
    δημιουργεί νέα πεδία το φορέας_ενότητα (foreas_enotita) το φορέα (foreas), 
    την ενότητα (enotita), εάν είναι έσοδο ('06') ή έξοδο ('02') (eidos)'''
    df = dfsrc[dfsrc.logar.str.len()==9].copy()
    df['foreas_enotita'] = df.logar.str[3:] #create foreas_enotita
    df['foreas'] = df.logar.str[6:] #create foreas
    df['enotita'] = df.logar.str[3:5] #create enotita
    df['eidos'] = df.logar.str[:2] #create eidos
    return df 
    
def calculate_diffs_on_year(df):
    ''' Δεδομένα από προϋπολογισμό
    Υπολογίζω τα πεδία διαφορών στο δεδομένο ενοποιημένο dataframe.
    x είναι τα έσοδα
    '''
    df['diff_diames_desm'] = df['diamorfomenos_x'] - df['desmefthenta']
    df['diff_diames_ental'] = df['diamorfomenos_x'] - df['entalthenta']
    df['diff_diames_plir'] = df['diamorfomenos_x'] - df['plirothenta']
    
    df['diff_diamex_desm'] = df['diamorfomenos_y'] - df['desmefthenta']
    df['diff_diamex_ental'] = df['diamorfomenos_y'] - df['entalthenta']
    df['diff_diamex_plir'] = df['diamorfomenos_y'] - df['plirothenta']
    
    df['diff_eggex_diames'] = df['eggekrimenos_y'] - df['diamorfomenos_x']
    return df
    
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