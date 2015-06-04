#-*- coding:utf-8 -*-

'''
Το αρχείο περιέχεις συναρτήσεις που χρησιμοποιώ τόσο για τους απολογισμούς όσο και για τους 
προϋπολογισμούς.
'''


#Ορισμοί Δομών Δεδομένων απαραίτητων για την ανάλυση
#Οι τίτλοι των χιλιάδων από τους ΚΑΕ
titles={'0':'PLIROMES GIA YPIRESIES',
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
exnames = ['logar','perigrafi','proteinomenos','eggekrimenos','anamorfoseis','diamorfomenos','desmefthenta','entalthenta','proplirothenta','plirothenta']

#Set the columns names for esoda
esnames = ['logar','perigrafi','proteinomenos','eggekrimenos','anamorfoseis','diamorfomenos']


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