# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Comprehend to
detect entities, phrases, and more in a document.
"""

import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

ACCESS_ID = "***"
ACCESS_KEY = "***"


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
    
    '''
    def detect_entities(self, text, language_code):
        """
        Detects entities in a document. Entities can be things like people and places
        or other common terms.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The list of entities along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_entities(
                Text=text, LanguageCode=language_code)
            entities = response['Entities']
            logger.info("Detected %s entities.", len(entities))
        except ClientError:
            logger.exception("Couldn't detect entities.")
            raise
        else:
            return entities
    '''

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
    '''
    def detect_pii(self, text, language_code):
        """
        Detects personally identifiable information (PII) in a document. PII can be
        things like names, account numbers, or addresses.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The list of PII entities along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_pii_entities(
                Text=text, LanguageCode=language_code)
            entities = response['Entities']
            logger.info("Detected %s PII entities.", len(entities))
        except ClientError:
            logger.exception("Couldn't detect PII entities.")
            raise
        else:
            return entities
    '''

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
    '''
    def batch_detect_sentiment(self, text, language_code):
        """
        Detects the overall sentiment expressed in a document. Sentiment can
        be positive, negative, neutral, or a mixture.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The sentiments along with their confidence scores.
        """
        try:
            response = self.comprehend_client.batch_detect_sentiment(
                TextList=[text,], LanguageCode=language_code)
            logger.info("Detected primary sentiment %s.", response['ResultList'][0]['Sentiment'])
        except ClientError:
            logger.exception("Couldn't detect sentiment.")
            raise
        else:
            return response
    '''
    '''
    def detect_syntax(self, text, language_code):
        """
        Detects syntactical elements of a document. Syntax tokens are portions of
        text along with their use as parts of speech, such as nouns, verbs, and
        interjections.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The list of syntax tokens along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_syntax(
                Text=text, LanguageCode=language_code)
            tokens = response['SyntaxTokens']
            logger.info("Detected %s syntax tokens.", len(tokens))
        except ClientError:
            logger.exception("Couldn't detect syntax.")
            raise
        else:
            return tokens
    '''

def usage_demo():
    print('-'*88)
    print("Welcome to the Amazon Comprehend detection demo!")
    print('-'*88)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    comp_detect = ComprehendDetect(boto3.client('comprehend', region_name='us-west-2', aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY))

    with open('reviews.txt') as reviews_file:
        reviews_file = reviews_file.read()

    demo_size = 3


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
    '''
    print("Detecting entities.")
    entities = comp_detect.detect_entities(reviews_file, lang_code)
    print(f"The first {demo_size} are:")
    pprint(entities[:demo_size])

    print()
    '''

    print("Detecting key phrases.")
    phrases = comp_detect.detect_key_phrases(reviews_file, lang_code)
    print(f"The first {demo_size} are:")
    pprint(phrases[:demo_size])

    print()
    '''
    print("Detecting personally identifiable information (PII).")
    pii_entities = comp_detect.detect_pii(reviews_file, lang_code)
    print(f"The first {demo_size} are:")
    pprint(pii_entities[:demo_size])

    print()
    '''

    print("Detecting sentiment.")
    sentiment = comp_detect.detect_sentiment(reviews_file, lang_code)
    print(f"Sentiment: {sentiment['Sentiment']}")
    print("SentimentScore:")
    pprint(sentiment['SentimentScore'])
    print()

    '''
    print("Detecting (BATCH) sentiment.")
    sentiment = comp_detect.batch_detect_sentiment(reviews_file, lang_code)
    print(f"Sentiment: {sentiment['ResultList'][0]['Sentiment']}")
    print("SentimentScore:")
    pprint(sentiment['ResultList'][0]['SentimentScore'])
    '''

    print()
    '''
    print("Detecting syntax elements.")
    syntax_tokens = comp_detect.detect_syntax(reviews_file, lang_code)
    print(f"The first {demo_size} are:")
    pprint(syntax_tokens[:demo_size])

    print()
    '''
    print("Thanks for watching!")
    print('-'*88)


if __name__ == '__main__':
    usage_demo()
