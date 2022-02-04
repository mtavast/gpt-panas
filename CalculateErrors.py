#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 16:50:15 2021

This script is used to calculate the number of errors from the log files. 

@author: tavastm1
"""
#from tabulate import tabulate

# All the log files
LogList = ['PANAS_bl_ada_R1.log',
           'PANAS_bl_babbage_R1.log',
           'PANAS_bl_curie_R1.log',
           'PANAS_bl_davinci_R1.log']

# Find all the lines in each log file, put in a dictionary
LogDict = {}
for logfile in LogList:
    lines_list = []
    f=open(logfile)
    lines = f.readlines()
    LogDict[logfile] = lines

# Search the log files line by line for the word ERROR. This means that the interview was stopped due to a incoherent answer.
ErrorList = {}
ErrorPercent = []
for logfile in LogList:
    #print(logfile)
    temp_log = LogDict[logfile]
    NumOfErrors = 0
    for i in range(len(temp_log)):
        temp = temp_log[i]
        if 'ERROR' in temp:
            NumOfErrors += 1
        else:
            pass
        if i == len(temp_log) -1:
            temp_list = []
            temp_list.append(logfile)
            temp_list.append((NumOfErrors / len(temp_log)) * 100) # Percentage of errors
            ErrorList[logfile] = NumOfErrors
            # List of lists
            ErrorPercent.append(temp_list)

#print(tabulate(ErrorPercent,headers=["Experimental condition", "Percentage of errors"], tablefmt="latex"))

for i in range(len(ErrorPercent)):
    print(ErrorPercent[i][0], round(ErrorPercent[i][1], ndigits=2))
    

# =============================================================================
# ### Can be used to print the log filenames
# engines = ['ada', 'davinci']
# experiments = ['PANAS_bl', 'PANAS_bl_only_verbal_anchors', 'PANAS_bl_likertverbalization', 'PANAS_bl_EEV', 'PANAS_bl_EEV_singleQ']
# for engine in engines:
#     for i in range(len(experiments)):
#         temp = experiments[i]
#         temp2 = f'{temp}_{engine}_R1.log'
#         print(temp2)
# ###
# =============================================================================
