# gpt-panas
This is the repository containing the data and code for the project "Language Models Can Generate Human-Like Self-Reports of Emotion". The work was published in the IUI'22 (27th International Conference on Intelligent User Interfaces) companion's work in progress -section. Read more here: https://dl.acm.org/doi/abs/10.1145/3490100.3516464

If you want to reproduce the results, you need to first download the human data according to the instructions in the HumanData -folder and run Format_Human_Data.py.

- Results/PANAS_bl -folder contains the GPT-3 data.
- R/EFA.R can be used to reproduce the factor analysis results.
- heatmaps.py can be used to reproduce Fig 1. a)
- HumanComparisons.py can be used to reproduce Fig 3.

If you want to replicate the data generation process, you will need your own OpenAI API -key. In this case, save your key as text file (key.txt) in this folder.
