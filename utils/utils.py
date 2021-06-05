from sklearn.model_selection import train_test_split


def getComments(X, clean):
  if clean:
    return X[(X['toxic'] == 0) & (X['severe_toxic'] == 0) & (X['obscene'] == 0)
                & (X['threat'] == 0) & (X['insult'] == 0) & (X['identity_hate'] == 0)]
  else:
    return X[(X['toxic'] == 1) | (X['severe_toxic'] == 1) | (X['obscene'] == 1)
                | (X['threat'] == 1) | (X['insult'] == 1) | (X['identity_hate'] == 1)]
                
# NOTE: pass sources=[] to keep only original data
def train_val_split(X, targets, val_size=0.2, random_state=42, sources=['de', 'fr', 'es']):
  # take only the original data
  train_en = X[X['source']=='en']
  # split comments from labels
  X_train = train_en['comment_text']
  y_train = train_en[targets]
  # split original data into training set and validation set
  X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=val_size, random_state=random_state)
  ### prepare for augmentation ###
  # get comments on which has been performed the augmentation
  train_en_nc = getComments(y_train, clean=False)
  val_en_nc = getComments(y_val, clean=False)
  # reset indexes to allow the alignment with the other sources
  train_en_nc.reset_index(drop=True, inplace=True)
  val_en_nc.reset_index(drop=True, inplace=True)
  # extract indexes of the original data
  indexes_train = train_en_nc.index
  indexes_val = val_en_nc.index
  # iterate over augmented data
  for source in sources:
    print('Augmenting with {0} ...'.format(source))
    # take only the augmented data from a specific source
    train_source = X[X['source']==source]
    # reset index to allow allignment with original data
    train_source.reset_index(drop=True, inplace=True)
    # each augmented data must belong to the same set of the original data to avoid overfitting
    X_train = X_train.append(train_source.loc[indexes_train]['comment_text'], ignore_index=True)
    y_train = y_train.append(train_source.loc[indexes_train][targets], ignore_index=True)
    X_val = X_val.append(train_source.loc[indexes_val]['comment_text'], ignore_index=True)
    y_val = y_val.append(train_source.loc[indexes_val][targets], ignore_index=True)
  return X_train, X_val, y_train, y_val