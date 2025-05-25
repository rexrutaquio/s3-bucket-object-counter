#############################################################################################
# This Version includes pagination, enabling it to count beyond the 1,000-object threshold  #
# ***** this VErsion will count the objects inside a specific folder in the bucket *******  #
#############################################################################################

import boto3
import os

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    folder_name = os.environ['FOLDER_NAME']

    s3 = boto3.client('s3')

    # Initialize object count and continuation token
    object_count = 0
    continuation_token = None

    # Ensure folder name ends with a '/' to treat it as a directory prefix
    if not folder_name.endswith('/'):
        folder_name += '/'

    while True:
        # List objects with the specified folder name as prefix
        if continuation_token:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=folder_name,
                ContinuationToken=continuation_token
            )
        else:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=folder_name
            )

        # Count the number of objects in the current response,
        # ignoring zero-byte folder placeholder objects
        for obj in response.get('Contents', []):
            if obj['Key'] != folder_name and obj['Size'] > 0:
                object_count += 1

        # Check for continuation token to see if there are more objects to list within the folder
        continuation_token = response.get('NextContinuationToken')
        if not continuation_token:
            break

    # Publish the count to CloudWatch
    cloudwatch.put_metric_data(
        Namespace='S3ObjectCount',
        MetricData=[
            {
                'MetricName': 'ObjectCount',
                'Dimensions': [
                    {
                        'Name': 'BucketName',
                        'Value': bucket_name
                    },
                    {
                        'Name': 'Folder',
                        'Value': folder_name
                    },
                ],
                'Value': object_count,
                'Unit': 'Count'
            },
        ]
    )
    
    return {
        'statusCode': 200,
        'body': f'{object_count} objects in folder {folder_name} of bucket {bucket_name}.'
    }
