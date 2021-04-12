#!/usr/bin/env python

from json import dumps
import argparse
from time import time
from boto3 import client

def main():   
    """Sends a test log to the specified Cloudwatch log group/stream: https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutLogEvents.html#API_PutLogEvents_RequestSyntax"""

    args = validate_input()

    cloudwatch_client = client('logs')

    log_group = args.log_group
    log_stream = args.log_stream
    message = args.message
    timestamp = int(time() * 1000)
    
    try:
        sequence_token = get_sequence_token(cloudwatch_client, log_group, log_stream)
        response = cloudwatch_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ],
            sequenceToken=sequence_token
        )
    except Exception as err:
        return print(err)

    return print(response)

def get_sequence_token(cloudwatch_client, log_group, log_stream):
    """Fetches the sequence token for the provided log stream"""
    
    response = cloudwatch_client.describe_log_streams(
        logGroupName=log_group,
        logStreamNamePrefix=log_stream, 
        limit=1
    )
    
    if (len(response.get('logStreams')) == 0):
        raise Exception(f"Log stream \"{log_stream}\" does not exist in log group \"{log_group}\".")

    sequence_token = response.get('logStreams')[0].get('uploadSequenceToken')
    
    return sequence_token

def validate_input():
    """Validates user input"""
    parser = argparse.ArgumentParser(description='Uploads log events to a Cloudwatch log group.')
    
    parser.add_argument('--log-group', type=str, required=True,
                        help='targeted Cloudwatch log group')
    parser.add_argument('--log-stream', type=str, required=True,
                        help='log stream in your Cloudwatch log group')
    parser.add_argument('--message', type=str, required=True,
                        help='log events to be uploaded.')

    return parser.parse_args()

if __name__ == '__main__':
    main()
