#######################################################################
# Note: This code is limited to counting up to 1,000 S3 objects only  #
#######################################################################

import boto3
import os

# Initialize S3 and CloudWatch clients
s3 = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    
    # List objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    # Count the number of objects
    object_count = response.get('KeyCount', 0)
    
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
