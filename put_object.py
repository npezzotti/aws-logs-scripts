#!/usr/bin/env python

import sys
import json
import boto3

USAGE = "To run this script, supply an s3 bucket and a key as required command line arguments."

def main(args):
    if (len(args) != 2):
        return print(USAGE)

    s3 = args[0]
    key = args[1]

    data = {'brand': 'Ford', 'model': 'F-250', 'id': 13245634, 'color': 'black'}
    serializedData = json.dumps(data)

    client = boto3.client('s3')
    
    try:
        response = client.put_object(
            Bucket=s3,
            Key=key,
            Body=serializedData,
        )
    except Exception as err:
        return print(err)

    return print(response)

if __name__ == '__main__':
    main(sys.argv[1:])
