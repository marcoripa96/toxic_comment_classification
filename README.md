# Multilabel Toxic Comment Classification

A toxic comment classification using BERT, RNNs, CNNs using data from https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge.

## Methodology
Two types of classification pipelines are built:

* Binary classification to classify toxic and non-toxic comments. Toxic comments are then labeled with their respective toxicity types. This is done because of a very imbalanced datasets.
* Multilabel classification

## Implemented Models

* Multichannel CNN with Fasttext embeddings
* BERT as a feature extractor followed by a Bi-LSTM for the classification
* Bi-LSTM with Fasttext embeddings
* Bi-GRU with Fasttext embeddings

## Data and Models
* All data used is available here: https://drive.google.com/drive/folders/1j9E8fUVUknDXnb3TwgvHC7sInN5U1Y-8?usp=sharing
* All trained models are available here: https://drive.google.com/drive/folders/1C48UKNX4iOEoMgKkKZyLRQ60rKPzrjg_?usp=sharing
