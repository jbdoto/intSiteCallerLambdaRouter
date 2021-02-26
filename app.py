import json
import urllib.parse
import boto3
import os

print('Loading function')
step_client = boto3.client('stepfunctions')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    try:
        # Get the new bucket object from the event and parse its filename:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        # key is the name of our .tar.gz file:
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        # grab sample_id from filename, eg: G6RV5.tar.gz yields G6RV5
        sample_id = key.split('.')[0]
        payload = {"SampleID": sample_id, "ObjectName": key, "BucketName": bucket_name, "SerialWait": "TRUE"}

        # trigger step function:
        state_machine_arn = os.environ['STATE_MACHINE_ARN']
        json_payload = json.dumps(payload)
        print('Starting intsitecaller with payload %s' % json_payload)
        response = step_client.start_execution(stateMachineArn=state_machine_arn, input=json_payload)
        print(response)
    except Exception as e:
        print(e)
        print('Error starting state machine. %s' % (e))
        raise e
