# -*- coding: utf-8 -*-
from googleapiclient.discovery import build
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME,
              YOUTUBE_API_VERSION,
              developerKey="AIzaSyDmbd-0qyZVxV9crXIPrgGBcYhILzkzPIM")
ucom = []
def load_comments(match):
    for item in match["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        print("Comment by user {}: {}".format(author, text))
        ucom.append(text)

def get_comment_threads(youtube, video_id, limit):
    results = youtube.commentThreads().list(
        part="snippet",
        maxResults=limit,
        videoId=video_id,
        textFormat="plainText"
    ).execute()
    return results

def get_comment_thread(youtube, video_id, mytoken, limit):
    results = youtube.commentThreads().list(
        part="snippet",
        maxResults=limit,
        videoId=video_id,
        textFormat="plainText",
        pageToken=mytoken
    ).execute()
    return results
limit1 = 100
limit = int(input("Enter number of comments: "))
vid = input("Enter video id: ")
video_id = vid
if limit>100:
  if limit%100==0:
    count=limit/100-1
  else:
    count=limit/100
else:
  count=0
  limit1=limit 
match = get_comment_threads(youtube, video_id, limit1)
next_page_token = match["nextPageToken"]
load_comments(match)
while count>0:
    if count==1:
      match1 = get_comment_thread(youtube, video_id, next_page_token, (limit-(limit/100)*100))
    else:    
      match1 = get_comment_thread(youtube, video_id, next_page_token, 100)
    next_page_token = match1["nextPageToken"]
    load_comments(match1)
    count=count-1
print(len(ucom))

import nltk 
filtered_comments=[]
import re
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
for comment in ucom:
    com = remove_emoji(comment)
    filtered_comments.append(com)
print(filtered_comments)
print(len(filtered_comments))

import nltk
import emoji
import re 
import statistics
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid=SentimentIntensityAnalyzer()
positive = 0
wpositive = 0
spositive = 0
negative = 0
wnegative = 0
snegative = 0
neutral = 0
track = []
for comment in filtered_comments:
  i = sid.polarity_scores(comment)['compound']
  if (i == 0):  
        neutral += 1
  elif (i > 0 and i <= 0.3):
      wpositive += 1
  elif (i > 0.3 and i <= 0.6):
      positive += 1
  elif (i > 0.6 and i <= 1):
      spositive += 1
  elif (i > -0.3 and i <= 0):
      wnegative += 1
  elif (i > -0.6 and i <= -0.3):
      negative += 1
  elif (i > -1 and i <= -0.6):
      snegative += 1
  track.append(i)
NoOfTerms = len(filtered_comments)
positive = format(100 * float(positive) / float(NoOfTerms), '0.2f')
wpositive = format(100 * float(wpositive) / float(NoOfTerms), '0.2f')
spositive = format(100 * float(spositive) / float(NoOfTerms), '0.2f')
negative = format(100 * float(negative) / float(NoOfTerms), '0.2f')
wnegative = format(100 * float(wnegative) / float(NoOfTerms), '0.2f')
snegative = format(100 * float(snegative) / float(NoOfTerms), '0.2f')
neutral = format(100 * float(neutral) / float(NoOfTerms), '0.2f')
Final_score = statistics.mean(track) 
if Final_score>0:
    print("Using Vader Sentiment Analyzer: ")
    print("    Overall Reviews are Positive with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
elif Final_score<0:
    print("Using Vader Sentiment Analyzer: \n")
    print("Overall Reviews are Negative with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
else :
    print("Using Vader Sentiment Analyzer: \n")
    print("Overall Reviews are Moderate with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
print()
print("Detailed Report using Vader Sentiment: ")
print(str(positive) + "% people thought it was positive")
print(str(wpositive) + "% people thought it was weakly positive")
print(str(spositive) + "% people thought it was strongly positive")
print(str(negative) + "% people thought it was negative")
print(str(wnegative) + "% people thought it was weakly negative")
print(str(snegative) + "% people thought it was strongly negative")
print(str(neutral) + "% people thought it was neutral")

from textblob import TextBlob
positive = 0
wpositive = 0
spositive = 0
negative = 0
wnegative = 0
snegative = 0
neutral = 0
track = []
for comment in filtered_comments:
  analysis = TextBlob(comment)
  i = analysis.sentiment.polarity
  if (i == 0):  
        neutral += 1
  elif (i > 0 and i <= 0.3):
      wpositive += 1
  elif (i > 0.3 and i <= 0.6):
      positive += 1
  elif (i > 0.6 and i <= 1):
      spositive += 1
  elif (i > -0.3 and i <= 0):
      wnegative += 1
  elif (i > -0.6 and i <= -0.3):
      negative += 1
  elif (i > -1 and i <= -0.6):
      snegative += 1
  track.append(i)
NoOfTerms = len(filtered_comments)
positive = format(100 * float(positive) / float(NoOfTerms), '0.2f')
wpositive = format(100 * float(wpositive) / float(NoOfTerms), '0.2f')
spositive = format(100 * float(spositive) / float(NoOfTerms), '0.2f')
negative = format(100 * float(negative) / float(NoOfTerms), '0.2f')
wnegative = format(100 * float(wnegative) / float(NoOfTerms), '0.2f')
snegative = format(100 * float(snegative) / float(NoOfTerms), '0.2f')
neutral = format(100 * float(neutral) / float(NoOfTerms), '0.2f')
Final_score = statistics.mean(track) 
if Final_score>0:
    print("Using TextBlob Sentiment Analyzer: ")
    print("    Overall Reviews are Positive with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
elif Final_score<0:
    print("Using TextBlob Sentiment Analyzer: \n")
    print("Overall Reviews are Negative with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
else :
    print("Using TextBlob Sentiment Analyzer: \n")
    print("Overall Reviews are Moderate with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
print()
print("Detailed Report using TextBlob: ")
print(str(positive) + "% people thought it was positive")
print(str(wpositive) + "% people thought it was weakly positive")
print(str(spositive) + "% people thought it was strongly positive")
print(str(negative) + "% people thought it was negative")
print(str(wnegative) + "% people thought it was weakly negative")
print(str(snegative) + "% people thought it was strongly negative")
print(str(neutral) + "% people thought it was neutral")
