import tweepy
from textblob import  TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")

consumerkey = "your API"
consumerkeysecret = "your API"
accesstoken="your API"
accesstokensecret="your API"

#create OAuthhandler object

authenticate = tweepy.OAuthHandler(consumerkey, consumerkeysecret)

#set access token ans secret

authenticate.set_access_token(accesstoken, accesstokensecret)

#create tweepy API object to fetch tweets

api = tweepy.API(authenticate, wait_on_rate_limit= True)


posts = api.user_timeline(screen_name='BillGates', count= 100, lang = 'en', tweet_mode="extended")

# convert to dataframe

df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
df.head()

#cleaning the tweets using regular expression

def clean(text):
  text = re.sub(r"^(?=.{1,254}$)(?=.{1,64}@)[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*@[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$",'',text)
  text = re.sub(r'#/[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,4}/','',text)
  text = re.sub(r'RT[\s]+(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)','',text)
  text = re.sub(r'^http:\/\/\S+(\/\S+)*(\/)?$','',text)
  return text

df['Tweets'] = df['Tweets'].apply(clean)

  df

#get the subjectivity of the tweets

#subjectivit means facts

  def getsubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

#get the Polarity of the tweets

#polarity means positive words and negative words

def getpolarity(text):
  return TextBlob(text).sentiment.polarity


df['subjectivity'] = df['Tweets'].apply(getsubjectivity)
df['polarity'] = df['Tweets'].apply(getpolarity)


df

allwords = ' '.join([twts for twts in df['Tweets']])

# display the tweets using wordcloud

wordcloud = WordCloud(width = 500, height = 500,random_state= 20, max_font_size=119).generate(allwords)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# get the score of positive and negative words

def getanalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return "Neutral"
  else:
    return "Positive"


df["Analysis"] = df['polarity'].apply(getanalysis)


df

#diplay the positive tweets

j = 1
sortdf  = df.sort_values(by=['polarity'])
for i in range(0, sortdf.shape[0]):
  if(sortdf["Analysis"][i] == "Positive"):
    print(str(j)+ ")"  + sortdf['Tweets'][i])
    print()
    j = j+1


#diplay the negative tweets

j = 1
sortdf  = df.sort_values(by=['polarity'])
for i in range(0, sortdf.shape[0]):
  if(sortdf["Analysis"][i] == "Negative"):
    print(str(j)+ ")"  + sortdf['Tweets'][i])
    print()
    j = j+1


#display the positive , negative using Scatterplot.


plt.figure(figsize=(8,6))

for i in range(0, df.shape[0]):
  plt.scatter(df['polarity'][i],df['subjectivity'][i],color='blue')

plt.title("Sentimental Analysis")
plt.xlabel("polarity")
plt.ylabel("subjectivity")
plt.show()












  
