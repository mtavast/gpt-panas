#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 22:13:08 2021

@author: tavastm1
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 21:35:25 2021

@author: tavastm1
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Import the human reference data
sesoi = pd.read_csv('HumanData/PANAS_SESOI.csv')

# Import gpt data
engines = []
engines.append('davinci')
replication_number = 1
experiment_list = ['PANAS_bl']
titles = ['GPT-3 Davinci']

# Dataframes to a dictionary
experiment_dfs = {}
for experiment in experiment_list:
    for engine in engines:
        experiment_dfs[f'{experiment}_{engine}'] = pd.read_csv(f'Output/{experiment}_{engine}_R{replication_number}.csv')


#%% Scale Scores
import pandas as pd
negatives = []
positives = []
positives_t = pd.Series()

NumOfRows = len(sesoi)
temp_data = sesoi
    
for i in range(NumOfRows):
    data = temp_data.iloc[i,:]
    answers_positive = data["interested"] + data["excited"] + data["strong"] + data["alert"] + data["enthusiastic"] + data["proud"] + data["inspired"] + data["determined"] + data["attentive"] + data["active"] 
    answers_negative = data["distressed"] + data["upset"] + data["guilty"] + data["scared"] + data["hostile"] + data["irritable"] + data["ashamed"] + data["nervous"] + data["jittery"] + data["afraid"] 
    positives.append(answers_positive)
    negatives.append(answers_negative)
    ## Just testing
    positives_s = pd.Series(answers_positive)
    positives_t = positives_t.append(positives_s)
      
    
print(f'{engine} Positives:', round((sum(positives) / len(positives)), ndigits=1), 'SD: ', round(np.std(positives), ndigits=1))
print(f'{engine} Negatives:', round((sum(negatives) / len(negatives)), ndigits=1), 'SD: ', round(np.std(negatives), ndigits=1))
                #print(f'{experiment_name} Balance:', (sum(affectbalance) / len(affectbalance)))
#%% Scale Scores
compare = {'sesoi': sesoi, 'GPT': experiment_dfs['PANAS_bl_davinci']}

for column_i in range(20):
    for item in compare:
        temp_list = []
        temp = compare[item]
        NumOfRows = len(temp)
        temp = temp[["interested", "excited", "strong", "alert", "enthusiastic", "proud", "inspired", "determined", "attentive", "active", "distressed", "upset", "guilty", "scared", "hostile", "irritable", "ashamed", "nervous", "jittery", "afraid"]]
        for i in range(NumOfRows):
            if i == NumOfRows - 1:
                data = temp.iloc[i,column_i]
                temp_list.append(data)
                column_name = temp.columns[column_i]
                print(f' {column_name} {item} Column mean', sum(temp_list) / len(temp_list), 'Length', len(temp_list))
            else:
                data = temp_data.iloc[i,column_i]
                temp_list.append(data)

#%% Bar chart
plt.rcParams['legend.title_fontsize'] = '24'
experiment = 'PANAS_bl'
TitleTemp = 'GPT-3 Davinci'
sesoi = sesoi[["interested", "excited", "strong", "alert", "enthusiastic", "proud", "inspired", "determined", "attentive", "active", "distressed", "upset", "guilty", "scared", "hostile", "irritable", "ashamed", "nervous", "jittery", "afraid"]]
labels = [1, 2, 3, 4, 5]
GPT = experiment_dfs[f'{experiment}_davinci']
GPT = GPT[["interested", "excited", "strong", "alert", "enthusiastic", "proud", "inspired", "determined", "attentive", "active", "distressed", "upset", "guilty", "scared", "hostile", "irritable", "ashamed", "nervous", "jittery", "afraid"]]
fig = plt.figure()


for i in range(20):
    plt.style.use('ggplot')
    plt.subplot(4,5,i+1)
    ## SESOI DATA
    temp = sesoi.iloc[:, i]
    column_title = GPT.columns[i]
    temp2 = Counter(temp)
    # Dictionary keys contains values for 1-5, divide by number of total observations
    means_sesoi = [temp2[1] / len(temp), temp2[2] / len(temp), temp2[3] / len(temp), temp2[4] / len(temp), temp2[5] / len(temp)]
    # GPT data
    temp = GPT.iloc[:, i]
    temp2 = Counter(temp)
    # Dictionary keys contains values for 1-5, divide by number of total observations
    means_gpt = [temp2[1] / len(temp), temp2[2] / len(temp), temp2[3] / len(temp), temp2[4] / len(temp), temp2[5] / len(temp)]


    x = np.arange(start=1,stop=6)  # the label locations
    width = 0.25  # the width of the bars
   
    rects1 = plt.bar(x - width, means_gpt, width, label='GPT-3 Davinci')
    rects2 = plt.bar(x, means_sesoi, width, label='Human Data [1]')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.title(f'{column_title}')
    if i > 14:
        plt.xticks(x)        
        plt.grid(axis='x')
    else:
        plt.xticks([])

    if i == 0:
        plt.figlegend(fontsize='16', loc='upper right', bbox_to_anchor=(1, 1))
        plt.suptitle(f'Item level PANAS responses for GPT-3 Davinci and Human reference data', fontsize=22)
   
plt.subplots_adjust(right=0.88)   
manager = plt.get_current_fig_manager()
manager.window.showMaximized()  
plt.show() 
fig.set_size_inches((18.5, 8.5), forward=False)
plt.savefig(f'Figures/GPTHumans_{TitleTemp}.png', dpi=500)