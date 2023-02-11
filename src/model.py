
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import re
import joblib

from features.py import preprocess, transform_train_data

def naive_bayes_model(train_df, tweet_column_name, label_column_name):
	df = train_df.copy()
	#Load from json
	tweet_name = tweet_column_name
	label_name =  label_column_name
	model_df = trainsform_train_data(df, tweet_name, label_name)

	vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1)).fit(X_train)
	x_train_vectorized = vectorizer.transform(X_train)

	model = MultinomialNB(alpha=0.1) #Multinominal looks at the occurence count
	model.fit(x_train_vectorized, Y_train)

	#Load from json
	filename_vectorizer = "vectorizer.sav"
	filename_NB = "final_naivebayes.sav"

	joblib.dump(vectorizer, filename_vectorizer)
	joblib.dump(model, filename_NB)

	return

