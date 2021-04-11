#!/usr/bin/python

from json import dumps
from sys import argv
from time import time
from boto3 import client

USAGE = "To run this script, supply a log group and stream name as required command line arguments."

def main(args):   
    """Sends a test log to the specified Cloudwatch log group/stream: https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutLogEvents.html#API_PutLogEvents_RequestSyntax"""

    if (len(args) != 2):
        return print(USAGE)

    data = {'brand': 'Ford', 'model': 'F-250', 'id': 13245634, 'color': 'black'}
    serializedData = dumps(data)

    cloudwatch_client = client('logs')

    log_group = args[0]
    log_stream = args[1]
    timestamp = int(time() * 1000)
    
    try:
        sequence_token = get_sequence_token(cloudwatch_client, log_group, log_stream)
        response = cloudwatch_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': '{"status": "ERROR"}'
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

if __name__ == '__main__':
    main(argv[1:])
