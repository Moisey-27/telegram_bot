import pandas as pd
import time
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os


basedir = os.path.abspath(os.getcwd())
workbooks_dir = os.path.abspath(os.path.join(basedir, '../../datasets/csv_all_in_one/all_stemmer.csv'))
df = pd.read_csv(workbooks_dir).sample(frac=1)

df.columns = ['category', 'article_name', 'article_link', 'article_text']
print(df.head())

X_train, X_test, y_train, y_test = train_test_split(df['article_text'], df['category'], test_size=.15, random_state=42)


vectorizer = CountVectorizer()

X_train_BOW = vectorizer.fit_transform(X_train)
X_test_BOW = vectorizer.transform(X_test)

print(X_train_BOW.shape, X_test_BOW.shape)
print(X_train.iloc[200])

# Векторное представление
print(type(X_train_BOW[200]))
print(X_train_BOW[200])


start = time.time()

clf = LogisticRegression(random_state=0, max_iter=1000).fit(X_train_BOW, y_train)

end = time.time() - start
print(f'Время обучения: {end}')

# вычисляем предсказания
y_predict_BOW = clf.predict(X_test_BOW)

# вычисляем метрику accuracy
print(accuracy_score(y_predict_BOW, y_test))