# coding: utf-8

# # COMS W1002 Computing in Context: Computing in the humanities

# In this project you will develop tools for performing sentiment analysis on
# a database of tweets from across the country. When the project is complete 
# you should be able to estimate the sentiment of tweets filtered by content.

import codecs
import datetime

# **Problem 1** Write a function called `make_tweets` that takes as input a 
# file name and returns a list of dictionaries. Each dictionary corresponds 
# to a tweet.


def make_tweets(filename):
    with codecs.open(filename,encoding='utf-8', errors='ignore') as tweet_txt:
        tweets=[]
        for line in tweet_txt:
            #Split each line in file by tab
            lines = line.split('\t')
            #Initialize dictionary to store tweets in
            d={}
            d['latitude']=float(lines[0].split(",")[0].strip('"[]"'))
            d['longitude']=float(lines[0].split(",")[1].strip('"[]"'))
            dt=lines[2].split()
            #Get year/month/day 
            dt[0]=dt[0].split('-')
            year=int(dt[0][0])
            month=int(dt[0][1])
            day=int(dt[0][2])
            #Get hour/minute/second
            dt[1]=dt[1].split(':')
            hour=int(dt[1][0])
            minute=int(dt[1][1])
            second=int(dt[1][2])      
            #Convert variables to datetime notation 
            d['time']=datetime.datetime(year, month, day, hour, minute, second)
            d['text']=lines[3].strip().lower()
            tweets.append(d)
    return tweets


# **Problem 2** Write a function `add_sentiment` to determine the sentiment of 
# each tweet by taking the average sentiment over all of the words in the 
#tweet. The function should return a new list of tweets where each tweet has a 
# new key '`sentiment`' with numeric value between -1 and 1, or *None* 
# representing the sentiment of the tweet. 

import csv 
from string import punctuation

#Run the make_tweets file with corresponding file name
# tweets= make_tweets(filename)

def add_sentiment(tweets,filename):
    #Create new list of tweets with sentiment key 
    tweets_2 = []
    word_list = []
    with open('sentiments.csv') as sentiments_csv:
        #Create fieldnames for sentiment file
        fieldnames = ['word','sentiment']
        reader=csv.DictReader(sentiments_csv,fieldnames=fieldnames)
        #Initialize list of just words listed in sentiment file
        sentiment_list = []
        #Convert each word/sentiment pair to dictionary 
        for row in reader:
            d=dict(row)
            sentiment_list.append(d)
    #Create separate list of words listed in sentiments.csv file
    for entry in sentiment_list:
        word_list.append(entry['word'])
    #For each tweet, get the text of the current tweet
    for tweet in tweets:
        current_text = tweet['text']
        #Store number of words with sentiments
        num_items =0
        sentiment_val = 0
        items = current_text.split()
        #Check if each word is in the sentiments.csv file
        for word in items:
            word =word.strip(punctuation)
            for list_item in word_list:
                if word == list_item:
                #If the word in the tweet is in the sentiment list, get the 
                # corresponding sentiment value 
                    num_items +=1
                    sentiment_val += float(sentiment_list[word_list.index(word)]['sentiment'])
        if (num_items > 0):
            tweet['sentiment']=sentiment_val/num_items
        else:
            tweet['sentiment']=0
        tweets_2.append(tweet)
    return tweets_2


# **Problem 3**  Write a function called `tweet_filter` that will return a 
# new list of tweets filtered by the content of the tweet text.


#Run the make_tweets function; input file name parameter
tweets=make_tweets(filename)
#Run the add_sentiment function; input file name parameter
tweets_2=add_sentiment(tweets, filename)

def tweet_filter(tweets, words):
    words=words.split(' ')
    words=set(words)
    #Create a new array to store the tweets that contain the words 
    tweets_with_words=[]
    for tweet in tweets_2:
        #Create new list for tweet without punctuation
        new_current = []
        current_tweet=tweet['text'].split(' ')
        for word in current_tweet:
            #Strip punctuation off word in tweet and append to new_current
            word=word.strip(punctuation)
            new_current.append(word)
        # If the search words are a subset of the set of words in tweet,
        # to list of tweets that satisfy the condition
        if words.issubset(set(new_current)):
            tweets_with_words.append(tweet)
    return tweets_with_words


# **Problem 4** Use your work above and below to answer the following questions:

# 1. What is the average sentiment of tweets containing the word 'beer'?

tweets = make_tweets('some_tweets.txt')
tweets_2=add_sentiment(tweets, 'some_tweets.txt')
tweets=tweets_2[::]

    #Run tweet_filter on 'beer'
beer = tweet_filter(tweets, 'beer')
    
average_sentiment = 0

#For every tweet containing word 'beer', find the sentiment value
for tweet in beer:
    average_sentiment += tweet['sentiment']
#The average sentiment is the sum of sentiments divided by the number of 
# tweets containing the word 'beer'
average_sentiment=average_sentiment/len(beer)
print(average_sentiment)

# average_sentiment = 0.09375

# 2. What is the average sentiment of tweets containing the word 'coffee'?
 
tweets=make_tweets('some_tweets.txt')
tweets_2=add_sentiment(tweets, 'some_tweets.txt')
tweets=tweets_2[::]

coffee = tweet_filter(tweets, 'coffee')

average_sentiment = 0

for tweet in coffee:
    average_sentiment += tweet['sentiment']
average_sentiment=average_sentiment/len(coffee)
print(average_sentiment)

# average_sentiment = 0.107142

# 3. Consider the average sentiment of the tweets containing at lesast one 
# of the words 'beer', 'movie','coffee', 'work'. Which word leads to a list of 
# tweets with the lowest average sentiment?

tweets=make_tweets('some_tweets.txt')
tweets_2=add_sentiment(tweets, 'some_tweets.txt')
tweets=tweets_2[::]
    
movie = tweet_filter(tweets, 'movie')
work = tweet_filter(tweets, 'work')

#Calculate average sentiment for tweets with word 'movie'
average_sentiment = 0

for tweet in movie:
    average_sentiment += tweet['sentiment']
average_sentiment=average_sentiment/len(movie)
print(average_sentiment)

# average_sentiment = -0.011719


#Calculate average sentiment for tweets with word 'work'
average_sentiment = 0

for tweet in work:
    average_sentiment += tweet['sentiment']
average_sentiment=average_sentiment/len(work)
print(average_sentiment)

# average_sentiment = 0.060088

# Lowest average sentiment: 'movie'
