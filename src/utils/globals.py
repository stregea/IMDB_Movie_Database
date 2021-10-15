import os

# Database path
DATABASE = os.path.abspath('../imdb.db')

# The log file containing the pertinent information about the program
LOG_FILE = os.path.abspath('../imdb.log')

# Path to the folder containing the zipped datasets.
DATASETS = os.path.abspath('../DataSets/')

# Path to the folder containing the zipped datasets.
COMBINED = os.path.abspath('../DataSets/Combined/')

# Path to the folder containing the data dictionary.
DATA_DICTIONARY = os.path.abspath('../DataDictionary/')

tconst = 0
ordering = 1
title = 2
region = 3
language = 4
types = 5
attributes = 6
isOriginalTitle = 7
averageRating = 8
numVotes = 9
titleType = 10
primaryTitle = 11 
originalTitle = 12
isAdult = 13
startYear = 14
endYear = 15
runtimeMinutes = 16
genres = 17
nconst = 18
primaryName = 19
birthYear = 20
deathYear = 21
primaryProfession = 22
