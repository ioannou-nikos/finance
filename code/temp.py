# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#tgpath = '../Documents/ThinkStats2/code/'
#import sys
#sys.path.insert(0,tgpath)

import analytic
import nsfg

df =  analytic.ReadBabyBoom(filename = tgpath+'babyboom.dat')
diffs = df.minutes.diff()
cdf = thinkstats2.Cdf(diffs, label='actual')
thinkplot.Cdf(cdf)
thinkplot.Show(xlabel='minutes',ylabel='CDF')

#Plot the complementary CDF
thinkplot.Cdf(cdf, complement=True)
thinkplot.Show(xlabel='minutes',ylabel='CDF',yscale='log')

df1 = nsfg.ReadFemPreg()
df1