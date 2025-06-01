
############################################################
#  This Version can be used inside an Ec2 instance instead #
#  of Lambda Function                                      #
############################################################

import boto3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def count_s3_objects(bucket_name, folder_name):
    # Initialize S3 and CloudWatch clients with the specified region
    s3 = boto3.client('s3', region_name='ap-southeast-2')
    cloudwatch = boto3.client('cloudwatch', region_name='ap-southeast-2')

    logging.info("Starting object count in bucket '%s' within folder '%s'", bucket_name, folder_name)

    # Initialize object count and continuation token
    object_count = 0
    continuation_token = None

    # Ensure folder name ends with a '/' to treat it as a directory prefix
    if not folder_name.endswith('/'):
        folder_name += '/'

    while True:
        logging.info("Listing objects with continuation token: %s", continuation_token)

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
        # ignoring zero-byte folder placeholder objects
        current_batch_count = 0
        for obj in response.get('Contents', []):
            if obj['Key'] != folder_name and obj['Size'] > 0:
                object_count += 1
                current_batch_count += 1

        logging.info("Counted %d objects in current batch.", current_batch_count)

        # Check for continuation token to see if there are more objects to list within the folder
        continuation_token = response.get('NextContinuationToken')
        if not continuation_token:
            break

    # Publish the count to CloudWatch
    logging.info("Publishing object count to CloudWatch: %d objects", object_count)
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
    
    logging.info("Finished counting. Total objects in folder '%s' of bucket '%s': %d", folder_name, bucket_name, object_count)

# Set bucket name and folder name
bucket_name = 'my_s3_bucket_name'
folder_name = 'my_folder'

if __name__ == '__main__':
    count_s3_objects(bucket_name, folder_name)
