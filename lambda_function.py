# this is an aws lambda function wrapper, for a simple hello world, triggered event

import boto3
import os
import uuid
import sys
from urllib.parse import unquote_plus

s3_client = boto3.client( 's3' )

def lambda_handler( event, context ):

    for record in event['Records']:
        
        bucket = record['s3']['bucket']['name']
        
        key = unquote_plus(record['s3']['object']['key'])
        print( key )
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/parsed-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)
        with open( download_path, 'r') as f:
            text = f.read()

        text += '\nhello again!\n'

        with open( upload_path, 'w' ) as f:
            f.write( text )

        outbucket = bucket[:-3]
        # key is the uploaded file name
        s3_client.upload_file(upload_path, '{}-out'.format(outbucket), 'more-' + key)
    
    return { 'message':'hello world' }

