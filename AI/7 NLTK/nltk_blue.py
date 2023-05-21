
# coding=utf-8
import matplotlib.pyplot as plt
import nltk, re, pprint
from nltk import word_tokenize
import random
"""
In Chapter 2, complete exercises 4, 5, 7, 9, 12, 17, 18, 23, and 27.
"""
# Question 4:
"""
☼ Read in the texts of the State of the Union addresses, using the state_union corpus reader. 
Count occurrences of men, women, and people in each document. What has happened to the usage of these words over time?
"""
# from nltk.corpus import state_union
# # dictionary of words
# # men
# word_pairs = []
# for fileid in state_union.fileids():
#     for word in state_union.words(fileid):
#         if word.lower() in ["men","women","people"]:
#             word_pairs.append((word.lower(),fileid[:4]))
# stcfd = nltk.ConditionalFreqDist(word_pairs)
# stcfd.plot()

"""
Investigate the holonym-meronym relations for some nouns. 
Remember that there are three kinds of holonym-meronym relation, 
so you need to use: member_meronyms(), part_meronyms(), 
substance_meronyms(), member_holonyms(), part_holonyms(), and substance_holonyms().
"""
"""
Notes:
Brown corpus:
- text is categorized by genre 

 	
>>> from nltk.corpus import brown
>>> brown.categories()
['adventure', 'belles_lettres', 'editorial', 'fiction', 'government', 'hobbies',
'humor', 'learned', 'lore', 'mystery', 'news', 'religion', 'reviews', 'romance',
'science_fiction']
>>> brown.words(categories='news')
['The', 'Fulton', 'County', 'Grand', 'Jury', 'said', ...]
>>> brown.words(fileids=['cg22'])
['Does', 'our', 'society', 'have', 'a', 'runaway', ',', ...]
>>> brown.sents(categories=['news', 'editorial', 'reviews'])
[['The', 'Fulton', 'County'...], ['The', 'jury', 'further'...], ...]


Example	Description
fileids()	                the files of the corpus
fileids([categories])	    the files of the corpus corresponding to these categories
categories()	            the categories of the corpus
categories([fileids])	    the categories of the corpus corresponding to these files
raw()	                    the raw content of the corpus
raw(fileids=[f1,f2,f3])	    the raw content of the specified files
raw(categories=[c1,c2])	    the raw content of the specified categories
words()	                    the words of the whole corpus
words(fileids=[f1,f2,f3])	the words of the specified fileids
words(categories=[c1,c2])	the words of the specified categories
sents()	                    the sentences of the whole corpus
sents(fileids=[f1,f2,f3])	the sentences of the specified fileids
sents(categories=[c1,c2])	the sentences of the specified categories
abspath(fileid)	            the location of the given file on disk
encoding(fileid)	        the encoding of the file (if known)
open(fileid)	             open a stream for reading the given corpus file
root	                    if the path to the root of locally installed corpus
readme()	                the contents of the README file of the corpus

- Conditional frequency distributions
 - Frequency distibutions - occurences of each item in a list
 - CFDs pair event with conditions,
 - Each pair in the form of (condition, event)

 - Also can creat bigram with pairs words

 - Lexical resource - collection of words and associate info
 - lexical entry - headword and add information
 - homonym - two distinct words with same spelling
 - Ex: saw(cutting instrument) vs saw(past tense of see)
 - Ex: last letter in names: 
     cfd = nltk.ConditionalFreqDist(
...           (fileid, name[-1])
...           for fileid in names.fileids()
...           for name in names.words(fileid))

- Pronoucing dictionary
- Comparitive wordlist
- Swadesh wordlists
 - .entries() method returns tuples with pair of specified lanuage
 - Shoebox and Toolbox
 - 5 WordNet
 synoyms - same meaning of words
 - wordlist can explore synonyms /synset
>>> from nltk.corpus import wordnet as wn
>>> wn.synsets('motorcar')
[Synset('car.n.01')]

>>> wn.synset('car.n.01').lemmas() [1]
[Lemma('car.n.01.car'), Lemma('car.n.01.auto'), Lemma('car.n.01.automobile'),
Lemma('car.n.01.machine'), Lemma('car.n.01.motorcar')]
>>> wn.lemma('car.n.01.automobile') [2]
Lemma('car.n.01.automobile')
>>> wn.lemma('car.n.01.automobile').synset() [3]
Synset('car.n.01')
>>> wn.lemma('car.n.01.automobile').name() [4]
'automobile'
lemma = synset + word
- hyponym - immdediate in wordset hyearchy

>>> motorcar = wn.synset('car.n.01')
>>> types_of_motorcar = motorcar.hyponyms()
>>> types_of_motorcar[0]
Synset('ambulance.n.01')
>>> sorted(lemma.name() for synset in types_of_motorcar for lemma in synset.lemmas())
['Model_T', 'S.U.V.', 'SUV', 'Stanley_Steamer', 'ambulance', 'beach_waggon',
'beach_wagon', 'bus', 'cab', 'compact', 'compact_car', 'convertible',
'coupe', 'cruiser', 'electric', 'electric_automobile', 'electric_car',
'estate_car', 'gas_guzzler', 'hack', 'hardtop', 'hatchback', 'heap',
'horseless_carriage', 'hot-rod', 'hot_rod', 'jalopy', 'jeep', 'landrover',
'limo', 'limousine', 'loaner', 'minicar', 'minivan', 'pace_car', 'patrol_car',
'phaeton', 'police_car', 'police_cruiser', 'prowl_car', 'race_car', 'racer',
'racing_car', 'roadster', 'runabout', 'saloon', 'secondhand_car', 'sedan',
'sport_car', 'sport_utility', 'sport_utility_vehicle', 'sports_car', 'squad_car',
'station_waggon', 'station_wagon', 'stock_car', 'subcompact', 'subcompact_car',
'taxi', 'taxicab', 'tourer', 'touring_car', 'two-seater', 'used-car', 'waggon',
'wagon']

>>> motorcar.hypernyms()
[Synset('motor_vehicle.n.01')]
>>> paths = motorcar.hypernym_paths()
>>> len(paths)
2
>>> [synset.name() for synset in paths[0]]
['entity.n.01', 'physical_entity.n.01', 'object.n.01', 'whole.n.02', 'artifact.n.01',
'instrumentality.n.03', 'container.n.01', 'wheeled_vehicle.n.01',
'self-propelled_vehicle.n.01', 'motor_vehicle.n.01', 'car.n.01']
>>> [synset.name() for synset in paths[1]]
['entity.n.01', 'physical_entity.n.01', 'object.n.01', 'whole.n.02', 'artifact.n.01',
'instrumentality.n.03', 'conveyance.n.03', 'vehicle.n.01', 'wheeled_vehicle.n.01',
'self-propelled_vehicle.n.01', 'motor_vehicle.n.01', 'car.n.01']
nltk.app.wordnet()
"""

# Questions 5:
# from nltk.corpus import wordnet as wn
# # investigating the synsets for the word liberty, democracy, justice
# words = ["liberty","cat","democracy"]
# for word in words:
#     print("Word: ",word)
#     for syn in wn.synsets(word):
#         print(syn)
#         print("part meronyms: ")
#         print([syn2.name() for syn2 in syn.part_meronyms()])
#         print("member meronyms: ")
#         print([syn2.name() for syn2 in syn.member_meronyms()])
#         print("substance meronyms: ")
#         print([syn2.name() for syn2 in syn.substance_meronyms()])

#         print("part holonyms: ")
#         print([syn2.name() for syn2 in syn.part_holonyms()])
#         print("member holonyms: ")
#         print([syn2.name() for syn2 in syn.member_holonyms()])
#         print("substance holonyms: ")
#         print([syn2.name() for syn2 in syn.substance_holonyms()])

# question 7
# look state of the union addresses
# from nltk.corpus import state_union
# for id in state_union.fileids():
#     print("file: ",id)
#     text = nltk.Text(state_union.words(id))
#     text.concordance("however")
# 9
# from nltk.corpus import gutenberg
# print(gutenberg.fileids())

# def lexical_diversity(fileid):
#     words = gutenberg.words(fileid)
#     distinct = set(words)
#     return len(distinct)/len(words)

# def sentence_length(fileid):
#     words = gutenberg.words(fileid)
#     sentences = gutenberg.sents(fileid)
#     return len(words)/len(sentences)

# print("Austen vs whitman")
# print("lexical diversity: ")
# print("austen-sense.txt", lexical_diversity("austen-sense.txt"))
# print("whitman - leaves.txt",lexical_diversity("whitman-leaves.txt"))

# print("sentence length: ")
# print("austen-sense.txt", sentence_length("austen-sense.txt"))
# print("whitman - leaves.txt",sentence_length("whitman-leaves.txt"))

# whitman = nltk.Text(gutenberg.words("whitman-leaves.txt"))
# austen = nltk.Text(gutenberg.words('austen-sense.txt'))
# # context of the word leaves

# whitman.concordance('leaves')
# austen.concordance('leaves')

# whitman.similar('leaves')
# austen.similar('leaves')
# 12:
# from nltk.corpus import cmudict
# entries = cmudict.entries()
# wordToPro = dict()
# for entrie,pron in entries:
#     if entrie not in wordToPro:
#         wordToPro[entrie] = [pron]
#     else:
#         wordToPro[entrie].append(pron)

# print("Distinct words: ", len(wordToPro))
# print("more than one pronounciation: ", len([e for e in wordToPro if len(wordToPro[e]) > 1]))
# 17
from nltk.corpus import gutenberg
from nltk.corpus import stopwords
# STOP = set(stopwords.words('english'))
# # print(STOP)
# def most_frequent(text):
#     dist = nltk.FreqDist([w.lower() for w in text if w.isalpha() and w not in STOP])
#     common = [tup[0] for tup in dist.most_common(50)]
#     print(common)

# most_frequent(gutenberg.words('austen-emma.txt'))

# 18
# bi = list(nltk.bigrams([word for word in gutenberg.words('austen-emma.txt') if word.isalpha() and word not in STOP]))
# dist = nltk.FreqDist(bi)
# print([tup[0] for tup in dist.most_common(50)])

# 23
# def ziph(text):
#     dist = nltk.FreqDist([word for word in text if word.isalpha()])
#     vals = dist.most_common()
#     print(vals)
#     plt.plot([i for i in range(len(vals))],[tup[1] for tup in vals])
#     plt.yscale('log')
#     plt.xscale('log')
#     plt.show()

# # ziph(gutenberg.words('austen-emma.txt'))
# import random
# randtext = ""
# for i in range(190000):
#     randtext += random.choice('abcdefg ')

# ziph(randtext.split())

# 27:
# from nltk.corpus import wordnet as wn
# def calc_average(pos):
#     totalsense = 0
#     wordCOunt = 0
#     all_synsets = wn.all_synsets(pos=pos)
#     for synset in all_synsets:
#         words = synset.lemma_names()
#         for w in words:
#             wordCOunt += 1
#             totalsense += len(wn.synsets(w))
#     return totalsense/wordCOunt
# print(calc_average(wn.ADV))
"""
Chapter 3
>>> from urllib import request
>>> url = "http://www.gutenberg.org/files/2554/2554-0.txt"
>>> response = request.urlopen(url)
>>> raw = response.read().decode('utf8')
>>> type(raw)
<class 'str'>
>>> len(raw)
1176893
>>> raw[:75]
'The Project Gutenberg EBook of Crime and Punishment, by Fyodor Dostoevsky\r\n'

Tokenize:
>>> tokens = word_tokenize(raw)
>>> type(tokens)
<class 'list'>
>>> len(tokens)
254354
>>> tokens[:10]
['The', 'Project', 'Gutenberg', 'EBook', 'of', 'Crime', 'and', 'Punishment', ',', 'by']

Trim unwanted text
>>> raw.find("PART I")
5338
>>> raw.rfind("End of Project Gutenberg's Crime")
1157743
>>> raw = raw[5338:1157743] [1]
>>> raw.find("PART I")
0
Dealing with HTML
>>> url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
>>> html = request.urlopen(url).read().decode('utf8')
>>> html[:60]
'<!doctype html public "-//W3C//DTD HTML 4.0 Transitional//EN'
>>> from bs4 import BeautifulSoup
>>> raw = BeautifulSoup(html, 'html.parser').get_text()
>>> tokens = word_tokenize(raw)
>>> tokens
['BBC', 'NEWS', '|', 'Health', '|', 'Blondes', "'to", 'die', 'out', ...]

"""
# 20
from urllib import request
# url = "https://darwinawards.com/darwin/darwin2021-01.html"
# html = request.urlopen(url).read().decode('utf8')
# from bs4 import BeautifulSoup
# raw = BeautifulSoup(html,'html.parser').get_text()
# token = word_tokenize(raw)
# # print(token)
# start = raw.find('Petty')
# end = raw.rfind('.')
# raw = raw[start:end]
# print("Darwin award text: ")
# print(raw)

# 22

url = "http://news.bbc.co.uk/"

def unknown(url):
    html = request.urlopen(url).read().decode('utf-8')
    keywords = {'script','type','div','span','class','li','return'}
    words = re.findall(r'\b[a-z]+\b',html,re.I)
    vocab = set(nltk.corpus.words.words())
    words = [w for w in words if w.lower() in vocab and w.lower() not in keywords]
    # print(words)
    text = []
    # stopwords = set('a,abbr,address,area,article,aside,audio,b,base,bdi,bdo,blockquote,body,br,button,canvas,caption,cite,code,col,colgroup,data,datalist,dd,del,details,dfn,dialog,div,dl,dt,em,embed,fieldset,figcaption,figure,footer,form,h1,h2,h3,h4,h5,h6,head,header,hgroup,hr,html,i,iframe,img,input,ins,kbd,label,legend,li,link,main,map,mark,menu,meta,meter,nav,noscript,object,ol,optgroup,option,output,p,param,picture,pre,progress,q,rp,rt,ruby,s,samp,script,section,select,slot,small,source,span,strong,style,sub,summary,sup,table,tbody,td,template,textarea,tfoot,th,thead,time,title,tr,track,u,ul,var,video,wbr'.split(","))
    i =0
    prev = False
    while i < len(words) - 1:
        regex = words[i]+r'\s' + words[i+1]
        if re.search(regex,html):
            text.append(words[i])
            text.append(words[i+1])
            prev = True
            i += 2
        else:
            if prev:
                text.append('\n')
            prev = False
            i += 1
    extracted = " ".join(text)
    print(extracted)
# unknown(url)
from nltk.corpus import movie_reviews
documents = []
for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        documents.append((list(movie_reviews.words(fileid)),category))
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
random.shuffle(documents)

word_features = list(all_words)[:2000]
def document_features(doc):
    document_words = set(doc)
    features = {}
    for word in word_features:
        features[word] = word in document_words
    return features
featuresets = [(document_features(d),c) for d,c in documents]
train_set,test_set = featuresets[100:],featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier,test_set))
classifier.show_most_informative_features(30)



    



    


