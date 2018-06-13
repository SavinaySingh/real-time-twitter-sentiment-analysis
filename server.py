import tweepy
import time
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
from tweepy import Stream,OAuthHandler
from tweepy.streaming import StreamListener
import re
from flask import Flask,render_template,request
app = Flask(__name__)
def calctime(a):
    return time.time()-a

positive=0
negative=0
compound=0
count=0
pos=0
neg=0
count_pos=0
count_neg=0
neutral=0
ntrl=0
initime=time.time()
plt.ion()
consumer_key = 'K71liuYcaJPFtbDaAb4RFYwHd'
consumer_secret ='63cYvvqiaOvcxrg0L9WSXZ0AHuAednyPZSGuo2R7tbWIMfVgBR'

access_token = '1005146743074254848-Y9NAMyOB9aH4sMHCwohgZAqkNnQEQl'
access_token_secret = 'MgT580EDkX9msRLNgWHaB9fAvdcSEYAyEK4pEbXzew0i3'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api=tweepy.API(auth)

@app.route('/')
def hello_world():

    return render_template("index.html")


@app.route('/answer',methods=["POST"])
def index():
    class listener(StreamListener):
        def on_data(self, raw_data):
            global initime
            t = int(calctime(initime))
            all_data = json.loads(raw_data)
            tweet = all_data["text"].encode("utf-8")
            tweet = " ".join(re.findall("[a-zA-Z]+", tweet))
            blob = TextBlob(tweet.strip())

            global positive
            global negative
            global compound
            global count
            global pos, neg, count_neg, count_pos, neutral, ntrl

            count = count + 1
            senti = 0
            for sen in blob.sentences:
                senti = sen.sentiment.polarity
                if sen.sentiment.polarity > 0:
                    positive = sen.sentiment.polarity
                    count_pos += 1

                elif sen.sentiment.polarity < 0:
                    negative = sen.sentiment.polarity
                    count_neg += 1
                else:
                    neutral += 1
            compound += senti
            print count
            # print count_pos
            # print count_neg
            # print tweet.strip()
            # print senti
            # print t
            # print str(positive)+' '+str(negative)+' '+str(compound)

            pos = (count_pos * 100) / count
            neg = (count_neg * 100) / count
            ntrl = (neutral * 100) / count


            print(tweet.strip())
            print("positive :",pos)
            print("negative:",neg)
            print("neutral:",ntrl)
            if count == 200:
                return False
            else:
                return True

        def on_error(self, status_code):
            print(status_code)


    text=request.form['text']
    twitterStream = Stream(auth, listener(count))
    twitterStream.filter(track=[text])
    dict = {'positive': pos, 'negative': neg, 'neutral': ntrl}
    return render_template('index2.html', result=dict)


if __name__ == '__main__':
    app.run(host = '0.0.0.0' , port = 5000)
