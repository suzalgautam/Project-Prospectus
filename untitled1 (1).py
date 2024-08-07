# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10V5lm_OVCIO0fKD7svjV-7ULn8RxbbJw
"""

# Import necessary libraries
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from IPython.display import Markdown, display, Image
import re

# Function to print the title
def print_title(title):
    display(Markdown(f'# {title}'))

print_title("Analyzing Sentiment in Social Media During Major Political Events")

# Function to display the header image
def display_header_image(image_url):
    display(Image(url=image_url))

header_image = "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQ9HZyzuhKqap59vFs7lcI1eAlVv-sYa-sAhVzzBaqxa4DnPu0mQ7McNlJWRkUbpQELP-OFHbYD0mNgZlc"  # replace with your actual image link
display_header_image(header_image)

# Function to print the abstract
def print_abstract(abstract_text):
    display(Markdown(abstract_text))

abstract = """
## Abstract

This project aims to analyze sentiment on social media during major political events using Python. The focus is on Twitter data,
leveraging natural language processing (NLP) techniques to identify sentiment trends and their correlation with political events.
Key tasks include data collection, data cleaning, sentiment analysis, and visualization of results. By examining tweets related to
specific political events, this project seeks to uncover patterns in public opinion and how they shift during these events. The project
utilizes libraries such as Tweepy for data collection, Pandas for data cleaning, TextBlob and VADER for sentiment analysis, and Matplotlib
and Seaborn for visualization.
"""

print_abstract(abstract)

# Twitter API credentials
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Function to authenticate to Twitter API
def authenticate_twitter(api_key, api_secret_key, access_token, access_token_secret):
    try:
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        api.verify_credentials()  # Verify credentials
        print("Twitter Authentication Successful")
        return api
    except tweepy.TweepyException as e:
        print(f"Error during Twitter Authentication: {e}")
        return None

# Function to fetch tweets
def fetch_tweets(api, query, count=100):
    if api is None:
        return pd.DataFrame()  # Return an empty DataFrame if API authentication failed

    try:
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode='extended').items(count)
        tweet_list = [[tweet.created_at, tweet.user.screen_name, tweet.full_text] for tweet in tweets]
        tweet_df = pd.DataFrame(tweet_list, columns=['Datetime', 'Username', 'Text'])
        return tweet_df
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return pd.DataFrame()

# Function to clean tweets
def clean_tweet(text):
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)  # Remove @ mentions
    text = re.sub(r'#', '', text)  # Remove '#' symbol
    text = re.sub(r'RT[\s]+', '', text)  # Remove RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove hyperlinks
    text = re.sub(r'\n', ' ', text)  # Remove new lines
    return text

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Function to plot sentiment
def plot_sentiment(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Sentiment', data=df, palette='viridis')
    plt.title('Sentiment Analysis of Tweets')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()

# Main function to run the analysis
def run_analysis(query, tweet_count):
    # Authenticate to Twitter
    api = authenticate_twitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Fetch tweets
    tweets_df = fetch_tweets(api, query, tweet_count)

    if tweets_df.empty:
        print("No tweets fetched. Please check the query and try again.")
        return None

    # Clean tweets
    tweets_df['Cleaned_Text'] = tweets_df['Text'].apply(clean_tweet)

    # Analyze sentiment
    tweets_df['Sentiment'] = tweets_df['Cleaned_Text'].apply(analyze_sentiment)

    # Plot sentiment
    plot_sentiment(tweets_df)

    return tweets_df

# Run the analysis for a specific political event
query = "US Presidential Debate 2024"  #
tweet_count = 1000  # number of tweets to fetch
tweets_df = run_analysis(query, tweet_count)

# Check if tweets_df is not None before attempting to display it
if tweets_df is not None:
    # Display the first few rows of the resulting DataFrame
    display(tweets_df.head())
else:
    print("No data to display.")