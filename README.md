# Q2-Project

## How Spam Affects the Sentiment of Tweets

## Contributors
Lucas Lee, Tyson Tran, Yi (Skylar) Li


## Objective
The objective of our research is to develop a pipeline that filters spam content to model noise-reduced sentiments towards abortion on Twitter in real-time and analyze how spam content affects said sentiments. We compared the use of both Naive Bayes and a transfer learning model based on BERT to do spam filtration, and analyzed the impact of spam on sentiment distribution results to gain a deeper understanding of the role it plays in shaping public opinion on social media platforms.


## Pipeline
This project is produced as part of the DSC180B Capstone at UCSD, working with mentors from DataStax. In this project, we utilized Apache Pulsar through Astra Streaming to create a pipeline that ingests live stream of abortion related tweets, incoporate spam-filtering ML models, and performs sentiment analysis. This is primarily done through the following steps:
<img src="visuals/Untitled drawing (2).jpg" width=350 height=600> 
  
1. A producer makes Twitter API calls to request a stream of tweets through the FilteredStreamV2 endpoint 
2. The producer then publishes each incoming tweet (stringified Json) to a pulsar topic — Raw Tweet Topic.
3. Pulsar consumers subscribes to the Raw Tweet Topic and
   a) Consumer 1 performs sentiment analysis directly.
   b) Consumer 2 deploys Naive Bayes Model to label spam tweets, then performs SA.
   c) Consumer 3 deploys BERT Model to label spam tweets, then performs SA.
4. Consumers then update data to a data source.
5. Grafana visualizes the finding on <a href="https://skylar1013.grafana.net/d/_ztsas0Vz/capstone?orgId=1&from=1675065600000&to=1676188799000">dashboards</a>


With the above described pipeline, we now have a real-time stream of tweets being classified. We used Google Spreadsheet <a href="https://docs.google.com/spreadsheets/d/1fZ6MsCqtPXHWekonx2QGst0-eGei9ABzMG5LFDMEFbA/edit#gid=0">Google Spreadsheet</a> to collect real-time tweets with producer running.

## Requirements
- `requirements.txt` provided with all dependencies needed to run the code below
- `capstone_googlesheet_key.json` provided necessary credentials to update tweets to database.
- Astra Streaming account
- Twitter developer account

### Required Envronmental Variables
Running the producers and consumers require Astra Streaming topic keys. Setting up topics and creating an account is free, and more information can be found at the tutorial [here](https://docs.google.com/document/d/1VS31dXTIAmEkIh9o_9FcAhD-rVvcmnTo_Zm1zSMgCmY/edit).

The shell envrionmental variables are used within the `Producer` and `Consumer` classes within `producer.py` and `consumer.py`.
- `ASTRA_STREAMING_TOKEN`
- `ASTRA_STREAMING_URL`
- `ASTRA_TOPIC`


## How to run
`run.py test`. This runs a test pipeline on test data.
This will then run:
`python src/producer.py`. This makes requests to the Twitter API, publishing remote-work related tweets to a pulsar topic. In its current test tag, it will run the `src/producer_offline.py`, which is encouraged to be used to test.
`python src/consumer_*.py`. This captures the cleaned tweets, utilizes spam detection ML models, performs sentiment analysis, alters it so that it feeds your needs for downstream analysis. Note that there are three such consumers that will be simultanouesly run in the background. Please use `ps` to check the list of processes and `kill [pid]` to end the processes. This is fully intended as producer and consumers are long running jobs in the background.



## Usage
* Since the publishing time of the tweet is currently calculated by when the consumer receives the tweet from the topic, it's recommended to use concurrently run both `producer.py` and `consumer.py` simultaneously
* Keep in mind that this requires the setup of the Astra Streaming dashboard, a tutorial is available [here](https://docs.google.com/document/d/1VS31dXTIAmEkIh9o_9FcAhD-rVvcmnTo_Zm1zSMgCmY/edit#heading=h.3znysh7)
* With the above setup, the only thing left to change is the topic that the `Consumer` subscribes to, which is in its constructor.
* The path and nameof the generated CSV is modifiable in the constructor of a `Consumer` in `consumer.py`

## Files
- `src/producer.py`: Main driver class for fetching tweets
- `src/consumer_*.py`: Main driver class for filtering spams and performing sentiment analysis.
- `requirements.txt`: Required dependencies in Python

