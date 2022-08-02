# gpt-panas
This is the repository containing the data and code for the project "Language Models Can Generate Human-Like Self-Reports of Emotion". The work was published in the IUI'22 (27th International Conference on Intelligent User Interfaces) companion's work in progress -section. Read more here: https://dl.acm.org/doi/abs/10.1145/3490100.3516464

If you want to reproduce the results, you need to first download the human data according to the instructions in the HumanData -folder and run Format_Human_Data.py.

- Results/PANAS_bl -folder contains the GPT-3 data.
- R/EFA.R can be used to reproduce the factor analysis results.
- heatmaps.py can be used to reproduce Fig 1. a)
- HumanComparisons.py can be used to reproduce Fig 3.

If you want to replicate the data generation process, you will need your own OpenAI API -key. In this case, save your key as text file (key.txt) in this folder.

If you use the work, please cite:

@inproceedings{10.1145/3490100.3516464,
author = {Tavast, Mikke and Kunnari, Anton and H\"{a}m\"{a}l\"{a}inen, Perttu},
title = {Language Models Can Generate Human-Like Self-Reports of Emotion},
year = {2022},
isbn = {9781450391450},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3490100.3516464},
doi = {10.1145/3490100.3516464},
abstract = {Computational interaction and user modeling is presently limited in the domain of emotions. We investigate a potential new approach to computational modeling of emotional response behavior, by using modern neural language models to generate synthetic self-report data, and evaluating the human-likeness of the results. More specifically, we generate responses to the PANAS questionnaire with four different variants of the recent GPT-3 model. Based on both data visualizations and multiple quantitative metrics, the human-likeness of the responses increases with model size, with the largest Davinci model variant generating the most human-like data.},
booktitle = {27th International Conference on Intelligent User Interfaces},
pages = {69–72},
numpages = {4},
keywords = {affect, emotion, GPT-3, Language models, PANAS},
location = {Helsinki, Finland},
series = {IUI '22 Companion}
}


