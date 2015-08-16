# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:30:38 2015

@author: urban
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Make some initial pandas configuration
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier\n"
pd.set_option('expand_frame_repr',True)
pd.set_option('use_inf_as_null',True)
plt.rcParams['figure.figsize'] = (15, 5)
pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x)) #Set thousands separator
