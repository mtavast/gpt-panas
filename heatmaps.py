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
import os
import collections
from gpt_psych import score_panas
from collections import Counter

#########   Set up and load data ############

engines = []
engines.append('PANAS_bl_ada')
engines.append('PANAS_bl_babbage')
engines.append('PANAS_bl_curie')
engines.append('PANAS_bl_davinci')
replication_number = 1
experiment_list = ['PANAS_bl']
titles = ['Ada', 'Babbage', 'Curie', 'Davinci']
# Dataframes to a dictionary
experiment_dfs = {}
for engine in engines:
    experiment_dfs[f'{engine}'] = pd.read_csv(f'Output/{engine}_R{replication_number}.csv')

# Import human data
sesoi = pd.read_csv('HumanData/PANAS_SESOI.csv')
experiment_dfs['Human_sesoi'] = sesoi    # add to dictionary
engines.append('Human_sesoi')            # and for plotting
        
#%%
#% Plot heatmaps  
# Correlation matrices
corr_matrices = []
for engine in engines:
    temp = experiment_dfs[f'{engine}']    # takes the string and interprets it as a expression
    #temp = temp[["interested", "excited", "strong", "alert", "enthusiastic", "proud", "inspired", "determined", "attentive", "active", "distressed", "upset", "guilty", "scared", "hostile", "irritable", "ashamed", "nervous", "jittery", "afraid"]]
    # Same order as in the origianl PANAS validation study tables
    temp = temp[['enthusiastic','interested','determined', 'excited', 'inspired', 'alert', 'active', 'strong', 'proud', 'attentive', 'scared', 'afraid', 'upset', 'distressed','jittery', 'nervous', 'ashamed', 'guilty', 'irritable','hostile']]

    corr_matrices.append(temp.corr(method='spearman'))

print(corr_matrices[0].min().min(), corr_matrices[1].min().min(), corr_matrices[2].min().min(), corr_matrices[3].min().min(), corr_matrices[4].min().min())

titles = ['GPT-3 Ada', 'GPT-3 Babbage', 'GPT-3 Curie', 'GPT-3 Davinci', 'Human data [1]']
titles = titles*2
fsize=8     # ticks
fsize2= 16  # titles
cbmin = -1    # from -1 to 1

for count, item in enumerate(corr_matrices):
    titles_ = titles[count]
    # Ylabels
    if count == 0:
        plt.subplot(1,5,count+1)
        sns.heatmap(item, square=True, cbar=False, vmin=cbmin, vmax=1, yticklabels=1, xticklabels=3)
        plt.title(f'{titles_}', fontsize=fsize2)
        plt.xticks(fontsize=fsize)
            # Rownames
    elif count == 2:
        plt.subplot(1,5,count+1)
        sns.heatmap(item, square=True, cbar=False, vmin=cbmin, vmax=1, yticklabels=False, xticklabels=3)
        plt.title(f"Correlation heatmaps (Spearman's) \n \n \n {titles_}", fontsize=fsize2)
        plt.xticks(fontsize=fsize)
    # Colorbar
    elif count == 4:
        fig = plt.gcf()
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.83, 0.38, 0.010, 0.23])
        plt.subplot(1,5,count+1)
        sns.heatmap(item, square=True, cbar=True, cbar_ax=cbar_ax, vmin=cbmin, vmax=1, yticklabels=False, xticklabels=3)
        plt.title(f'{titles_}', fontsize=fsize2)
        plt.xticks(fontsize=fsize)
        #plt.suptitle("Correlation heatmaps (Spearman's)", fontsize=16, y=0.96, x=0.47, fontweight="bold")
    else:
        plt.subplot(1,5,count+1)
        sns.heatmap(item, square=True, cbar=False, vmin=cbmin, vmax=1, yticklabels=False, xticklabels=3)
        plt.title(f'{titles_}', fontsize=fsize2)
        plt.xticks(fontsize=fsize)
        
plt.show()
manager = plt.get_current_fig_manager()
manager.window.showMaximized()
fig.set_size_inches((15, 8.5), forward=False)
plt.savefig('Figures/Heatmaps.png', dpi=500)


#%% Score panas
            
n_participants = 150
Balance = {}
PosS = {}
NegS = {}
for engine in engines:
    if engine == 'Human_sesoi':
        pass
    else:
        datapath = f'Results/PANAS_bl/'
        affectbalance = []
        positives = []
        negatives = []
        for participant in range(n_participants):  
            filename = os.path.join(datapath, f'{engine}_P{participant}_answers_Rep{replication_number}.csv')
            temp, temp2, temp3 = score_panas(filename)
            affectbalance.append(temp)
            positives.append(temp2)
            negatives.append(temp3)
            # Add the data to the dictionary when the final participant
            if participant == n_participants - 1:
                print(f'{engine} Positives:', round((sum(positives) / len(positives)), ndigits=1), 'SD: ', round(np.std(positives), ndigits=1))
                print(f'{engine} Negatives:', round((sum(negatives) / len(negatives)), ndigits=1), 'SD: ', round(np.std(negatives), ndigits=1))
                #print(f'{experiment_name} Balance:', (sum(affectbalance) / len(affectbalance)))
                Balance[f'{engine}_'] = affectbalance
                PosS[f'{engine}_'] = positives
                NegS[f'{engine}_'] = negatives
                                    
            
        
