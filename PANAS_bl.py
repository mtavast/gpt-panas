#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:35:35 2021

The whole questionnaire without experience description, using similar prime as in the original study.
      In this case, previously answered questions are included in the prompt, but their order is randomzied to counteract
      the recency bias. No vberbalization of the Likert answers

@author: tavastm1
"""
import csv
from gpt_psych import  panas_items, trim_response, randomize_examples, log_answer, shuffle_prompt
import pandas as pd
import openai
import copy
import random

##################################################
#################### SETTINGS ####################
##################################################
openai.api_key = open("key.txt", "r").read() # To reproduce the code, you need to create a txt file with your openai key
start = 126
end = 150
engine = "curie"
experiment_name = 'PANAS_bl'
replication_number = 1
logfile = f'{experiment_name}_{engine}_R{replication_number}.log'
#################################################

for participant in range(end):
    if participant >= start:
        answers = []  
        # Read everything needed for the prompt
        prompt_start=open("prompts/Interview_start.txt", "r").read()
        questionnaire_instructions = open("prompts/PANAS_instructions.txt", "r").read()
        practice_intro = open("prompts/practice_intro.txt", "r").read()
        participants_df = pd.read_csv("Matlab/participants.csv", header=None)
        participant_text = participants_df[0][participant]
        # Randomize the example order
        examples = randomize_examples(verbalize=False)                        # the participant number controls the random seed
        # Put it all together
        prompt_initial = prompt_start + "\n" + participant_text + "\n\n" + practice_intro + "\n\n" + examples + "\n\n" + questionnaire_instructions
        item_list = [] # for item shuffling
        item_order_orig = [] # for logging
        panas_items = random.sample(panas_items, k=len(panas_items))
        # Query responses
        for count, item in enumerate(panas_items):
            item_order_orig.append(item)
            item_q  = f'\n\nResearcher: On a scale from 1 to 5, where 1 is "strongly disagree" and 5 is "strongly agree", please rate the statement "Right now I feel {item}.'
            item_list.append(item_q)
            # This is for saving the full interwiev with a readable flow (in reality with every query the items are shuffled)
            itemQuerySuffix="\n\nParticipant:"
            if count == 0:
                prompt_full=prompt_initial+item_q+ '"' + itemQuerySuffix  
            else:
                prompt_full=prompt_full+item_q+ '"' + itemQuerySuffix
            #
            # Shuffle items
            prompt, item_order = shuffle_prompt(prompt=prompt_initial, items=item_list, item_number=count, item_order=item_order_orig)

            #query response
            print("Querying for item: ",item)
            response = openai.Completion.create(engine=engine, prompt=prompt, max_tokens=64,
                                                #these are the default OpenAI playground parameters
                                                temperature=0.7,
                                                top_p=1.0,
                                                frequency_penalty=0,
                                                presence_penalty=0,
                                                best_of=1)
            response_orig=response["choices"][0]["text"]
        
            #trim response
            response = trim_response(response_orig)
            #add response to prompt and to items in the item list
            prompt_temp = copy.deepcopy(prompt) + response
            prompt_full=prompt_full+response
            item_list[-1] = item_list[-1] + "\"\n\nParticipant:" + response
            # log the prompt and the response
            log_answer(response, logfilename=logfile, item=item, engine=engine, participant=participant, replication_number=replication_number,  prompt_logging = prompt , response_logging = response_orig, item_order = item_order)
            # Find the answer
            ans = int(response[1]) 
            if ans != 1 and ans != 2 and ans != 3 and ans != 4 and ans != 5:
                raise ValueError('Answer not an integer between 1-5')
            answers.append(ans)
            #print(prompt)
        # Finally save the answers
        with open(f'Results/{experiment_name}/{experiment_name}_{engine}_P{participant}_answers_Rep{replication_number}.csv', mode='w') as csv1:
            writer = csv.writer(csv1, delimiter=',')
            writer.writerow(panas_items)    # items as column headers
            writer.writerow(answers)        # answers to rows
            
        with open(f'Results/{experiment_name}/{experiment_name}_{engine}_P{participant}_interview_Rep{replication_number}.txt', mode='w') as interview:
            interview.writelines(prompt_full) 