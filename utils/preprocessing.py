import nltk
import pandas as pd
import numpy as np
import string
import pickle
import re
import unicodedata
from nltk import word_tokenize
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from contracted_forms import contractions
from emoticons import emoticons_replaces
from patterns import regex_patterns

nltk.download('stopwords')
nltk.download('punkt')

class Preprocessor():

  def __init__(self, lower=True, remove_chars_repetitions=True, 
               replace_contractions=True, remove_stopwords=True, replace_emojis=True,
               correct_bad_words=True, keep_punct='', path_to_tokenizer = None, 
               num_words=20000, max_len=150):
    self.lower = lower
    self.remove_chars_repetitions = remove_chars_repetitions
    self.replace_contractions = replace_contractions
    self.remove_stopwords = remove_stopwords
    self.replace_emojis = replace_emojis,
    self.correct_bad_words = correct_bad_words,
    self.keep_punct = keep_punct
    self.path_to_tokenizer = path_to_tokenizer
    self.num_words = num_words
    self.max_len = max_len

    if self.path_to_tokenizer is not None:
      # load tokenizer if provided
      self.tokenizer = self.__loadTokenizer()
    else:
      # instantiate new tokenizer
      self.filters = self.__initTokenizerFilters()
      self.tokenizer = Tokenizer(num_words=num_words, filters=self.filters)

  #############  UTILS  ############# 
  # return length of the longest document
  def maxDoclength(self, docs):
    return max([len(doc.split()) for doc in docs])

  # return max_len for which the tokenizer is instantiated
  def getMaxLen(self):
    return self.max_len

  # return vocabulary size
  def getVocabularySize(self):
    return len(self.tokenizer.word_index) + 1
  
  # tokenize a document
  def tokenize(self, doc):
    return word_tokenize(doc)

  #############  PREPROCESS  ############# 
  # preprocess a document
  def preprocessDoc(self, doc):
    if self.lower:
      doc = doc.lower()
    # convert to ascii and remove extra white spaces
    doc = self.__unicodeToAscii(doc.strip())
    # remove links
    doc = re.sub(r'https?://\S+|www\.\S+', ' ', doc)
    # replace contractions
    if self.replace_contractions:
      doc = self.__replaceContractions(doc)
    # replace emojis
    if self.replace_emojis:
      doc = self.__replaceEmojis(doc)
    # replace time related words
    doc = doc.replace('utc', ' ')
    # remove repeated characters if > 2
    doc = self.__removeRepetitions(doc)
    # correct bad words
    if self.correct_bad_words:
      doc = self.__correctWords(doc)
    # remove extra white spaces
    doc = re.sub(r'[" "]+', " ", doc)
    # remove everything but letters
    doc = re.sub(r"[^a-zA-Z"+ self.keep_punct + "]+", " ", doc)
    # remove stopwords
    if self.remove_stopwords:
      doc = self.__removeStopwords(doc)
    # remove mentions starting with @
    doc = re.sub(r'@\w+', '', doc)
    # remove extra white spaces
    doc = re.sub(r'[" "]+', " ", doc)
    return doc

  # transform doc from unicode to ascii
  def __unicodeToAscii(self, doc):
    return ''.join(c for c in unicodedata.normalize('NFD', doc) if unicodedata.category(c) != 'Mn')

  # remove stopwords
  def __removeStopwords(self, doc):
    stopwords_list=stopwords.words('english')
    tokens = word_tokenize(doc)
    clean_tokens = [token for token in tokens if (token not in stopwords_list) and (len(token) > 2 or (token in self.keep_punct))]
    return " ".join(clean_tokens) 

  # replace contractions
  def __replaceContractions(self, doc):
    tokens = doc.split()
    clean_tokens = [contractions[token] if token in contractions else token for token in tokens]
    return " ".join(clean_tokens)
  
  # replace emojis
  def __replaceEmojis(self, doc):
    tokens = doc.split()
    clean_tokens = [emoticons_replaces[token] if token in emoticons_replaces else token for token in tokens]
    return " ".join(clean_tokens)
  

  # remove repetitions (helloooo => hello)
  def __removeRepetitions(self, doc):
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    doc = pattern.sub(r"\1", doc)
    return doc

  def __correctWords(self, doc):
    for word, patterns in regex_patterns.items():
      for pattern in patterns:
        doc = re.sub(pattern, word, doc)
    return doc

  #############  TOKENIZER AND SEQUENCES  ############# 
  def __loadTokenizer(self):
    with open(self.path_to_tokenizer, 'rb') as handle:
      tokenizer = pickle.load(handle)
    return tokenizer
  
  # initialize tokenizer filters
  def __initTokenizerFilters(self):
    base_filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    for punct in self.keep_punct: 
      base_filters = base_filters.replace(punct, '')
    return base_filters
  
  # get tokenizer
  def getTokenizer(self):
    return self.tokenizer
  
  # save tokenizer
  def saveTokenizer(self, path):
    with open(path, 'wb') as handle:
      pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
  
  # fit tokenizer on given docs
  def fitTokenizer(self, docs):
    self.tokenizer.fit_on_texts(docs)
  
  # transform docs to sequences and add padding if needed
  def toSequences(self, docs):
    sequences = self.tokenizer.texts_to_sequences(docs)
    sequences = pad_sequences(sequences, padding='post', maxlen=self.max_len)
    return sequences