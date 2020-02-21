import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="saran"
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
print()
print(sql)

for a in df['topik'].values.item
  print(a)