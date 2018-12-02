import boto3
import requests
from requests_aws4auth import AWS4Auth


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

# Lambda execution starts here
def lambda_handler(event, context):
    for record in event['Records']:

        # Get the bucket name and key for the new file
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        client=boto3.client('rekognition')

        response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':key}})

        print('Detected labels for ' + key)    
        labels = []
        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))
            labels.append(label['Name'])

        document= {
            'objectKey': key,
            'bucket': bucket,
            'createdTimestamp': record['eventTime'],
            'labels': labels,
        }
        
        # print('this is my url', url)
        # print('this is my awsauth', awsauth)
        # print('this is my document',document)
        # print('this is my headers', headers)

        r = requests.post(url, auth=awsauth, json=document, headers=headers)
        print("request API response", r.text)
        
        # g = requests.get(host+'/'+index+'/_search?face')
        # print(g.text)

# from elasticsearch import Elasticsearch, RequestsHttpConnection
# from requests_aws4auth import AWS4Auth
# import requests
# import boto3

# host = 'https://vpc-photos-myembdnp3phlpewoockbi2csmy.us-east-1.es.amazonaws.com/' # For example, my-test-domain.us-east-1.es.amazonaws.com
# region = 'us-east-1' # e.g. us-west-1

# index = 'photos'
# type = 'lambda-type'
# url = host + '/' + index + '/' + type

# headers = { "Content-Type": "application/json" }

# service = 'es'
# credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)

# # es = Elasticsearch(
# #     hosts = [{'host': host, 'port': 443}],
# #     http_auth = awsauth,
# #     use_ssl = True,
# #     verify_certs = True,
# #     connection_class = RequestsHttpConnection
# # )

# def lambda_handler(event, context):
#     for record in event['Records']:

#         bucket = record['s3']['bucket']['name']
#         key = record['s3']['object']['key']
        
#         client=boto3.client('rekognition')

#         response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':key}})
        
#         print('Detected labels for ' + key)    
#         labels = []
#         for label in response['Labels']:
#             print (label['Name'] + ' : ' + str(label['Confidence']))
#             labels.append(label['Name'])

#         json = {
#             'objectKey': key,
#             'bucket': bucket,
#             'createdTimestamp': record['eventTime'],
#             'labels': labels,
#         }

#         # document = {
#         #     "title": "Moneyball",
#         #     "director": "Bennett Miller",
#         #     "year": "2011"
#         # }

#         r = requests.post(url, auth=awsauth, json=json, headers=headers)
#         print(r.text)

#         # es.index(index="photos", doc_type="image", body=json)

#         # print(es.get(index="photos", doc_type="image"))