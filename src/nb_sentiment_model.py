import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import re
import joblib
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def naive_bayes_model(train_df, tweet_column_name, label_column_name, vectorizer_fp, mdl_fp):
    """_summary_: Builds the Multinomial Naive Bayes Model

        Args:
            train_df: The dataframe to train the model
            tweet_column_name: A string of the column name containing the tweets
            label_column_name: A string of the column name containg the labels
            vectorizer_fp: A string of the file path to save a built file of the vectorizer for the model
            mdl_fp: A string of the file path to save a built file of the naive bayes model

        Returns:
            A naive bayes model as well as 2 files containg a vectorizer and the naive bayes model
    """
	model_df = train_df.copy()

	X_train, X_test, Y_train, Y_test = train_test_split(model_df[tweet_column_name], 
                                                    model_df[label_column_name], 
                                                    random_state=1)

	vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1)).fit(X_train)
	x_train_vectorized = vectorizer.transform(X_train)

	model = MultinomialNB(alpha=0.5) #Multinominal looks at the occurence count
	model.fit(x_train_vectorized, Y_train)

	joblib.dump(vectorizer, vectorizer_fp)
	joblib.dump(model, mdl_fp)

	return model

def sentiment_analyzer(sentence):
        """_summary_: Analyze the sentiment of a sentence

        Args:
            sentence (str): sentence to analyze

        Returns:
            str: Positive, Negative, or Neutral
        """
        model = SentimentIntensityAnalyzer()
        polarity = model.polarity_scores(sentence)
        compound_score = polarity["compound"]

        if compound_score >= 0.05:
            return "Positive"
        elif compound_score < 0.05 and compound_score > -0.05:
            return "Neutral"
        else:
            return "Negative"

