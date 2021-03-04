import json
import os

import boto3

print('Loading function')
step_client = boto3.client('stepfunctions')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    try:
        # Get the new bucket object from the event and parse its filename:
        bucket_name = event['detail']['requestParameters']['bucketName']
        # key is the name of our .tar.gz file, eg samples/G6RV5.tar.gz:
        key = event['detail']['requestParameters']['key']

        # grab sample_id from filename, eg: samples/G6RV5.tar.gz yields G6RV5:
        parts = key.split('.')[0]
        sample_id = parts.split('/')[1]
        filename = key.split('/')[1]
        # These env vars come from BucketConfiguration.yaml in aws-ab3.
        # Batch job parameters are specified in BatchConfiguration.yaml
        run_command = os.environ['RUN_COMMAND']
        serial_wait = os.environ['SERIAL_WAIT']
        payload = {"SampleID": sample_id, "ObjectName": key, "BucketName": bucket_name, "Filename": filename,
                   "SerialWait": serial_wait, "RunCommand": run_command, "JobType": "PARENT"}

        # trigger step function:
        state_machine_arn = os.environ['STATE_MACHINE_ARN']
        json_payload = json.dumps(payload)
        print('Starting intsitecaller with payload %s' % json_payload)
        response = step_client.start_execution(stateMachineArn=state_machine_arn, input=json_payload)
        print(response)
    except Exception as e:
        print(e)
        print('Error starting state machine. %s' % e)
        raise e
