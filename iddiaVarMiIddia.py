from keras.models import load_model
import pandas as pd
import pickle
import numpy  as np
from keras.preprocessing.sequence import pad_sequences
import sys
from scipy import spatial
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentPoolEmbeddings, Sentence, CharacterEmbeddings
import torch
import re
import nltk

def norm_tweet(tweet):
    WPT = nltk.WordPunctTokenizer()
    stop_word_list  = nltk.corpus.stopwords.words('turkish')
    pattern = r"[{}]".format(",.;@#!") 
    tweet = re.sub(pattern, "", str(tweet))
    tweet = tweet.lower()
    tweet = tweet.strip()
    tokens = WPT.tokenize(tweet)
    filtered_tokens = [token for token in tokens if token not in stop_word_list]
    tweet = ' '.join(filtered_tokens)
    return tweet

def embed_tweet(tweetList):
    # initialize the word embeddings
    tr_embedding = WordEmbeddings('tr')
    char_embedding = CharacterEmbeddings()

    # initialize the document embeddings, mode = mean
    document_embeddings = DocumentPoolEmbeddings([tr_embedding,char_embedding])
        

    tweetTensors=[]
    for tweet in tweetList:
        #print(norm_tweet(tweet))
        sentence = Sentence(norm_tweet(tweet))
        document_embeddings.embed(sentence)
        tweetTensors.append(sentence.get_embedding().data)
    return tweetTensors

def predictAccorrdingToCosineSim(tweets):
    tweetTensors = embed_tweet(tweets)
    claimTensors = torch.load("claimTensors.pt")
    check_worthy_tweet=[]
    for tweeetIndex in range(len(tweetTensors)):
        found = False
        for claimIndex in range(len(claimTensors)):
            result = 1 - spatial.distance.cosine(tweetTensors[tweeetIndex],claimTensors[claimIndex])
            if result > 0.8:
                found = True
                break
        check_worthy_tweet.append(1 if found else 0)

    return check_worthy_tweet

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        print('Usage: {} <input.csv path>'.format(sys.argv[0]))
        print('<input.csv> should contain columns [tweet, obj_subj, has_claim]')
        print('0 -> Obj 1 -> Obj, 0 -> Tweet has no claim, 1 -> Tweet has claim')
        print('Output format: 1 -> Tweet has checkworthy claim')
        print('NOTE: CNN Model only uses tweets, LSTM Model also uses has_claim and objective/subjectiveness as features.')
        sys.exit(0)
        
    df = pd.read_csv(sys.argv[1])
    print('Loading LSTM Model...')
    LSTM_model = load_model('LSTMmodel.h5')
    print('Loaded LSTM Model.')
    print('Loading CNN Model...')
    CNN_model = load_model('CNNmodel.h5')
    print('Loaded CNN Model.')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    tweets = pad_sequences(tokenizer.texts_to_sequences(df['tweet']), padding='post', maxlen=300)
    other_features = np.array([df['obj_subj'], df['has_claim']]).T
    lstm_predicted = LSTM_model.predict([tweets, other_features])
    cnn_predicted = CNN_model.predict(tweets)
    teyit_predicted = predictAccorrdingToCosineSim(df['tweet'])

    predictions = pd.DataFrame(columns=['CNN', 'LSTM', 'CosSimWithTeyit'])
    predictions['CNN'] = [1 if pred > 0.5 else 0 for pred in cnn_predicted]
    predictions['LSTM'] = [1 if pred > 0.5 else 0 for pred in lstm_predicted]
    predictions['CosSimWithTeyit'] = [1 if pred > 0.8 else 0 for pred in teyit_predicted]

    predictions.to_csv('predictions.csv')
    print('\nSee predictions.csv for predictions.')






