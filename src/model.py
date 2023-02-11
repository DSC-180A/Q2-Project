
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import re
import joblib


def naive_bayes_model(train_df, tweet_column_name, label_column_name, vectorizer_fp, mdl_fp):

	model_df = train_df.copy()

	X_train, X_test, Y_train, Y_test = train_test_split(model_df[tweet_column_name], 
                                                    model_df[label_column_name], 
                                                    random_state=1)

	vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1)).fit(X_train)
	x_train_vectorized = vectorizer.transform(X_train)

	model = MultinomialNB(alpha=0.1) #Multinominal looks at the occurence count
	model.fit(x_train_vectorized, Y_train)

	joblib.dump(vectorizer, vectorizer_fp)
	joblib.dump(model, mdl_fp)

	return

