# -*- coding: utf-8 -*-
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analysis = TextBlob("The tab includes $10 billion for vacations and the balance in food, clothing, liquor and cigarettes that should have been paid for out of their own pockets.")
print(analysis.sentiment.subjectivity, analysis.sentiment.polarity)

# vader = SentimentIntensityAnalyzer()

# vs = vader.polarity_scores("The tab includes $10 billion for vacations and the balance in food, clothing, liquor and cigarettes that should have been paid for out of their own pockets.")
# print(vs)