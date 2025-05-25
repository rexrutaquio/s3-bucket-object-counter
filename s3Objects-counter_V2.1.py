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
    folder_name = os.environ['FOLDER_NAME']  # Specify the folder name here

    s3 = boto3.client('s3')

    # Initialize object count and continuation token
    object_count = 0
    continuation_token = None

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

        # Count the number of objects in the current response
        object_count += response.get('KeyCount', 0)

        # Check for continuation token to see if there are more objects to list within the folder
        continuation_token = response.get('NextContinuationToken')
        if not continuation_token:
            break

    # Publish the count to CloudWatch
    cloudwatch.put_metric_data(
        Namespace='S3ObjectCount',  # Custom namespace
        MetricData=[
            {
                'MetricName': 'ObjectCount',  # Custom metric name
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
