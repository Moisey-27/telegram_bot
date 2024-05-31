import pandas as pd
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

df = pd.read_csv('C:/Users/79185/Desktop/test_task/datasets/csv_all_in_one/all.csv')
df.columns = ['category', 'article_name', 'article_link', 'article_text']
df.sample(frac=1.0)

#nltk.download('stopwords')
stopWords = set(stopwords.words('russian'))


def clean_text(text):
    text = text.replace("\\", " ").replace(u"╚", " ").replace(u"╩", " ")
    text = text.lower()
    # удаление новых строк и переносов строк
    text = re.sub(r'\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', text)
    text = re.sub(r'[.\"«»,:;_%©?*,!@#$%^&()\d]|[+=]|[|[]]|/|\s{2,}|-', ' ', text)
    text = ' '.join(word for word in text.split() if len(word) > 3)
    # Стемминг + удаление стоп слов
    stemmer = SnowballStemmer("russian")
    text = ' '.join([stemmer.stem(word) for word in text.split() if word not in stopWords])

    return text


df['article_text'] = df['article_text'].apply(clean_text)

df.to_csv('C:/Users/79185/Desktop/test_task/datasets/csv_all_in_one/all_stemmer.csv', index=False)

print(df['article_text'][15])
