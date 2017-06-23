import tweepy, time, sys, datetime, re

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Establish all the stuff that I can do without getting onto Twitter
# First, train so that the tweets can be accurately analyzed
instances = 200
subjectDocs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:instances]]
objectDocs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:instances]]
trainSubjectDocs = subjectDocs[:160]
testSubjectDocs = subjectDocs[160:200]
trainObjectDocs = objectDocs[:160]
testObjectDocs = objectDocs[160:200]
trainingDocs = trainSubjectDocs+trainObjectDocs
testingDocs = testSubjectDocs+testObjectDocs
sentimentAnalyzer = SentimentAnalyzer()
allNegWords = sentimentAnalyzer.all_words([mark_negation(doc) for doc in trainingDocs])
unigramFeats = sentimentAnalyzer.unigram_word_feats(allNegWords, min_freq=4)
sentimentAnalyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigramFeats)
trainingSet = sentimentAnalyzer.apply_features(trainingDocs)
testSet = sentimentAnalyzer.apply_features(testingDocs)
trainer = NaiveBayesClassifier.train
classifier = sentimentAnalyzer.train(trainer, trainingSet)
sid = SentimentIntensityAnalyzer()

# Second, set up the regex so that emojis can be filtered out
# Thankfully our sitting president doesn't go overboard with the emojis
emojiPattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  
    u"(\ud83c[\udf00-\uffff])|"  
    u"(\ud83d[\u0000-\uddff])|"  
    u"(\ud83d[\ude80-\udeff])|"  
    u"(\ud83c[\udde0-\uddff])"  
    "+", flags=re.UNICODE)


# For security reasons, the key and secret values
# will be omitted whenever I push to github 
consumerKey = ''
consumerSecret = ''
accessKey = ''
accessSecret = ''
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessKey, accessSecret)
api = tweepy.API(auth)
 

 
# To test if I have a connection, send some test tweets
#api.update_status("Testing another bot")
#time.sleep(2)
#api.update_status("Connected")
# IT WORKS!

# First, extract tweets within a 24 hour period from @realDonaldTrump

timeStamp = time.time()
timeStampDayBefore = timeStamp - 86400
dateTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
dateTimeDayBefore = datetime.datetime.fromtimestamp(timeStampDayBefore).strftime('%Y-%m-%d %H:%M:%S')
#print(dateTimeStamp)
#print(dateTimeDayBefore)
trumpTweets = api.user_timeline(screen_name = 'realDonaldTrump', count = 40, include_rts = True)
tweetCorpus = []
for tweet in trumpTweets:
	tweetDate = str(tweet.created_at)
	#print(tweetDate)
	if (tweetDate < dateTimeDayBefore):
		break
	isRetweet = tweet.retweeted
	isFavorited = tweet.favorited
	#print(isRetweet)
	#print(isFavorited)
	tweetContents = tweet.text
	#print(tweetContents[0:2])
	if tweetContents[0:2] != "RT" and not isRetweet and not isFavorited:
		#print(tweetContents)
		#print("")
		tweetContents = emojiPattern.sub(r'', tweetContents)
		tweetContents = tweetContents.replace("amp;", "")
		tweetCorpus.append(tweetContents)

# Then go through the tweets and analyze them
negSum = 0
neutralSum = 0
posSum = 0
for tweet in tweetCorpus:
	ss = sid.polarity_scores(tweet)
	negVal = ss['neg']
	neutralVal = ss['neu']
	posVal = ss['pos']
	negSum += negVal
	neutralSum += neutralVal
	posSum += posVal

negAverage = negSum / len(tweetCorpus)
neutralAverage = neutralSum / len(tweetCorpus)
posAverage = posSum / len(tweetCorpus)

#print(negAverage)
#print(neutralAverage)
#print(posAverage)

# Use that analysis to make a tweet

tweetString = "Trump's Tweets Analysis - " + dateTimeStamp[0:10] + "\nNumber of Tweets: " + str(len(tweetCorpus))
tweetStringAdder = ""
if (negAverage > neutralAverage and negAverage > posAverage):
	tweetStringAdder = "He's not happy"
elif (neutralAverage > negAverage and neutralAverage > posAverage):
	tweetStringAdder = "He's neither in a good mood or bad mood"
else:
	tweetStringAdder = "He's in a good mood"

tweetString = tweetString + "\n" + tweetStringAdder
#print(tweetString)
api.update_status(tweetString)
api.update_status("This has been your daily analysis of Trump's tweets")

    