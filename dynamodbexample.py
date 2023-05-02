from textwrap import indent
import boto3
import json

s3 = boto3.client('s3')
dynam = boto3.resource('dynamodb')

# #########################################################################################
# #lambda function to grab object from s3 bucket to load json file to add item to dynamodb#
# #########################################################################################

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    jsonfile =event['Records'][0]['s3']['object']['key']
    resp = s3.get_object(
    Bucket=bucket,
    # IfMatch='dynamodbexample.json'
    Key=jsonfile
)

    resp_data = resp['Body']
    resp_data_read = resp_data.read()
    resp_data_decode = json.loads(resp_data_read)
    # resp_data_final = resp_data_read.decode("utf-8")
    table = dynam.Table('userlist')
    table.put_item(Item=resp_data_decode)
