import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import re
from datetime import datetime
from collections import Counter

# Twitter API credentials
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define search parameters
search_terms = ['fiebre', 'tos', 'gripe', 'estornudar', 'contagio', 'garganta', 
                'dolor cabeza', 'dificultad respirar', 'congestion nasal', 'mialgia', 
                'produccion esputo', 'hipoxemia', 'fatiga']
start_date = '2019-12-29'
end_date = '2020-03-14'
geocode = '4.6,-74.083333,50km'
language = 'es'

# Gather tweets
tweets = []
for term in search_terms:
    for tweet in tweepy.Cursor(api.search_tweets,
                               q=term,
                               lang=language,
                               geocode=geocode,
                               since=start_date,
                               until=end_date,
                               tweet_mode='extended').items():
        tweets.append(tweet)

# Pre-process data
def preprocess(tweet):
    # Convert to lowercase
    tweet = tweet.lower()
    # Remove non-alphanumeric characters
    tweet = re.sub(r'\W', ' ', tweet)
    # Remove stopwords
    stop_words = set(stopwords.words('spanish'))
    stop_words.update(['rt', 'https', 'co'])
    tweet = ' '.join([word for word in tweet.split() if word not in stop_words and len(word) > 3])
    return tweet

# Create DataFrame
data = {
    'user_created': [tweet.user.created_at for tweet in tweets],
    'date': [tweet.created_at.date() for tweet in tweets],
    'text': [preprocess(tweet.full_text) for tweet in tweets]
}

df = pd.DataFrame(data)

# Visualization: Date of user account creation
plt.figure(figsize=(10, 6))
df['user_created'].dt.date.value_counts().sort_index().plot(kind='bar')
plt.title('User Account Creation Dates')
plt.xlabel('Date')
plt.ylabel('Number of Accounts')
plt.show()

# Visualization: Tweets per day
plt.figure(figsize=(10, 6))
df['date'].value_counts().sort_index().plot(kind='bar')
plt.title('Number of Tweets per Day')
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.show()

# Visualization: Word Cloud
all_words = ' '.join([text for text in df['text']])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Tweets')
plt.axis('off')
plt.show()

