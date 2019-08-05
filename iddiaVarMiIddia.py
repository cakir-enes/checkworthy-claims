from keras.models import load_model
import pandas as pd
import pickle
import numpy  as np
from keras.preprocessing.sequence import pad_sequences
import sys

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

    predictions = pd.DataFrame(columns=['CNN', 'LSTM'])
    predictions['CNN'] = [1 if pred > 0.5 else 0 for pred in cnn_predicted]
    predictions['LSTM'] = [1 if pred > 0.5 else 0 for pred in lstm_predicted]

    predictions.to_csv('predictions.csv')
    print('\nSee predictions.csv for predictions.')
