
import sys
import os
import json

#Import functions from src
from src.etl import get_data
from src.features import data_wrangling, transform_train_data
from src.nb_sentiment_model import naive_bayes_model, sentiment_analyzer

def main(targets):

	if "test" in targets:
		#Build NB model
		with open("config/etl.json") as fh:
			data_cfg = json.load(fh)
			train_data = get_data(data_cfg["train_data"])
			twitter_data = get_data(data_cfg["twitter_data"])
		with open("config/features-params.json") as fh:
			feats_cfg = json.load(fh)
			NB_df = transform_train_data(train_data, feats_cfg["tweet_col_name"], feats_cfg["label_col_name"])
		with open("config/naive-bayes-params.json") as fh:
			NB_cfg = json.load(fh)
			NB_model = naive_bayes_model(NB_df, NB_cfg["tweet_column_name"], NB_cfg["label_column_name"], NB_cfg["vectorizer_fp"], NB_cfg["mdl_fp"])
		# run producer.py and consumer.py, both in backround

		os.system("python src/producer_offline.py &")
		os.system("python src/consumer_base.py &")
		os.system("python src/consumer_bert.py &")
		os.system("python src/consumer_nb.py")


	return

if __name__ == "__main__":
	targets = sys.argv[1:]
	main(targets)