#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 01:21:57 2022

@author: tavastm1
"""

import pandas as pd

# Data from osf
Human_data = pd.read_csv('HumanData/PANAS_total_analysis_data.csv')

# Only the T1 data, the first 20 columns
Human_data = Human_data.iloc[:,0:20]

# Drop the T1_NA and T1_PA from the column names
Human_data.columns = Human_data.columns.str.replace('T1_PA', '')
Human_data.columns = Human_data.columns.str.replace('T1_NA', '')

# Save the data as a csv-file
Human_data.to_csv(f'HumanData/PANAS_SESOI.csv', index=False)    
