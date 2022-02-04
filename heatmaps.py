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
                                    
            
#%%
######### Check histograms #########
count=0
# Ratings across items
for engine in engines:
    for value, experiment in enumerate(experiment_list):
        title_ = titles[value]
        count += 1
        temp = experiment_dfs[f'{experiment}_{engine}']
        temp2 = temp.iloc[:,:].values #np.array
        temp2 = temp2.flatten()
        plt.style.use('ggplot')
        plt.subplot(2,5,count)
        plt.hist(temp2)
        plt.title(f'{title_}')
        plt.suptitle('Histogram of responses generated arcoss all items')
        
#%%
######### Count the number of responses #########
count=0
ResponseDistribution = {}
# Ratings across items
for engine in engines:
    for value, experiment in enumerate(experiment_list):
        title_ = titles[value]
        count += 1
        temp = experiment_dfs[f'{experiment}_{engine}']
        temp2 = temp.iloc[:,:].values #np.array
        temp2 = temp2.flatten()
        ResponseDistribution[f'{experiment}_{engine}'] = collections.Counter(temp2)
        
dist = ResponseDistribution['PANAS_bl_only_verbal_anchors_davinci']

#%% Zoom to condition V in davinci (weird distribution)

ConditionV = experiment_dfs['PANAS_bl_only_verbal_anchors_davinci']
ConditionV= ConditionV[['enthusiastic','interested','determined', 'excited', 'inspired', 'alert', 'active', 'strong', 'proud', 'attentive', 'scared', 'afraid', 'upset', 'distressed','jittery', 'nervous', 'ashamed', 'guilty', 'irritable','hostile']]
PosItem = ConditionV.iloc[:,0:10]
NegItem = ConditionV.iloc[:,10:]
PosItem = PosItem.iloc[:,:].values #np.array
PosItem  = PosItem.flatten()
print('Positive item variance', np.var(PosItem))
PosItem = collections.Counter(PosItem)
NegItem = NegItem .iloc[:,:].values #np.array
NegItem  = NegItem.flatten()
print('Negative item variance', np.var(NegItem))
NegItem = collections.Counter(NegItem)
print('Positive item responses in davinci Condition V', Counter.most_common(PosItem))
print('Negative item responses in davinci Condition V', Counter.most_common(NegItem))
#%% Histograms 
# each item separately
for engine in engines:
    for experiment in experiment_list:
        plt.figure()
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        temp = experiment_dfs[f'{experiment}_{engine}']
        for i in range(20):
            plt.style.use('ggplot')
            plt.subplot(4,5,i+1)
            plt.hist(temp.iloc[:, i])
            temp = temp[['enthusiastic','interested','determined', 'excited', 'inspired', 'alert', 'active', 'strong', 'proud', 'attentive', 'scared', 'afraid', 'upset', 'distressed','jittery', 'nervous', 'ashamed', 'guilty', 'irritable','hostile']]
            column_title = temp.columns[i]
            plt.title(f'{column_title}')
            plt.suptitle(f'Item histograms {experiment} {engine}', fontsize=12)
            plt.show()
            plt.savefig(f'Figures/ItemHistogram_{experiment}_{engine}.png', dpi=300)
#%% The mean correlation across items, calculated from the upper triangular of the correlation matrix
# Only meaningful for ada, as this is done to demonstrate the high correlations apparent from the heatmaps.
# across all the items


for experiment in experiment_list:
    temp = experiment_dfs[f'{experiment}_ada']    # takes the string and interprets it as a expression
    temp = temp[['enthusiastic','interested','determined', 'excited', 'inspired', 'alert', 'active', 'strong', 'proud', 'attentive', 'scared', 'afraid', 'upset', 'distressed','jittery', 'nervous', 'ashamed', 'guilty', 'irritable','hostile']]
    temp = temp.corr(method='spearman')
    temp = temp.to_numpy() # to np. array
    CorrMask = np.mask_indices(20, np.triu, 1) # mask for the upper triangular, above diagonal
    temp = temp[CorrMask]                      # Include only the upper triangular
    temp = temp.flatten()
    print(f'{experiment} mean correlation:', round((sum(temp) / len(temp)), ndigits=2))
