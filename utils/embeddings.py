import numpy as np
import io

# Load fasttext vectors into embedding matrix
def load_fasttext_vectors(fname, tokenizer):
  vocab_size = len(tokenizer.word_index) + 1
  print('Loading FastText Model and building embedding matrix with vocabulary...')
  embedding_matrix = np.zeros((vocab_size, 300))
  vocabulary = dict(tokenizer.word_index.items())
  keys = vocabulary.keys()
  fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
        
  for line in fin:
      tokens = line.rstrip().split(' ')
      if tokens[0] in keys:
        embedding_matrix[vocabulary[tokens[0]]] = tokens[1:]
  print('DONE')
  return embedding_matrix

# Load glove vectors into embedding matrix
def load_glove_vectors(fname, tokenizer):
  vocab_size = len(tokenizer.word_index) + 1
  print('Loading Glove Model...')
  f = open(fname,'r')
  glove_model = {}
  for line in f:
      splitLines = line.split()
      word = splitLines[0]
      wordEmbedding = np.array([float(value) for value in splitLines[1:]])
      glove_model[word] = wordEmbedding
  print(len(glove_model), ' words loaded!')

  print('Building embedding matrix with vocabulary...')
  embedding_matrix = np.zeros((vocab_size, 200))
  i = 0
  for word, index in tokenizer.word_index.items():
    if word in glove_model:
      i = i + 1
      embedding_matrix[index] = glove_model[word]
  print('DONE')
  del glove_model
  return embedding_matrix