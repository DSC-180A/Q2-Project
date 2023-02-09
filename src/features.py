
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

def data_wrangling(df, label_column_name, columns_standardize, Tweet_col_Name):
    out = df.copy()
    out["label"] = out[label_column_name].replace("Quality", False).replace("Spam", True)
    out = standardize_columns(out, columns_standardize)
    out = features(out, Tweet_col_Name)
    col_standardized_name = ["standardize_" + i for i in columns_standardize]
    col_keep_other = [Tweet_col_Name, "label", "Type", "is_retweet", "length", "contains_at", "contains_hashtag", "contains_link", "contains_pic"]
    col_keep = col_keep_other + col_standardized_name
    return out[col_keep]    