# Twitter-Bot
Twitter bot using Twitter's API, tweepy, GPT-2, 3 Legged O-Auth, and Sentiment analysis
### AUTHOR: Michael Blank


## <B>START OF INSTRUCTIONS: </B>
The ***hw1_authenticator.py*** file contains all authenticator portions of the assignment (part 2). It also builds the corpus in the ***corpus.txt*** file and pulls the <B> @FreedoniaNews </B> into the ***freedoniatweets.txt*** file. It does this by pulling the tweets with tweepy and putting them in txt files.

The ***hw1_api.py*** file contains all of the bot posting activity, sentiment analysis, and botometer data collection. It does this by putting the tweets in an array, looping through the array and posting a response to the tweet when GPT-2 when the sentiment is correct.


### Important Notes in hw1_api.py:

 To change the number of training steps, the variable ***Steps*** in function <B> train_GPT() </B> can be changed accordingly.

***Uncomment nextline if you wish to train GPT.***
            
<code>sess = train_GPT()</code>.


***Uncomment nextlines if you wish to run GPT without training.***

<code> sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess) </code>


***Uncomment nextlines if you wish to post reply tweets to all 8 posts on FreedoniaNews.***

<code>
generated_text = '@FreedoniaNews ' + generated_text

generated_text = re.sub(r'^https?:\/\/.*[\r\n]*', '', generated_text, flags=re.MULTILINE)

generated_text = re.sub(r'http\S+', '', generated_text)

api.update_status(generated_text,in_reply_to_status_id = tweets_ids[i])

positioninidlist = positioninidlist + 1 </code>

### And most importantly in MAIN...

***Uncomment to reply to FreedoniaNews tweets.***
<code>tweet_reply(api, 'FreedoniaNews')</code>

***Uncomment to print Botometer results.***
<code>print(botometer_runner())</code>

Otherwise, just run ***hw1_authenticator.py*** for authentication and ***hw1_api.py*** for tweet replies and data analysis.

## <B> END OF INSTRUCTIONS </B>


## My results from the Botometer Test:

    {'cap': {'english': 0.08590409243653727, 'universal': 0.006431292840898396}, 'categories': {'content': 0.946174528632784, 'friend': 0.9136223598156034, 'network': 0.6495621487664512, 'sentiment': 0.8465067076913749, 'temporal': 0.845608000205838, 'user': 0.5957894732961813}, 'display_scores': {'content': 4.7, 'english': 2.4, 'friend': 4.6, 'network': 3.2, 'sentiment': 4.2, 'temporal': 4.2, 'universal': 0.6, 'user': 3.0}, 'scores': {'english': 0.4848645828256039, 'universal': 0.1285158337598371}, 'user': {'id_str': '1222181578144735232', 'screen_name': 'Michaelblank123'}}

My overall score, as an english user, was 2.4/5.0. I believe this intermidate score is a result of a few aspects of my account. The content of my tweets was seen to be extremely botlike, which could be a result of my 35 character tweet restriction that often cut the tweets short in the middle and the excessive number of tags that GPT produced, often unrelated to the parent tweet. Furthermore, it turns out being friends with other bot accounts severely affected my score (4.6). However, I believe my score was lowered by the fact that my account had real credentials (3.0) and my tweets still included the same subject as the parent tweet and sometimes provided realistic responses.


