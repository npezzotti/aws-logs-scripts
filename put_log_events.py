#!/usr/bin/python

import sys
from time import time
import boto3

def main(args):
    usage = "To run this script, supply a log group and stream name as required command line arguments."
    
    if (len(args) != 2):
        return print(usage) 

    client = boto3.client('logs')

    log_group = args[0]
    log_stream = args[1]

    sequenceToken = get_sequence_token(client, log_group, log_stream)

    timestamp = int(time() * 1000)

    try:
        response = client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': 'ERROR'
                }
            ],
            sequenceToken=sequenceToken
        )
    except client.exceptions.InvalidSequenceTokenException as e: 
        return print(f'Incorrect sequence token: {str(e)}')
    except client.exceptions.UnrecognizedClientException as e:
        return print(f'Please configure your AWS CLI before running thsi script: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html')

    return print("OK")

def get_sequence_token(client, log_group, log_stream):
    try:
        response = client.describe_log_streams(
            logGroupName=log_group,
            logStreamNamePrefix=log_stream, 
            limit=1
        )
    except client.exceptions.ResourceNotFoundException as e:
        return print(f'Resource not found: {str(e)}')

    if (len(response.get('logStreams')) == 0):
        return print(f"Log stream \"{log_stream}\" does not exist in log group \"{log_group}\".")
    sequence_token = response.get('logStreams')[0].get('uploadSequenceToken')
    
    return sequence_token

if __name__ == '__main__':
    main(sys.argv[1:])