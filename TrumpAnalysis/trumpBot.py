import tweepy, time, sys, datetime, re
 

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

emojiPattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  
    u"(\ud83c[\udf00-\uffff])|"  
    u"(\ud83d[\u0000-\uddff])|"  
    u"(\ud83d[\ude80-\udeff])|"  
    u"(\ud83c[\udde0-\uddff])"  
    "+", flags=re.UNICODE)

# First, extract tweets within a 24 hour period from @realDonaldTrump
timeStamp = time.time()
timeStampDayBefore = timeStamp - 86400
dateTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
dateTimeDayBefore = datetime.datetime.fromtimestamp(timeStampDayBefore).strftime('%Y-%m-%d %H:%M:%S')
trumpTweets = api.user_timeline(screen_name = 'realDonaldTrump', count = 40, include_rts = True)
tweetCorpus = []
for tweet in trumpTweets:
	tweetDate = str(tweet.created_at)
	if (tweetDate < dateTimeDayBefore):
		break
	tweetContents = tweet.text
	tweetContents = emojiPattern.sub(r'', tweetContents)
	tweetContents = tweetContents.replace("amp;", "")
	# print(tweetContents)
	# print("")
	tweetCorpus.append(tweetContents)

# Then go through the tweets and analyze them

    