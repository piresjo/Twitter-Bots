import tweepy, time, sys
 

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
# api.update_status("Test...")
# time.sleep(2)
# api.update_status("Hello World")
# IT WORKS!

# Some basics
    