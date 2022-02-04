#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 12:01:37 2021

@author: tavastm1
"""
import pandas as pd
import random
import os
import logging
import copy


def transform_verbal_answer(response_to_be_transformed):
    """
    Checks

    Parameters
    ----------
    response_to_be_transformed : TYPE
        DESCRIPTION.

    Returns
    -------
    num_answer : TYPE
        Transforms verbal answers to numerical form.
        1=strongly disagree, 2=disagree, 3 = neither agree nor disagree, 4 = agree, 5 = strongly agree
        Will return 0, if it does not find correspondence with the likertanswers list.

    """
    likertanswers=[
    'Strongly agree',
    'strongly agree',
    'Agree',
    'agree',
    'Neither agree nor disagree',
    'neither agree nor disagree',
    'Disgree',
    'disagree',
    'Strongly disagree',
    'strongly disagree',
    ]
    
    numerical_answers=[
    '5',
    '5',
    '4',
    '4',
    '3',
    '3',
    '2',
    '2',
    '1',
    '1',
    ]
    
    num_answer = ' 0' # this is set to zero, so that it will raise an error if there is no good verbal rating
    
    end_i = response_to_be_transformed.find(",")
    if end_i == -1:
        end_i = response_to_be_transformed.find(".")
    # If there is no comma, let's check dots    
    if end_i == -1:
        ans_temp = response_to_be_transformed[1:] 
    # Otherwise lets just take the whole response
    else:
        ans_temp = response_to_be_transformed[1:end_i] 
    
    # is there correspondence with preset verbal answers
    bool_list = [ans_temp == item for item in likertanswers]
    # Find the value that is true
    for count, item in enumerate(bool_list):
        if item == True:
            num_answer = numerical_answers[count]
            num_answer = ' ' + str(num_answer)
    
    return num_answer

def shuffle_prompt(prompt, items, item_number, item_order):
    """
    Shuffles the previoisly queried items to avoid recency bias.

    Parameters
    ----------
    prompt : Str
        The initial prompt where the items are added.
    items : List
        A list of items to be shuffled.
    item_number : Int
        needed because the first two items can't be randomized.
    item_order : List
        The order in which items are queried. Needed for logging the item order. The function shuffles these to the same order as is used in the prompt.

    Returns
    -------
    prompt : TYPE
        The shuffled prompt.
    item_order : TYPE
        In what order the items are in the prompt.

    """
    item_order = copy.deepcopy(item_order)
    items_shuffled = []
    items_temp=copy.deepcopy(items)
    ## for the first two items, there can't be any randomization
    if item_number == 0: 
        prompt = prompt + items_temp[0] + "\"\n\nParticipant:"
    elif item_number == 1:
        prompt = prompt + items_temp[0] + items_temp[1] + "\"\n\nParticipant:"
    else:
        last_item = items_temp.pop(-1)       # Save and remove from the list the item to be queried
        last_item_for_item_order = item_order.pop(-1)       # Save and remove from the list the item to be queried
        order = random.sample(range(len(items_temp)), k=len(items_temp))   # random order
        items_shuffled = [items_temp[i] for i in order]
        item_order = [item_order[i] for i in order]
        #items_shuffled = random.sample(items_temp, len(items_temp)) 
        n_items = len(items_temp)
        for i in range(n_items):
            prompt = prompt + items_shuffled[i]
        # Finally add the final item for the next query
        prompt = prompt + last_item + "\"\n\nParticipant:"
        item_order.append(last_item_for_item_order)
    
    return prompt, item_order

def randomize_examples(verbalize, path='prompts/',example_filenames="example_" , n_examples=3, onlyverbal=False):
    """
    Randomizes the examples for the initial prompt. 

    Parameters
    ----------
    verbalize : bool
        If true, examples contain reasoning for the answer, e.g. "because I do not believe in conspiracies."
    path : TYPE, optional
        Filepath. The default is 'prompts/'.
    example_filenames : TYPE, optional
         How the files containing the examples are named. The default is "example_".
    n_examples : TYPE, optional
        How many examples are sampled. The default is 3.
    onlyverbal : bool, optional
        If True, examples where there are no numerical answers are used. The default is False.

    Returns
    -------
    examples_string : TYPE
        DESCRIPTION.

    """

    # Read all the examples in a directory
    examples_list = []
    for file in os.listdir(path):
        if file.startswith(example_filenames):
            examples_list.append(open(path + file, "r").read())
    # Remove verbalization
    if verbalize == False:
        if onlyverbal == False:
            for i, value in enumerate(examples_list):
                temp = examples_list[i]
                examples_list[i] = temp[0:temp.find("Participant:") + 14] + '.'   
        if onlyverbal == True:
            for i, value in enumerate(examples_list):
                temp = examples_list[i]
                findend = temp.find("Participant:")
                end_i = temp.find(",", findend)
                examples_list[i] = temp[0:end_i] + '.'
    # Randomize the order 
    examples_list = random.sample(examples_list, k=n_examples)
    # Add to a string that will be added to the prompt
    for i in range(n_examples): 
        if i == 0:
            examples_string = examples_list[i]
        else:
            examples_string = examples_string + "\n\n" + examples_list[i]
            
    return examples_string


def trim_response(response):
    """
    

    Returns
    -------
    None.

    """
    #trim response
    response = response[0:response.find("Researcher:")]  # stop the response if the model started to create another question
    response = response[:response.find("\n")]            # stop the response after a single paragraph
    
    return response

def log_answer(text, logfilename, item, engine, participant, replication_number, prompt_logging, response_logging, item_order):
    """
    

    Parameters
    ----------
    text : str
        The response to be logged.
    logfilename : str
       DESCRIPTION.
    item : str
       DESCRIPTION.
    engine : str
        DESCRIPTION.
    participant : int
        DESCRIPTION.
    replication_number : TYPE
        DESCRIPTION.
    prompt_logging : TYPE
        DESCRIPTION.
    response_logging : TYPE
        DESCRIPTION.
    item_order : TYPE
        DESCRIPTION.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    None.

    """

    logger=logging.getLogger(__name__)
    logger.handlers = []    # remove all handlers
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler(logfilename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    resp_temp = text
    try:
        # Raises error if not a number
        value = int(resp_temp[1])      # Here will be the answer
        # if not a value between 1-5
        if value != 1 and value != 2 and value != 3 and value != 4 and value != 5:
            raise ValueError('Answer not an integer between 1-5')
    except ValueError as err:
        logger.error((err, f'QUERY : P{participant}_{item}_{engine}_Rep{replication_number}', f'PROMPT_USED: {prompt_logging}', f'RESPONSE GENERATED: {response_logging}', f'ITEM ORDER: {item_order}'))
    except IndexError as err2:
        logger.error((err2, f'QUERY : P{participant}_{item}_{engine}_Rep{replication_number}', f'PROMPT_USED: {prompt_logging}', f'RESPONSE GENERATED: {response_logging}',  f'ITEM ORDER: {item_order}'))
    else:
        logger.info(('SUCCESS', f'QUERY : P{participant}_{item}_{engine}_Rep{replication_number}', f'PROMPT_USED: {prompt_logging}', f'RESPONSE GENERATED: {response_logging}', f'ITEM ORDER: {item_order}'))
    finally:
        pass
    
def log_game(text, logfilename, response_logging):
    """
    
    Parameters
    ----------
    text : TYPE
        DESCRIPTION.
    logfilename : TYPE
        DESCRIPTION.
    response_logging : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    logger=logging.getLogger(__name__)
    logger.handlers = []    # remove all handlers
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler(logfilename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    logger.info((f'PROMPT USED: {text}', f'RESPONSE GENERATED: {response_logging}'))

def find_ratings(text, skip = 5, n_items=1):
    """ Find the ratings.
    
    A function to locate the numerical GPT-3 interview answers. In this project, GPT-3
    always answers 13 spaces after the letter P in Participant. Example:
        
        Researcher: On a scale from 1 to 5, where 1 is "strongly disagree" and 5 is "strongly agree", please rate the statement "I feel exhausted
        Participant: 3, because I didn't sleep well last night.
    
    Args:
        Text (str): The interview
        Skip (int): How many times "participant" appears in the text before the answers start. Default 5.
        n_items (int): How many items were queried. Default 1. 
    
    Returns:
        Answers (list): numerical answers generated by GPT-3
    -------
    None.

    """
     # 
    prompt_temp = text
    temp = []
    answers = []
    
    for i in range(skip + n_items):
        if i == 0:    # first answer from the initial prompt
            temp_initial = prompt_temp.find('Participant:') 
        elif i == 1:  
            temp.append(prompt_temp.find('Participant:', temp_initial+1))
        else:
            temp.append(prompt_temp.find('Participant:', temp[i-2]+1))
        if i > skip - 1:
            value = int(prompt_temp[temp[i-1]+13])
            if value != 1 and value != 2 and value != 3 and value != 4 and value != 5:
                raise ValueError('Answer not an integer between 1-5') 
            else:
                answers.append(value)   # the last 6 are the answers by GPT-3, it is always 13 index after the P

    return answers

def find_ratings_verbal(text, skip = 5, n_items=1):
    """ Find the ratings.
    
    A function to locate the numerical GPT-3 interview answers. In this project, GPT-3
    always answers 13 spaces after the letter P in Participant. Example:
        
        Researcher: On a scale from 1 to 5, where 1 is "strongly disagree" and 5 is "strongly agree", please rate the statement "I feel exhausted
        Participant: 3, because I didn't sleep well last night.
    
    Args:
        Text (str): The interview
        Skip (int): How many times "participant" appears in the text before the answers start. Default 5.
        n_items (int): How many items were queried. Default 1. 
    
    Returns:
        Answers (list): numerical answers generated by GPT-3
    -------
    None.

    """
    prompt_temp = text
    temp = []
    answers = []
    for i in range(skip + n_items):
        if i == 0:    # first answer from the initial prompt
            temp_initial = prompt_temp.find('Participant:') 
        elif i == 1:  
            temp.append(prompt_temp.find('Participant:', temp_initial+1))
        else:
            temp.append(prompt_temp.find('Participant:', temp[i-2]+1))
        if i > skip - 1:
            if int(prompt_temp[temp[i-1]+13]) == 1 or 2 or 3 or 4 or 5:
                answers.append(int(prompt_temp[temp[i-1]+13]))   # the last 6 are the answers by GPT-3, it is always 13 index after the P               
    return answers

def check_values(text, skip = 5, n_items=1):
    """ Find the ratings.
    
    A function to check the numerical GPT-3 interview answers. In this project, GPT-3
    always answers 13 spaces after the letter P in Participant. Example:
        
        Researcher: On a scale from 1 to 5, where 1 is "strongly disagree" and 5 is "strongly agree", please rate the statement "I feel exhausted
        Participant: 3, because I didn't sleep well last night.
        
    This function checks that
        a) the answers have values of 1,2,3,4, or 5
        b) there charathers after the answer is not numeric or '.' (decimal place)
    
    Args:
        Text (str): The interview
        Skip (int): How many times "participant" appears in the text before the answers start. Default 5.
        n_items (int): How many items were queried. Default 1. 
    
    Returns:
        Error if there is a problem, otherwise "Interview checked, all is good"
    -------
    None.

    """
    prompt_temp = text
    temp = []
    answers = []
    answers2 = []
    answers3 = []
    for i in range(skip + n_items):
        if i == 0:    # first answer from the initial prompt
            temp_initial = prompt_temp.find('Participant:') 
        elif i == 1:  
            temp.append(prompt_temp.find('Participant:', temp_initial+1))
        else:
            temp.append(prompt_temp.find('Participant:', temp[i-2]+1))
        if i > skip - 1:
            answers.append(prompt_temp[temp[i-1]+13])  # the last 6 are the answers by GPT-3, it is always 13 index after the P
            answers2.append(prompt_temp[temp[i-1]+14])
            answers3.append(prompt_temp[temp[i-1]+15])    
    return answers, answers2, answers3

def check_results(text, skip = 5, n_items=1):
    """ Find the ratings.
    
    A function to check the numerical GPT-3 interview answers. In this project, GPT-3
    always answers 13 spaces after the letter P in Participant. Example:
        
        Researcher: On a scale from 1 to 5, where 1 is "strongly disagree" and 5 is "strongly agree", please rate the statement "I feel exhausted
        Participant: 3, because I didn't sleep well last night.
        
    This function checks that
        a) the answers have values of 1,2,3,4, or 5
        b) there charathers after the answer is not numeric or '.' (decimal place)
    
    Args:
        Text (str): The interview
        Skip (int): How many times "participant" appears in the text before the answers start. Default 5.
        n_items (int): How many items were queried. Default 1. 
    
    Returns:
        Error if there is a problem, otherwise "Interview checked, all is good"
    -------
    None.

    """
    prompt_temp = text
    temp = []
    for i in range(skip + n_items):
        if i == 0:    # first answer from the initial prompt
            temp_initial = prompt_temp.find('Participant:') 
        elif i == 1:  
            temp.append(prompt_temp.find('Participant:', temp_initial+1))
        else:
            temp.append(prompt_temp.find('Participant:', temp[i-2]+1))
        if i > skip - 1:
            temp2 = prompt_temp[temp[i-1]+13]
            temp3 = prompt_temp[temp[i-1]+14]
            if temp2 == '1' or temp2 == '2' or temp2 == '3' or temp2 == '4' or temp2 == '5':
                pass
            else:
                print('CHECK values (not 1-5) in item', str(i-skip+1))
            if temp3.isnumeric() == True or temp3 == '.':
                print('CHECK decimal places item', str(i-skip+1)) 
    return 

def score_panas(datapath):
    """ Scores the PANAS questionnaire.
    
    Scores can range from 10 – 50 in both scales, with higher scores representing higher levels of 
    positive or negative affect.

    
    Input: 
        Datapath (str): to a .csv -file containing answers to PANAS questionnaire. 
        Csv file needs to have items as column names and data in rows

    Returns:
        affect_balance (int): positive scale - negative scale
        answers_positive (print): sum of values in positive scale items (numpy.int64)
        answers_negative (print): sum of values negative scale items (numpy.int64)
        
    -------
    None.

    """
    data = pd.read_csv(datapath)
    answers_positive = data["interested"] + data["excited"] + data["strong"] + data["alert"] + data["enthusiastic"] + data["proud"] + data["inspired"] + data["determined"] + data["attentive"] + data["active"] 
    answers_negative = data["distressed"] + data["upset"] + data["guilty"] + data["scared"] + data["hostile"] + data["irritable"] + data["ashamed"] + data["nervous"] + data["jittery"] + data["afraid"] 
    answers_positive = answers_positive.iloc[0]
    answers_negative = answers_negative.iloc[0]
    affect_balance = answers_positive - answers_negative
    return affect_balance, answers_positive, answers_negative


def check_events(n_events):
    events = []  
    unsatisfying_events = []  
    n_events = n_events             
    for i in range(n_events):
        temp = open(f'prompts/Events/event_{i}.txt').read()
        temp2 = open(f'prompts/Events/unsatisfying_event_{i}.txt').read()
        events.append(temp)
        unsatisfying_events.append(temp2)
    return events, unsatisfying_events



#######################
# QUESTIONNAIRE ITEMS #
#######################

likertanswers=[
    """
    Acceptable answers for the verbal only version
    """
    ' Strongly agree.',
    ' Strongly agree',
    ' strongly agree.',
    ' strongly agree',
    ' Agree.',
    ' Agree',
    ' agree.',
    ' agree',
    'Neither agree nor disagree.',
    'Neither agree nor disagree',
    'neither agree nor disagree.',
    'neither agree nor disagree',
    ' Disagree.',
    ' Disgree',
    ' disagree.',
    ' disagree',
    ' Strongly disagree.',
    ' Strongly disagree',
    ' strongly disagree.',
    ' strongly disagree'
    ]


sheldon_items=[
    #autonomy
    "that my choices were based on my true interests and values.",
    "free to do things my own way.",
    "that my choices expressed my \"true self.\"",
    #competence
    "that I was successfully completing difficult tasks and projects.",
    "that I was taking on and mastering hard challenges.",
    "very capable in what I did.",
    #relatedness
    "a sense of contact with people who care for me, and whom I care for.",
    "close and connected with other people who are important to me.",
    "a strong sense of intimacy with the people I spent time with.",
    #self-actualization-meaning,
    "that I was \"becoming who I really am.\"",
    "a sense of deeper purpose in life.",
    "a deeper understanding of myself and my place in the universe.",
    #physical thriving,
    "that I got enough exercise and was in excellent physical condition.",
    "that my body was getting just what it needed.",
    "a strong sense of physical well-being.",
    #pleasure-stimulation,
    "that I was experiencing new sensations and activities.",
    "intense physical pleasure and enjoyment.",
    "that I had found new sources and types of stimulation for myself.",
    #money-luxury
    "able to buy most of the things I want.",
    "that I had nice things and possessions.",
    "that I got plenty of money.",
    #security
    "that my life was structured and predictable.",
    "glad that I have a comfortable set of routines and habits.",
    "safe from threats and uncertainties.",
    #self-esteem,
    "that I had many positive qualities.",
    "quite satisfied with who I am.",
    "a strong sense of self-respect",
    #popularity-influence
    "that I was a person whose advice others seek out and follow.",
    "that I strongly influenced others' beliefs and behavior.",
    "that I had strong impact on what other people did.",
    ]

panas_items=[
    "interested", 
    "distressed", 
    "excited", 
    "upset", 
    "strong", 
    "guilty", 
    "scared", 
    "hostile",
    "enthusiastic", 
    "proud", 
    "irritable", 
    "alert", 
    "ashamed",
    "inspired",
    "nervous",
    "determined",
    "attentive",
    "jittery", 
    "active",
    "afraid"
]

def get_UMI_items(technology):
    UMI_items=[f"I use {technology}, but I question why I continue to use it",
    f"I use {technology}, but I wonder what is the point in using it",	
    f"I use {technology}, but I don't see why I should keep on bothering with it",	
    f"Other people will be upset if I don't use {technology}",	
    f"I use {technology} because others will not be pleased with me if I don't",	
    f"I feel under pressure from others to use {technology}",	
    f"I would feel bad about myself if I quit {technology}",	
    f"I would feel guilty if I quit using {technology}",	
    f"I would feel like a failure if I quit using {technology}",	
    f"Using {technology} is a sensible thing to do",	
    f"The benefits of using {technology} are important to me",	
    f"Using {technology} is a good way to achieve what I need right now",	
    f"I use {technology} because it reflects the essence of who I am",	
    f"Using {technology} is consistent with my deepest principles",	
    f"I use {technology} because it expresses my values",	
    f"I use {technology} because it is enjoyable",	
    f"I think using {technology} is an interesting activity",	
    f"Using {technology} is fun",	
    ]
    return UMI_items