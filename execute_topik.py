#!/usr/bin/env python

import mysql.connector
import os
import pandas as pd

from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  passwd=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_DATABASE')
)

df= pd.read_sql_query("select saran as sentence, topik as label from saran where topik is not null", mydb)

sentences = df['sentence'].values
y = df['label'].values

print(df['sentence'].values)
sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, y, test_size=0.2, random_state=1000)

vectorizer = CountVectorizer()
vectorizer.fit(sentences_train)
X_train = vectorizer.transform(sentences_train)
X_test  = vectorizer.transform(sentences_test)

classifier = LogisticRegression()
classifier.fit(X_train, y_train)
print("\n \n hasil \n -----------------------\n")


df= pd.read_sql_query("select id, saran as sentence, topik as label from saran where topik is null order by id", mydb)

cur = mydb.cursor()
df['topik']=(classifier.predict(vectorizer.transform(df['sentence'])))
idnum=df['id'].values.item(0)
print(df['id'].values)
topik='5'
sql = f"UPDATE saran SET topik='{topik}' WHERE id='{idnum}'"
stuff = [topik, idnum]
cur.execute(sql)
mydb.commit()