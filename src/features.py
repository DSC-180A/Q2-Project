
import pandas as pd
from scipy import stats
import re

def standardize_columns(df, columns):
    """_summary_: Standardizes a column with a z-score

        Args:
            df: The dataframe containg columns to standardize
            columns: list of strings of column names to standardize

        Returns:
            dataframe with new columns that are standardized with z-score
    """
    out = df.copy()
    for i in range(len(columns)):
        column_name = "standardize_" + columns[i]
        out[column_name] = stats.zscore(out[columns[i]], nan_policy="omit")
    return out

def features(df, Tweet_Col_Name):
    """_summary_: Creates new features about a tweet

        Args:
            df: The dataframe to create new features
            Tweet_Col_Name: The string name of the column containing the tweet contents

        Returns:
            dataframe with the new features created
    """
    out=df.copy()
    #Number of words in tweet
    out["length"] = out[Tweet_Col_Name].apply(lambda x: len(x.split(" "))) 
    #Check to see if the tweet is addressing someone specific
    out["contains_at"] = out[Tweet_Col_Name].apply(lambda x: "@" in x) 
    #Check to see if tweet is linked to category
    out["contains_hashtag"] = out[Tweet_Col_Name].apply(lambda x: "#" in x) 
    #Check to see if link is in tweet
    out["contains_link"] = out[Tweet_Col_Name].apply(lambda x: "http" in x) 
    #Check to see if pic is in tweet
    out["contains_pic"] = out[Tweet_Col_Name].apply(lambda x: "pic.twitter" in x) 
    return out

def data_wrangling(df, label_col_name, columns_standardize, tweet_col_name):
    """_summary_: Does all the data wranglings steps at once. Replaces label with True/False and applies 
                  standardize_columns and features function

        Args:
            df: The dataframe to wrangle the data for
            label_col_name: The string name of the column of labels
            columns_standardize: A list of string column names to standardize
            tweet_col_name: The string name of the column containing the tweet contents

        Returns:
            dataframe with new columns that are standardized with z-score
    """
    out = df.copy()
    # Replacing Quality/Spam with True/False
    out["label"] = out[label_col_name].replace("Quality", False).replace("Spam", True)
    # Standardizing columns
    out = standardize_columns(out, columns_standardize)
    # Creating features from tweet
    out = features(out, tweet_col_name)
    col_standardized_name = ["standardize_" + i for i in columns_standardize]
    col_keep_other = [tweet_col_name, "label", "Type", "is_retweet", "length", "contains_at", "contains_hashtag", "contains_link", "contains_pic"]
    col_keep = col_keep_other + col_standardized_name
    return out[col_keep]

def preprocess(string):
    """_summary_: Processing the tweet and removing extraneous features

        Args:
            string: String of the tweet text

        Returns:
            String of the processed tweet
    """
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
    """_summary_: Processing the Tweets for Naive Bayes

        Args:
            df: The dataframe of the train data
            tweet_col_name: A string of the column name that contains the tweet
            label_col_name: A string of the column name that contains the labels

        Returns:
            dataframe with new columns that are standardized with z-score
    """
    data = df.copy()
    data["label"] = data[label_col_name].replace("Quality", 0).replace("Spam", 1)
    data["Process_tweet"] = data[tweet_col_name].apply(preprocess)
    return data[["Process_tweet", "label"]]


