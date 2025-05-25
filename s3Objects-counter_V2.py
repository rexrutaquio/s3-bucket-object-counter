#############################################################################################
# This Version includes pagination, enabling it to count beyond the 1,000-object threshold  #
#############################################################################################

import boto3
import os

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    s3 = boto3.client('s3')

    # Initialize object count and continuation token
    object_count = 0
    continuation_token = None

    while True:
        # List objects in the S3 bucket with continuation token
        if continuation_token:
            response = s3.list_objects_v2(Bucket=bucket_name, ContinuationToken=continuation_token)
        else:
            response = s3.list_objects_v2(Bucket=bucket_name)

        # Count the number of objects in the current response
        object_count += response.get('KeyCount', 0)

        # Check for continuation token to see if there are more objects to list
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
                ],
                'Value': object_count,
                'Unit': 'Count'
            },
        ]
    )
    
    return {
        'statusCode': 200,
        'body': f'{object_count} objects in bucket {bucket_name}.'
    }
