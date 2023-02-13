
import pandas as pd

def get_train_data(path):
	df = pd.read_csv(path)
	return df

def get_twitter_data(path):
	df = pd.read_csv(path)
	return df
