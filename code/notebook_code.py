#Initialization code
#make plotting inline
#%matplotlib inline

#import the libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Import custom libraries
from analysis import Analysis
import fin_functions as funcs

#Setting some options
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier\n"
pd.set_option('expand_frame_repr',True)
pd.set_option('use_inf_as_null',True)
plt.rcParams['figure.figsize'] = (15, 5)
pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x)) #Set thousands separator

work = Analysis()
dc = work.get_clean()
#From analysis.ipynb
dc13 = dc[dc['etos']==2013]
enotites_counts = dc13['enotita'].value_counts(normalize=True, sort=False)
enotites_counts.plot(kind='barh', rot=0)
by_forea_enotita = dc.groupby(['foreas','enotita'])
agg_counts = by_forea_enotita.size().unstack().fillna(0)

norm_agg_counts = agg_counts.div(agg_counts.sum(1),axis=0)
norm_agg_counts.plot(kind='barh', stacked=True)
#From apologismos_2013_2015
#read the two sheets from excel file
total_cols = pd.read_excel('apologismos_2013_2015.xls',sheetname=3,header=0,parse_cols='A:I')
total_rows = pd.read_excel('apologismos_2013_2015.xls',sheetname=4,header=0,parse_cols='A:T')
#Sort by enotita and month
tr_sorted_by_source = total_rows.sort(['source','month'],ascending=[1,1])
enot = 3
xron = 14
tr_thess = funcs.build_enotita_year_img(enot,xron,tr_sorted_by_source)
tr_thess[['pct_egg_desm'+str(xron),'pct_egg_timol'+str(xron),'pct_egg_ental'+str(xron),'pct_egg_plir'+str(xron)]].plot()
tr_thess[['egg'+str(xron),'diam'+str(xron),'cs_desm'+str(xron),'cs_timol'+str(xron),'cs_ental'+str(xron),'cs_plir'+str(xron)]].plot()

#From ex11_14
df_raw = pd.read_csv('../data/ex_work_data.txt', sep=';', encoding='utf8',low_memory=False,index_col=False) #Read in the file
df = df_raw.copy()
#df[(df.A == 1) & (df.D == 6)]
#Δημιουργία μάσκας για αλυσιδωτό φιλτράρισμα
def mask(df,key,value):
    return df[df[key]==value]
#Εμφάνιση μόνο τεταρτοβάθμιων με διαμορφωμένο προϋπολογισμό διάφορο του 0
df1 = df[(df.vathmos>4) & (df.diamorfomenos!=0.0) & (df.trexon==1)]
df1[['diamorfomenos','eggekrimenos']].describe()
#Δημιουργία ενός αντιγράφου συγκεκριμένων στηλών από το αρχικό dataframe
dfcola = df[['etos','enotita','kae','eggekrimenos','diamorfomenos']]
dfcola = dfcola[(dfcola.diamorfomenos != 0)]
dfcola.diamorfomenos.plot()
#pd.crosstab(index=dfcola.etos, columns=dfcola.enotita,values=dfcola.diamorfomenos)

#Εξαιρούμε τις γραμμές όπου έχουμε ανυπαρξία ή μηδενική τιμή στο διαμορφωμένο προϋπολογισμό
dfClean = df_raw[(df_raw['diamorfomenos'].notnull()) & (df_raw['diamorfomenos'] != 0.0) & (df_raw['etos'].notnull()) & (df_raw['enotita'].notnull())]
#Δημιουργία crosstab για την παρακολούθηση των ενοτήτων ανά έτος
ctEtosEnotita = pd.crosstab([dfClean.etos,dfClean.foreas],[dfClean.enotita],values=dfClean.eggekrimenos,aggfunc=np.mean)
#Επιλογή μόνο ορισμένων στηλών
dfs = dfClean[['etos','enotita','kae','foreas','eggekrimenos','diamorfomenos']]
dfs = dfClean[['kae','eggekrimenos','diamorfomenos']]
dfClean.plot(kind='scatter',x='eggekrimenos',y='entalthenta')

def do_scatter_enotita(df, x_name, y_name, wid, hei):
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
        plt.scatter(p_data[x_name], p_data[y_name], s=60, c=clrs[i], label=i)
        plt.legend()
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        
def do_scatter_etos(df, x_name, y_name, wid, hei):
    clrs = ['r','b','g','c']
    j=1
    fig = plt.figure(1,figsize=(wid,hei)) #set the figure
    for i in [2011,2012,2013,2014]:
        p_data = df[df.etos == i].dropna()
        if j == 1:
            ax = fig.add_subplot(4,1,j)
        else:
            fig.add_subplot(4,1,j,sharex = ax, sharey=ax)
        plt.scatter(p_data[x_name], p_data[y_name], s=60, c=clrs[j-1], label=i)
        plt.legend()
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        j = j+1
        
def do_scatter_etos_enotita(df, x_name, y_name, wid, hei):
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
            plt.scatter(p_data[x_name], p_data[y_name], s=60, c=clrs[i], label= yrs[j])
            plt.legend()
            
#Από το αρχικό dataframe φιλτράρουμε μόνο τις εγγραφές του έτους
etos = 2013
df2011 = df_raw[(df.etos == etos)]

#Εξαιρούμε τις γραμμές όπου έχουμε ανυπαρξία ή μηδενική τιμή στο διαμορφωμένο προϋπολογισμό
df2011 = df2011[(df2011['diamorfomenos'].notnull()) & (df2011['diamorfomenos'] != 0.0)]
do_scatter_enotita(dfClean, 'diamorfomenos','plirothenta', 15, 30)
do_scatter_etos(df_raw,'diamorfomenos','plirothenta', 15, 15)
do_scatter_etos_enotita(df_raw,'diamorfomenos','plirothenta',15,30)

df14 = df_raw[(df_raw.etos == 2014)]
df14 = df14[(df14['diamorfomenos'].notnull()) & (df14['diamorfomenos'] != 0.0)]
df14_counts = df14['enotita'].value_counts()
df14_counts.plot(kind='barh',rot=0)
#From proipologismoi12-14.ipynb
df = pd.read_csv('proipol12_14.csv', sep=';', encoding='utf8') #Read in the file
dfex = df[df.a==2] #exoda
dfes = df[df.a==6] #esoda
ex = dfex[dfex.etos < 2015] #exoda 2012-2014
es = dfes[dfes.etos < 2015] #esoda 2012-2014
exgp = ex.groupby(['c','etos'],as_index=False) #group by KAE and enotita
exgp.size()#display the size of groups
exgp.describe()#Describe the groups
#Work with diamorfomenos
exgp[['eggek','diam']].agg([np.mean,np.std]).reset_index()
#From proipologismoi.ipynb
#Set an array for the filenames
ex_names = ['ex_2012','ex_2013','ex_2014']
es_names = ['es_2012','es_2013','es_2014']

#Διάβασμα των αρχείων εξόδων
exdfs = {}
for dfname in ex_names: 
    #print dfname
    exdfs[dfname] = pd.read_excel(dfname +'.xls',sheetname=0,header=None,skiprows=1, parse_cols='A:J',names=funcs.exnames)
    
#Διάβασμα των αρχείων εσόδων
esdfs = {}
for dfname in es_names:
    #print dfname
    esdfs[dfname] = pd.read_excel(dfname +'.xls',sheetname=0,header=None,skiprows=1, parse_cols='A:F',names=funcs.esnames)
    
#Διάβασμα του αρχείου δεδομένων
cur_year = '2013'
df = exdfs['ex_' + cur_year]

#Προσθήκη των απαραίτητων πεδίων με χρήση του αρχείου συναρτήσεων
df = funcs.format_dataframe(df)

#Φιλτράρισμα όλων των κωδικών που είναι πρωτογενείς και έχουν διαμορφομένο προϋπολογισμό
dfclean = df[(df.diamorfomenos != 0) & (df.logar.str[-1:] != '0') & (df.logar.str.len() > 9)] 

#Υπολογίζουμε τα συνολικά αθροίσματα για τα παρακάτω πεδία
total_sums = dfclean[['eggekrimenos','diamorfomenos','plirothenta','entalthenta']].sum()
#Μόνο αριθμητικά δεδομένα

#Ομαδοποιούμε κατά ενότητα
grp_enotita = dfclean.groupby('enotita')
grp_enotita.head()

#Αφαιρούμε τα επενδυτικά δηλαδή τη χιλιάδα 9
dfpagia = dfclean[dfclean.xiliada != '9']
t = dfpagia[['eggekrimenos','diamorfomenos','plirothenta','entalthenta']].sum()

#Γράφημα χιλιάδας
target_var = 'eggekrimenos'
df1 = df[df.last_three == '000'].iloc[:,2:]
df2 = df1.pivot_table(target_var,index='enotita',columns='kae',aggfunc='sum')
df3 = df2.div(df2.sum(1),axis=0)
df3.plot(kind='bar',stacked=True,colormap=cmap,figsize=(12,8))

#Ανάλυση χιλιάδων σε εκατοντάδες - Μόνο το 0000 που είναι και ο κύριος όγκος
for i in '0':
    df1 = df[(df.xiliada == i) & (df.last_two == '00') & (df.last_three != '000')].iloc[:,2:]
    df2 = df1.pivot_table('plirothenta',index='enotita',columns='kae',aggfunc='sum')
    df3 = df2.div(df2.sum(1),axis=0)
    df3.plot(kind='bar',stacked=True,colormap=cmap,figsize=(12,8),title=titles[i])
    
#Ανάλυση χιλιάδων σε εκατοντάδες - Οι υπόλοιπες χωρίς τη 0000
for i in '123456789':
    df1 = df[(df.xiliada == i) & (df.last_two == '00') & (df.last_three != '000')].iloc[:,2:]
    df2 = df1.pivot_table('plirothenta',index='enotita',columns='kae',aggfunc='sum')
    df3 = df2.div(df2.sum(1),axis=0)
    df3.plot(kind='bar',stacked=True,colormap=cmap,figsize=(12,8),title=titles[i])
    
#Καταγραφή των λογαριασμών που αντιστοιχούν σε φορείς
foreis = df[(df.logar.str.len() == 9) & (df.enotita == '01')]
foreis = foreis[['foreas','perigrafi']]
foreis

#Ανάλυση σε δεκάδες
temp = df[(df.xiliada == '0') & (df.logar.str[-3:-2] == '8') & (df.logar.str[-2:-1] != '0')  ]
t = df[(df.kae == '0873') & (df.eggekrimenos != 0)]
t[['logar','perigrafi','eggekrimenos']]

#From proipologismoi-copy.ipynb
#Set the columns names for exoda
exnames = ['logar','perigrafi','proteinomenos','eggekrimenos','anamorfoseis','diamorfomenos','desmefthenta','entalthenta','proplirothenta','plirothenta']
#Set the columns names for esoda
esnames = ['logar','perigrafi','proteinomenos','eggekrimenos','anamorfoseis','diamorfomenos']

#Set an array for the filenames
ex_names = ['ex_2012','ex_2013','ex_2014']
es_names = ['es_2012','es_2013','es_2014']

exdfs = {}
for dfname in ex_names: 
    #print dfname
    exdfs[dfname] = pd.read_excel(dfname +'.xls',sheetname=0,header=None,skiprows=1, parse_cols='A:J',names=exnames)
    
esdfs = {}
for dfname in es_names:
    #print dfname
    esdfs[dfname] = pd.read_excel(dfname +'.xls',sheetname=0,header=None,skiprows=1, parse_cols='A:F',names=esnames)
    
reload(funcs)
ex_foreas_13 = funcs.build_dataframe_forea(exdfs['ex_2013']) 
es_foreas_13 = funcs.build_dataframe_forea(esdfs['es_2013'])

ex_foreas_14 = funcs.build_dataframe_forea(exdfs['ex_2014']) 
es_foreas_14 = funcs.build_dataframe_forea(esdfs['es_2014'])

merged = pd.merge(es_foreas_13,ex_foreas_13,on='foreas_enotita')
reload(funcs)
merged = funcs.calculate_diffs_on_year(merged)
merged.columns

pivot_enotita = merged.pivot_table('plirothenta',index='enotita_y',columns='foreas_y',aggfunc=sum)
normed_pivot_enotita = pivot_enotita.div(pivot_enotita.sum(1),axis=0)
from matplotlib import cm
cmap = cm.get_cmap('spectral')
normed_pivot_enotita.plot(kind='bar',stacked=True, figsize=(12,8), colormap=cmap)

normed_pivot_enotita

filter_merged = merged[merged.foreas_y == '071'].copy()
filter_merged[['foreas_y','perigrafi_y','enotita_y','plirothenta']]
pivot_forea = merged.pivot_table('plirothenta',index='foreas_y',columns='enotita_y',aggfunc=sum)
normed_pivot_forea = pivot_forea.div(pivot_forea.sum(1),axis=0)
normed_pivot_forea.plot(kind='bar',stacked=True, figsize=(12,8), colormap=cmap)
normed_pivot_forea
filter_merged = merged[merged.foreas_y == '293'].copy()
filter_merged[['foreas_y','perigrafi_y','enotita_y','plirothenta','entalthenta','desmefthenta']]

### Ενοποίηση του 2014 με βάση την ενότητα_φορέα και ανάλυση.
merged = pd.merge(es_foreas_14,ex_foreas_14,on='foreas_enotita')
reload(funcs)
merged = funcs.calculate_diffs_on_year(merged)
merged.columns
pivot_enotita = merged.pivot_table('plirothenta',index='enotita_y',columns='foreas_y',aggfunc=sum)
normed_pivot_enotita = pivot_enotita.div(pivot_enotita.sum(1),axis=0)
from matplotlib import cm
cmap = cm.get_cmap('spectral')
normed_pivot_enotita.plot(kind='bar',stacked=True, figsize=(12,8), colormap=cmap)
normed_pivot_enotita
filter_merged = merged[merged.foreas_y == '071'].copy()
filter_merged[['foreas_y','perigrafi_y','enotita_y','plirothenta']]
pivot_forea = merged.pivot_table('plirothenta',index='foreas_y',columns='enotita_y',aggfunc=sum)
normed_pivot_forea = pivot_forea.div(pivot_forea.sum(1),axis=0)
normed_pivot_forea.plot(kind='bar',stacked=True, figsize=(12,8), colormap=cmap)
normed_pivot_forea
filter_merged = merged[merged.foreas_y == '293'].copy()
filter_merged[['foreas_y','perigrafi_y','enotita_y','plirothenta','entalthenta','desmefthenta']]

###Πλήρης Ενοποίηση

def make_g(df):
    diam = df[['foreas','diamorfomenos','desmefthenta','entalthenta','plirothenta']]
    grp = diam.groupby('foreas') 
    g = grp.agg({'foreas': lambda x: x.iloc[0],'diamorfomenos':"sum",'desmefthenta':"sum",'entalthenta':"sum",'plirothenta':"sum"})
    return g

def make_g2(df):
    diam = df[['enotita','foreas','diamorfomenos','desmefthenta','entalthenta','plirothenta']]
    grp = diam.groupby(['foreas','enotita'])
    return grp

g13 = make_g(ex_foreas_13)
g14 = make_g(ex_foreas_14)

gg13 = make_g2(ex_foreas_13)
gg14 = make_g2(ex_foreas_14)
g13.sum()
g14.sum()
gm = pd.merge(g13,g14,on="foreas")
gm[['desmefthenta_x','desmefthenta_y']].plot(kind='bar')
df = exdfs['ex_2014']
df[(df.logar.str[11:]=='000') & (df.logar.str[3:5]=='01') & (df.diamorfomenos != 0)]
reload(funcs)
df = funcs.format_dataframe(df)
df[(df.kae == '9000') & (df.foreas == '721')]
#Γράφημα χιλιάδας
target_var = 'eggekrimenos'
df1 = df[df.last_three == '000'].iloc[:,2:]
df2 = df1.pivot_table(target_var,index='enotita',columns='kae',aggfunc='sum')
df3 = df2.div(df2.sum(1),axis=0)
df3.plot(kind='bar',stacked=True,colormap=cmap,figsize=(12,8))

#Ανάλυση χιλιάδων σε εκατοντάδες - Μόνο το 0000 που είναι και ο κύριος όγκος
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
for i in '0':
    df1 = df[(df.xiliada == i) & (df.last_two == '00') & (df.last_three != '000')].iloc[:,2:]
    df2 = df1.pivot_table('plirothenta',index='enotita',columns='kae',aggfunc='sum')
    df3 = df2.div(df2.sum(1),axis=0)
    df3.plot(kind='bar',stacked=True,colormap=cmap,figsize=(12,8),title=titles[i])
#Ανάλυση χιλιάδων σε εκατοντάδες - Οι υπόλοιπες χωρίς τη 0000
for i in '123456789':
    df1 = df[(df.xiliada == i) & (df.last_two == '00') & (df.last_three != '000')].iloc[:,2:]
    df2 = df1.pivot_table('plirothenta',index='enotita',columns='kae',aggfunc='sum')
    df3 = df2.div(df2.sum(1),axis=0)
    df3.plot(kind='bar',stacked=True,colormap=cmap,figsize=(12,8),title=titles[i])
#Καταγραφή των λογαριασμών που αντιστοιχούν σε φορείς
foreis = df[(df.logar.str.len() == 9) & (df.enotita == '01')]
foreis = foreis[['foreas','perigrafi']]
foreis
#Ανάλυση σε δεκάδες
temp = df[(df.xiliada == '0') & (df.logar.str[-3:-2] == '8') & (df.logar.str[-2:-1] != '0')  ]
t = df[(df.kae == '0873') & (df.eggekrimenos != 0)]
t[['logar','perigrafi','eggekrimenos']]