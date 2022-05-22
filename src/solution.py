# Importing Libraries
import nltk, re, pprint
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pprint, time
import random
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk
!pip install wordcloud
from wordcloud import WordCloud
# Loading Dataset
artists = pd.read_csv("artists.txt")
events = pd.read_csv("events_title.txt", sep = "\t")
print(events)
events.columns = ["Title"]
events.describe()
events.count()
artists.head()
artists.columns = ["Artists"]
artists.describe()
artists.count()
artists.info
# Generating WordCloud
text1 = str(pd.read_csv("artists.txt"))
text2 = str(pd.read_csv("events_title.txt", sep = "\t"))
word_cloud1 = WordCloud(width = 1200, height = 800, collocations = False, background_color = 'white').generate(text1)
word_cloud2 = WordCloud(width = 1200, height = 800, collocations = False, background_color = 'white').generate(text2)
plt.imshow(word_cloud1, interpolation='bilinear')
plt.axis("off")
plt.show()
plt.imshow(word_cloud2, interpolation='bilinear')
plt.axis("off")
plt.show()
import spacy
from spacy import displacy
from spacy import tokenizer
# NLP Model
nlp = spacy.load('en_core_web_sm')
doc = nlp(str(events))
sentences = list(doc.sents)
# Using tokenization
for token in doc:
    print(token.text)
# print entities
ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
print(ents)
# Using displaycy function for entities
displacy.render(doc, style='ent', jupyter=True)
for ent in doc.ents:
    print(ent.text,ent.label_)
ner=nlp.get_pipe("ner")
nlp.pipe_names
doc=nlp(str(events))
for ent in doc.ents:
    print(ent.text,ent.label_)
# Getting pipeline component
ner=nlp.get_pipe("ner")
# Adding a training dataset
train_set = [
    ("Ben works in TicketSwap", {"entities": [(0, 3, "PERSON")]}),
    ("Michael was on leave yesterday", {"entities": [(0, 7, "PERSON")]}),
    ("The guy said his name was Joseph", {"entities": [(26, 32, "PERSON")]}),
    ("Pink is my favorite singer",{"entities": [(0, 4, "PERSON")]}),
    ("On 26.07.2020, Jonas Borthers Band performed", {"entities": [(15, 29, "PERSON")]}),
    ("Craig Charles at The Tivoli", {"entities": [(0, 13, "PERSON")]}),
    ("Jamey Johnson", {"entities": [(0, 13, "PERSON")]}),
    ("Tomorrowland Presents Dimitri Vegas & Like Mike", {"entities": [(22, 35, "PERSON"), (38, 47, "PERSON")]}),
    ("Red, Lacey Sturm, Righteous Vendetta at The Bourbon", {"entities": [(0, 3, "PERSON"), (5, 16, "PERSON"), (18, 36, "PERSON")]}),
    ("Nils Frahm", {"entities": [(0, 10, "PERSON")]}),
    ("Lastly, we waited for Shakira to arrive at concert", {"entities": [(22, 29, "PERSON")]}),
    ("Alex the Astronaut & Stella Donnelly - Adelaide, SA", {"entities": [(0, 18, "PERSON"), (21, 36, "PERSON")]})
]

# Adding labels to the `ner`

for _, annotations in train_set:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])
        
# Disable pipeline components that are not to be changed
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

import random
from spacy.util import minibatch, compounding
from spacy.training.example import Example
from pathlib import Path

# Training Model
with nlp.disable_pipes(*unaffected_pipes):
    # Training for 30 iterations
    for iteration in range(30):
        # shuufling examples  before every iteration
        random.shuffle(train_set)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(train_set, size=compounding(4.0, 32.0, 1.001))
        for text, annotations in batch:
            #texts, annotations = zip(*batch)
            doc = nlp.make_doc(str(texts))
            set1 = Example.from_dict(doc, annotations)
            nlp.update([set1], drop=0.5, losses=losses)
            print("Losses", losses)
 
# Custom Model - Adding new label to ner
ner.add_label("PERSON")

# Resuming training
optimizer = nlp.resume_training()
move_names = list(ner.move_names)

# List of pipes to be trained
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

# List of pipes to be remained unaffected in training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]


# Begin training by disabling other pipeline components
with nlp.disable_pipes(*other_pipes):
    sizes = compounding(1.0, 4.0, 1.001)
    # Training for 30 iterations
    for itn in range(30):
        # shuffle examples before training
        random.shuffle(train_set)
        # batch up the examples using spaCy's minibatch
        batches = minibatch(train_set, size=sizes)
        # dictionary to store losses
        losses = {}
        for text, annotations in batch:
            #texts, annotations = zip(*batch)
            doc = nlp.make_doc(str(events))
            set1 = Example.from_dict(doc, annotations)
            nlp.update([set1], drop=0.5, sgd=optimizer, losses=losses)
            print("Losses", losses)
        
test_text = "Superstar Saturdays feat. Sam Feldt"
doc = nlp(test_text)
print("Entity in '%s'" % test_text)
for ent in doc.ents:
    print(ent)
    
print(ent)
