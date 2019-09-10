import datetime
import hashlib
import re
import time

import feedparser
import nltk
import telegram

import config

last_post_date = datetime.datetime.now()

# Regex for getting description from summary
description = re.compile("(?<=>).*?(?=\[)")

bot = telegram.Bot(token=config.bot_token)

last_hash = ''

while True:
    news = feedparser.parse(config.rss_link)['items']
    m = hashlib.sha256()
    m.update(str(news[0]['link']).encode('utf-8'))

    if m.digest() != last_hash:
        summary = news[0]['summary']
        match = description.search(summary)
        # Splitting description by sentences
        sentences = nltk.tokenize.sent_tokenize(summary[match.span()[0]:match.span()[1]])

        # Logging data
        print(news[0]['link'])
        print(sentences[0], sentences[1])
        print(m.digest())
        bot.send_message(
            chat_id=config.channel_id,
            text=sentences[0] + " " + sentences[1] + '\n\n' + news[0]['link'])

        last_hash = m.digest()
    time.sleep(300)
