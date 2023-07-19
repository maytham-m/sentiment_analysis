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

ACCESS_ID = "AKIA6KT35UHOCTJD54GF"
ACCESS_KEY = "E5p2SdDJPjSHxZXKwH9bq6lYf27WMz11ADxI4r3b"


response = client.start_sentiment_detection_job(
    InputDataConfig={
        'S3Uri': 's3://maythamsbucket/OBJECT_NAME',
        'InputFormat': 'ONE_DOC_PER_FILE'|'ONE_DOC_PER_LINE'
    },
    OutputDataConfig={
        'S3Uri': 's3://maythamsbucket/OUTP',
        'KmsKeyId': '77bcab2d-6b07-48cd-adbd-d715926ff16c'
    },
    DataAccessRoleArn='arn:aws:s3:::maythamsbucket',
    JobName='myJob',
    LanguageCode='en'|'es'|'fr'|'de'|'it'|'pt'|'ar'|'hi'|'ja'|'ko'|'zh'|'zh-TW',
    #ClientRequestToken='string',
    VolumeKmsKeyId='77bcab2d-6b07-48cd-adbd-d715926ff16c',
    VpcConfig={
        'SecurityGroupIds': [
            'string',
        ],
        'Subnets': [
            'string',
        ]
    }
)


