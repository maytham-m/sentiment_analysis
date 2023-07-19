# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Comprehend to
detect entities, phrases, and more in a document.
"""

from datetime import datetime
from outscraper import ApiClient

import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

import streamlit as st

import plotly.express as px

import pandas as pd


logger = logging.getLogger(__name__)

ACCESS_ID = "AKIA6KT35UHOCTJD54GF"
ACCESS_KEY = "E5p2SdDJPjSHxZXKwH9bq6lYf27WMz11ADxI4r3b"


class ComprehendDetect:
    """Encapsulates Comprehend detection functions."""
    def __init__(self, comprehend_client):
        """
        :param comprehend_client: A Boto3 Comprehend client.
        """
        self.comprehend_client = comprehend_client

    
    def detect_languages(self, text):
        """
        Detects languages used in a document.

        :param text: The document to inspect.
        :return: The list of languages along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_dominant_language(Text=text)
            languages = response['Languages']
            logger.info("Detected %s languages.", len(languages))
        except ClientError:
            logger.exception("Couldn't detect languages.")
            raise
        else:
            return languages


    def detect_key_phrases(self, text, language_code):
        """
        Detects key phrases in a document. A key phrase is typically a noun and its
        modifiers.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The list of key phrases along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_key_phrases(
                Text=text, LanguageCode=language_code)
            phrases = response['KeyPhrases']
            logger.info("Detected %s phrases.", len(phrases))
        except ClientError:
            logger.exception("Couldn't detect phrases.")
            raise
        else:
            return phrases
    
    def detect_sentiment(self, text, language_code):
        """
        Detects the overall sentiment expressed in a document. Sentiment can
        be positive, negative, neutral, or a mixture.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The sentiments along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_sentiment(
                Text=text, LanguageCode=language_code)
            logger.info("Detected primary sentiment %s.", response['Sentiment'])
        except ClientError:
            logger.exception("Couldn't detect sentiment.")
            raise
        else:
            return response



st.title('Sentiment Analysis on Customer Reviews')
url = st.text_input("Paste the url of the Google Maps location: ")
number_of_reviews = st.slider("How many reviews would you like to analyse?", 0, 20)

#number_of_reviews = 5

if st.button('Run'):

    #'https://www.google.com/maps/place/Atlantis,+The+Palm/@25.1303886,55.1170255,16.56z/data=!4m9!3m8!1s0x3e5f153e3609c979:0x5945a418a804ac5!5m3!1s2021-07-17!4m1!1i2!8m2!3d25.1304426!4d55.1171498'
    #'https://www.google.com/maps/place/PwC/@25.2007427,55.2726391,17z/data=!4m9!1m2!2m1!1spwc!3m5!1s0x3e5f428139416ec1:0x1068135ebb8e92a7!8m2!3d25.201603!4d55.2726522!15sCgNwd2MiA4gBAZIBHmJ1c2luZXNzX21hbmFnZW1lbnRfY29uc3VsdGFudA'
    api_client = ApiClient(api_key='Z29vZ2xlLW9hdXRoMnwxMDgxMjg1MjUyMTM2MzgxNTIyMTB8NGRlMmRlOTU3Ng')
    response = api_client.google_maps_business_reviews(
        url,
        language='en',
        limit = 50,
        organizations_per_query_limit=1
    )

    print(response)

    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")

    #st.write('**The reviews are: **')   

    f = open("/Users/maytham/Desktop/sentiment_analysis/reviews.txt", "w")
    num = number_of_reviews
    for review in response[0]['reviews_data']:
        print(review['review_text'])
        if review['review_text'] != None:
            f.write(review['review_text'])
            f.write('\n')
            #st.text(review['review_text'])
            num = num - 1
        if num <= 0:
            break
            

    f.close()


    print('-'*88)
    print("Welcome to the Amazon Comprehend detection demo!")
    print('-'*88)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    comp_detect = ComprehendDetect(boto3.client('comprehend', region_name='us-west-2', aws_access_key_id=ACCESS_ID,
            aws_secret_access_key= ACCESS_KEY))

    with open('reviews.txt') as reviews_file:
        reviews_file = reviews_file.read()

    #demo_size = 3


    print("Sample text used for this demo:")
    print('-'*88)
    print(reviews_file)
    print('-'*88)

    print()

    print("Detecting languages.")
    languages = comp_detect.detect_languages(reviews_file)
    pprint(languages)
    lang_code = languages[0]['LanguageCode']

    print()

    print("Detecting key phrases.")
    phrases = comp_detect.detect_key_phrases(reviews_file, lang_code)
    #print(f"The first {demo_size} are:")
    print(f"They are:")
    #pprint(phrases[:demo_size])
    pprint(phrases)

    phrases_sorted = sorted(phrases, key = lambda i: i['Score'])

    print("sorted:")
    print(phrases_sorted)

    st.write('**The top **',5,'** phrases are: **')
    for i in range(5):
        st.text(phrases_sorted[-1 -i]['Text'])

    print()

    print("Detecting sentiment.")
    sentiment = comp_detect.detect_sentiment(reviews_file, lang_code)
    print(f"Sentiment: {sentiment['Sentiment']}")
    print("SentimentScore:")
    pprint(sentiment['SentimentScore'])

    sent_dict = dict(sorted(sentiment['SentimentScore'].items(), key=lambda item: item[1])).items()

    sentiment_sorted = list(sent_dict)


    st.write('**The strongest sentiment from the **', number_of_reviews - num-1, '**reviews is:**')

    print(sentiment_sorted)
    print()
    print(sentiment_sorted[3])
    st.write(sentiment_sorted[3][0], ', at ', '{:.2f}%.'.format(sentiment_sorted[3][1]*100))

    
    data = {'Sentiment': [sentiment_sorted[0][0], sentiment_sorted[1][0], sentiment_sorted[2][0], sentiment_sorted[3][0]], 'Score': [float('{:.2f}'.format(sentiment_sorted[0][1]*100)), float('{:.2f}'.format(sentiment_sorted[1][1]*100)), float('{:.2f}'.format(sentiment_sorted[2][1]*100)), float('{:.2f}'.format(sentiment_sorted[3][1]*100))]}
    fig1 = px.pie(data, values='Score', names='Sentiment', title='Sentiment Breakdown')
    st.write(fig1)

    
    #df = pd.DataFrame(data)
    #print(df)
    #fig2 = px.pie(df, values='Score', names='Sentiment', title='Sentiment Breakdown')
    #st.write(fig2)
    #fig2.show()
    


    print("Thanks for watching!")
    print('-'*88)
