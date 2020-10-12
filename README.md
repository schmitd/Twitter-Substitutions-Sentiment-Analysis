# Twitter-Substitutions-Sentiment-Analysis
Measuring the sentiment of Tweets including words with asterisks substituted for various letters.
The original goal was to see if a change in sentiment could be measured when people were avoiding the twitter search mechanism by obscuring the names of public figures or events.
Users often use this tactic to avoid interactions from people who intentionally seek out confrontations over certian topics.

This code is dependent on (tweepy)[www.tweepy.org] and (NLTK)[www.ntlk.org]
You will also need your own Twitter API keys in a secrets folder to use the tweet scraping functionality.
sentiment_lexicon.py requires that you provide your own files containing postive and negative sentiment words. 
