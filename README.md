## Detect Checkworthy Claims


## How to run?
- `python iddiaVarMiIddia.py <inputs.csv path>` or `python iddiaVarMiIddia.py -h` for help.
- <input.csv> should contain columns [tweet, obj_subj, has_claim].
- 0 -> Obj 1 -> Obj, 0 -> Tweet has no claim, 1 -> Tweet has claim.
- Output format: 1 -> Tweet has checkworthy claim.
- NOTE: CNN Model only uses tweets, LSTM Model also uses has_claim and objective/subjectiveness as features.

- Set data paths inside notebooks.
- Follow cells in the notebook for the relevant model.


## Required Packages:
- Keras
- Flair
- Spacy
- Nltk
- Scipy
- Sklearn
- Pandas_ml

