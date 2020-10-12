from nltk.tokenize import word_tokenize, sent_tokenize
import json

class sentiment_lexicon:
    neg_words = set()
    pos_words = set()

    def __init__(self, pos_path, neg_path):
        with open(pos_path, 'r', encoding="latin-1") as pos_file:
            self.pos_words = set( pos_file.read().splitlines() )
        with open(neg_path, 'r', encoding="latin-1") as neg_file:
            self.neg_words = set( neg_file.read().splitlines() )

    """
    Return sentiment as an integer -1 to 1
    
    Tallies the positive and negative words from the lexicon in a sentence, and takes the difference. Classifies as -1
    for negative, 1 for positive and 0 for neutral (differnce of zero). 
    """
    def analyze_sentiment(self, sentence_in):
        word_list = word_tokenize(sentence_in)
        sentiment = 0
        for word in word_list:
            if word in self.neg_words:
                sentiment -= 1
            if word in self.pos_words:
                sentiment += 1
        if sentiment > 0: return 1
        elif sentiment == 0: return 0
        else: return -1

    def analyze_tweet(self, tweet):
        sentences = sent_tokenize(tweet)
        sentiment = 0
        for sent in sentences:
            sentiment += self.analyze_sentiment(sent)
        if sentiment > 0: return 1
        elif sentiment == 0: return 0
        else: return -1    

            
"""
Takes tweet text in gets sentiment out.
"""
        
def main():
    lex = sentiment_lexicon("../data/opinion-lexicon-English/positive-words.txt",
                            "../data/opinion-lexicon-English/negative-words.txt")  # Liu Hu Lexicon
    with open("../data/data_test2.json", 'r') as file:
        arr = json.load(file)
    for obj in arr:
        print(f"{obj}", lex.analyze_tweet(obj['tweet_text']))

if __name__ == "__main__":
    main()

    #TODO NEGATION WORDS
    #NORMALIZE BY THE NUMBER OF WORDS TOTAL IN TWEET
