text-canary
===========

A simple web API service that helps people handle text.

# Use Case

+ twitter pos tagging

+ spellchecking

+ tokenization

+ POS tagging

+ emotion analysis

+ positive, neg cue distribution

# Features

+ 6 NLP APIs 

+ Simple web interface

+ Allow large file upload 

+ Large-scale NLP computation

+ Distribution/threading*

*So far, job disstribution has not yet been tested on multiple machines due to the limited access and system privilege constraints on Penn's biglab grid. However, the distribution library (scoop) is a pretty widely adopted package for scientific computing so theoretically the model should scale.

# Software Components

+ server.py - The server that handles all API requests and combines all component together.

+ nlp.py - The natural language processing library package. It includes functions such as part-of-speech (POS) tagging, twitter-specific POS tagging, spell checking, lemmatization/stemming, preprocessing (POS tagging + spell checking + lemmatization/stemming), emotion analysis, polarity distribution, and pointwise mutual information (PMI). 

+ dictionary_reader.py - The class that combines multiple sentiment lexicons including Bing Liu's Opinion Lexicon, WordNetAffect, Emoticon Dictionary, and MPQA. See the "Other Dependencies" section for more details about each lexical resource. One of the advantages of this library is that it fuses multiple dictionaries while providing a tag set conversion table enabling easy integration

+ spell_checker.py - The spell checker corrects mispelled words. It takes big.txt as input to initialize.

+ analyzer.py - The module uses dictionaries to perform emotion analysis, polarity distribution computation, and pmi approximation.

+ *_scale.py - These scripts use the scoop library to achieve concurrency. Essentially, the underlying method is similar to the single instance case. The only difference is parallelism. 

+ tests.py - Test script to automate module testing

# Functionalities and Use Cases

+ Part-of-Speech Tagging - Part-of-speech tagging is a fundamental NLP paradigm for extracting syntactic information. In addition to offering a general tagger, the system provides a twitter-specific POS tagger (trained with real tweets), which achieves higher accuracy and  offers a richer tag set. The API is useful for developers who are interesting in incorporating POS information will benefit from the API.

+ Spell Checking - The API offers a simple way to correct spelling.

+ Emotion analysis -  Psychologists divide human private states into five basic emotions: joy, fear, disgust, anger, and surprise. This API analyzes input text and calculates the emotional word distribution for the text

+ Polarity distribution - The API scans over the input text and calculates the positive/negative token distribution. 

+ Pointwise mutual information - The API uses concepts rom information retrieval to approximate, on average, how related each token is assoicated with emotional words. If this value is positive, the text has an overall positive sentiment. If the value is negative, the text is likely to convey negative valence. Otherwise, the text is neutral. The API approximates the score and leaves the interpretation (such as cut-off, threshold values to the user).

# Python Dependencies

+ spell_checker - http://norvig.com/spell-correct.html

+ scoop - used to achieve concurrency

+ flask - used to develop a very simple frontend and API

+ numpy - used for more efficient numerical computation when approximating PMI

# Other Dependencies
The project makes use of many lexical resources and citations are given below:

+ Minqing Hu and Bing Liu. Mining and summarizing customer reviews. Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD-2004, full paper), Seattle, Wash- ington, USA, Aug 22-25, 2004

+ Janyce Wiebe, Theresa Wilson , and Claire Cardie, Annotating expressions of opinions and emotions in language, Language Resources and Evaluation, volume 39, issue 2-3, pp. 165-210, 2005

+ Carlo Strapparava and Alessandro Valitutti. WordNet-Affect: an affective extension ofWordNet. In Pro- ceedings ofthe 4th International Conference on Language Resources and Evaluation (LREC 2004), Lisbon, May 2004, pp. 1083-1086.

The project also makes use of the Twitter POS tagger from CMU:

Improved Part-of-Speech Tagging for Online Conversational Text with Word Clusters 
Olutobi Owoputi, Brendan O’Connor, Chris Dyer, Kevin Gimpel, Nathan Schneider and Noah A. Smith. 
In Proceedings of NAACL 2013.

# Miscellaneous

+ To run the Twitter POS tagger, I did it by running a subprocess. Although this is not ideal, that's the interface the jar file seems to provide. Jython is slow and I don't want to use Jython just to integrate one feature.

+ Due to the way it is designed, scoop is most naturally invoked as a script (run when __name__=='__main__'). Additionally, invoking scoop requires a "-m" tag. Therefore, the system spawns a new process (a broker) that handles workers. 

