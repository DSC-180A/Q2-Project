
import pandas as pd
from scipy import stats

def standardize_columns(df, columns):
    out = df.copy()
    for i in range(len(columns)):
        column_name = "standardize_" + columns[i]
        out[column_name] = stats.zscore(out[columns[i]], nan_policy="omit")
    return out

def features(df, Tweet_Col_Name):
    out=df.copy()
    out["length"] = out[Tweet_Col_Name].apply(lambda x: len(x.split(" "))) #Number of words in tweet
    out["contains_at"] = out[Tweet_Col_Name].apply(lambda x: "@" in x) #Check to see if the tweet is addressing someone specific
    out["contains_hashtag"] = out[Tweet_Col_Name].apply(lambda x: "#" in x) #Check to see if tweet is linked to category
    out["contains_link"] = out[Tweet_Col_Name].apply(lambda x: "http" in x) #Check to see if link is in tweet
    out["contains_pic"] = out[Tweet_Col_Name].apply(lambda x: "pic.twitter" in x) #Check to see if pic is in tweet
    return out

def data_wrangling(df, label_col_name, columns_standardize, tweet_col_name):
    out = df.copy()
    out["label"] = out[label_column_name].replace("Quality", False).replace("Spam", True)
    out = standardize_columns(out, columns_standardize)
    out = features(out, Tweet_col_Name)
    col_standardized_name = ["standardize_" + i for i in columns_standardize]
    col_keep_other = [Tweet_col_Name, "label", "Type", "is_retweet", "length", "contains_at", "contains_hashtag", "contains_link", "contains_pic"]
    col_keep = col_keep_other + col_standardized_name
    return out[col_keep]

def preprocess(string):
    tweet = string.lower()
    #Remove links
    tweet = re.sub(r"http\S+", "", tweet)
    #Remove pics
    tweet = re.sub(r"pic.twitter\S+", "", tweet)
    #Remove @
    tweet = re.sub(r"@\S+", "", tweet)
    #Remove #
    tweet = re.sub(r"#\S+", "", tweet)
    #Replace new line or tab with space
    tweet = re.sub(r"[\n\t]+", " ", tweet)
    #Only keeping words
    tweet = re.sub(r"[^a-zA-Z ]+", "", tweet)
    #Removing multiple spaces
    tweet = re.sub(r"[\s\s]+", " ", tweet)
    #Remove leading spaces
    tweet=tweet.strip()

    return tweet


def transform_train_data(df, tweet_col_name, label_col_name):
    data = df.copy()
    data["label"] = data[label_column_name].replace("Quality", 0).replace("Spam", 1)
    data["Process_tweet"] = data[tweet_column_name].apply(preprocess)
    return data[["Process_tweet", "label"]]
