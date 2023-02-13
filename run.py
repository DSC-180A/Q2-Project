
import sys
import os
import json

#Import functions from src
from src.etl import get_train_data, get_twitter_data
from src.features import data_wrangling, transform_train_data
from src.nb_model import naive_bayes_model, sentiment_analyzer

def main(targets):

	if "test" in targets:
		# run producer.py and consumer.py, both in backround

		os.system("python src/producer_offline.py &")
		os.system("python src/consumer_base.py &")
		os.system("python src/consumer_bert.py &")


	if "features" in targets:
		with open("config/features-params.json") as fh:
			feats_cfg = json.load(fh)
			viz_df = data_wrangling(train_data, feats_cfg["label_col_name"], feats_cfg["columns_standardize"], feats_cfg["tweet_col_name"])
			NB_df = transform_train_data(train_data, feats_cfg["tweet_col_name"], feats_cfg["label_col_name"])

	if "model" in targets:
		with open("config/naive-bayes-params.json") as fh:
			NB_cfg = json.load(fh)
			NB_model = naive_bayes_model(NB_df, NB_cfg["tweet_column_name"], NB_cfg["label_column_name"], NB_cfg["vectorizer_fp"], NB_cfg["mdl_fp"])


	return

if __name__ == "__main__":
	targets = sys.argv[1:]
	main(targets)