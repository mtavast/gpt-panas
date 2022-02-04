#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 21:40:00 2021

@author: tavastm1
"""

import pandas as pd
import os
from gpt_psych import score_panas

##
n_participants = 150
#experiment_names = ['PANAS_bl_EEV_singleQ']

experiment_names = ['PANAS_bl']
#experiment_names.extend(['PANAS_bl', 'PANAS_bl_only_verbal_anchors', 'PANAS_bl_EEV', 'PANAS_bl_EEV_singleQ', 'PANAS_bl_likertverbalization'])

engine = 'curie'
replication_number = 1

for experiment_name in experiment_names:
    datapath = f'Results/{experiment_name}/'
    answers = []
    for participant in range(n_participants):  
        filename = os.path.join(datapath, f'{experiment_name}_{engine}_P{participant}_answers_Rep{replication_number}.csv')
        #temp, temp2, temp3 = score_panas(filename)
        #temp = pd.read_csv(filename)
        if participant == 0:
            answers = pd.read_csv(filename,index_col=False)  # use the first as starting point for appending
            items = answers.columns          # items are the column names
        else:
            temp = pd.read_csv(filename)
            answers = answers.append(temp,ignore_index=True)
        
    # Save the answers, to be continued in R
    answers.to_csv(f'Output/{experiment_name}_{engine}_R{replication_number}.csv', index=False)    
 