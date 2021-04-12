#!/usr/bin/env python

from json import dumps
from argparse import ArgumentParser
from boto3 import client

def main():
    args = validate_input()

    s3_client = client('s3')

    s3 = args.s3
    key = args.key
    body = args.body
    
    try:
        response = s3_client.put_object(
            Bucket=s3,
            Key=key,
            Body=body,
        )
    except Exception as err:
        return print(err)

    return print(response)

def validate_input():
    """Validates user input"""
    
    parser = ArgumentParser(description='Uploads an object to an s3 bucket.')
    
    parser.add_argument('--s3', type=str, required=True,
                        help='the s3 to upload to')
    parser.add_argument('--key', type=str, required=True,
                        help='the key for the uploaded object')
    parser.add_argument('--body', type=str, required=True,
                        help='the object to be uploaded')

    return parser.parse_args()

if __name__ == '__main__':
    main()
