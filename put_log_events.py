#!/usr/bin/python

import sys
from time import time
import boto3

USAGE = "To run this script, supply a log group and stream name as required command line arguments."

def main(args):    
    if (len(args) != 2):
        return print(USAGE)

    client = boto3.client('logs')

    log_group = args[0]
    log_stream = args[1]
    timestamp = int(time() * 1000)
    
    try:
        sequence_token = get_sequence_token(client, log_group, log_stream)
        response = client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': 'ERROR'
                }
            ],
            sequenceToken=sequence_token
        )
    except Exception as err:
        return print(err)

    return print(response)

def get_sequence_token(client, log_group, log_stream):
    
    response = client.describe_log_streams(
        logGroupName=log_group,
        logStreamNamePrefix=log_stream, 
        limit=1
    )
    
    if (len(response.get('logStreams')) == 0):
        raise Exception(f"Log stream \"{log_stream}\" does not exist in log group \"{log_group}\".")

    sequence_token = response.get('logStreams')[0].get('uploadSequenceToken')
    
    return sequence_token

if __name__ == '__main__':
    main(sys.argv[1:])