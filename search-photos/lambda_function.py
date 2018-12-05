import boto3
import requests
import botocore.response as br
from requests_aws4auth import AWS4Auth
import json
import base64

region = 'us-east-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-photos-homework2-mn2totrrrk7e6pcdgr7a63vlzy.us-east-1.es.amazonaws.com' # the Amazon ES domain, including https://
index = 'photos'
typ = 'image'
url = host + '/' + index + '/' + typ

headers = { "Content-Type": "application/json" }

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("event", event)
    client = boto3.client('lex-runtime')

    response = client.post_text(
        botName = "SearchPhotos",
        botAlias = "SearchOne",
        userId = context.aws_request_id,
        inputText = event['params']['querystring']['q'], #replace with get text
    )

    # lex will return a json with details of the intent 
    s = response['slots']['categories']

    if s == None: 
        return []

    # there's a possibility of multiple keywords, so have to split the string
    labels = s.split()
    # print(labels)

    images = []
    for label in labels:
        r = requests.get(url + '/'+ '_search?q=labels:' + label)
        # print(r.text)
        data = r.json()
        # print("data", data)
        for item in data['hits']['hits']:
            # print(item['_source']['objectKey'])
            if item['_source']['objectKey'] not in images:
                images.append(item['_source']['objectKey'])
    print("image list", images)

    return images
    """
    print("contents of s3")    
    for key in s3.list_objects(Bucket='photos-homework2')['Contents']:
        print(key['Key'])

    body_list = []
    for image in images:
        
        response = s3.get_object(
            Bucket = 'photos-homework2',
            Key = image,
        )
        print("s3 response", response)
        body_response = response['Body']
        streaming_obj = br.StreamingBody(raw_stream=body_response, content_length=response['ContentLength'])
        # streaming_obj.read(amt=None)

        string_data = streaming_obj.read() #.decode('base64')
        # print("string data", string_data)
        # encoded = base64.b64encode(string_data)
        # ret = {
        #     "statusCode": 200,
        #     "body": response['Body'],
        #     "isBase64Encoded": False
        # }

        
        body_list.append(string_data)

    # print(body_list)
    return body_list
    """
        


