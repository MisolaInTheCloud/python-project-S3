import boto3
import uuid
import json
from botocore.exceptions import ClientError

# AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = f"misolam4aceproject {uuid.uuid4()}"
file_name = "upload.txt"
table_name = "Students"

response_data = {}

try:
    # 1. Create S3 bucket
    s3.create_bucket(Bucket=misolam4aceproject , CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
    response_data['bucket_created'] = misolam4aceproject 

    # 2. Upload file to S3
    s3.upload_file(file_name, bucket_name, file_name)
    response_data['file_uploaded'] = file_name

    # 3. Generate pre-signed URL
    url = s3.generate_presigned_url('get_object',
        Params={'Bucket': bucket_name, 'Key': file_name},
        ExpiresIn=3600)
    response_data['pre_signed_url'] = url

    # 4. Create DynamoDB table
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'StudentID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'StudentID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    response_data['dynamodb_table'] = table_name

    # 5. Insert and retrieve record
    table.put_item(Item={'StudentID': 'S001', 'Name': 'Kemisola Adelakun', 'Email': 'misolakhemmy@gmai.com'})
    item = table.get_item(Key={'StudentID': 'S001'})['Item']
    response_data['student_record'] = item

except ClientError as e:
    response_data['error'] = str(e)

# 6. Output result as JSON
print(json.dumps(response_data, indent=4))
