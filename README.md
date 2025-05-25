Automated S3 Object Counting and Visualization in Grafana

### Overview

This project involves creating an automated solution to count objects in an AWS S3 bucket at regular intervals and visualize the counts using Grafana. The system leverages AWS Lambda for computation, Amazon CloudWatch for metric storage, and Grafana for data visualization. The solution is ideal for monitoring S3 bucket activity and analyzing trends over time.

### Architecture

1. **AWS Lambda**: A serverless function used to retrieve and count the number of objects in the specified S3 bucket.
2. **Amazon CloudWatch**: A monitoring and observability service where the counts are published as custom metrics.
3. **Grafana**: An open-source analytics and interactive visualization tool for displaying CloudWatch metrics.

### Components

#### AWS Lambda Function

- **Purpose**: Counts objects in an S3 bucket and publishes the count to CloudWatch.
- **Language**: Python
- **Key Features**:
  - Scheduled execution via CloudWatch Events.
  - Publishes counts using the CloudWatch API.

#### IAM Role and Policy

- **Purpose**: Provides necessary permissions for Lambda to access S3 bucket and CloudWatch.
- **Policy**:
  ```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "s3:ListBucket"
              ],
              "Resource": "arn:aws:s3:::your-bucket-name"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "cloudwatch:PutMetricData"
              ],
              "Resource": "*"
          }
      ]
  }
  ```
  - Replace `"your-bucket-name"` with the actual name of your S3 bucket.

#### CloudWatch Event Rule

- **Purpose**: To schedule periodic execution of the Lambda function.
- **Configuration**:
  - Create a rule with a cron expression (e.g., `cron(0 * * * ? *)`) to execute hourly.

#### Grafana Dashboard

- **Purpose**: Visualizes the object count metrics stored in CloudWatch.
- **Configuration**:
  - Set up CloudWatch as a data source in Grafana.
  - Create a graph panel to display metrics from the `S3ObjectCount` namespace.

### Step-by-Step Setup

1. **AWS Lambda Configuration**:
   - Create a new Lambda function using the AWS console.
   - Configure the function to use Python as the runtime.
   - Deploy the provided code and set the environment variable `BUCKET_NAME`.

2. **IAM Role Setup**:
   - Create an IAM role with the specified policy.
   - Associate the role with the Lambda function.

3. **CloudWatch Event Rule**:
   - Navigate to the CloudWatch Events section in AWS and create a new rule.
   - Define the schedule using cron syntax.

4. **Grafana Integration**:
   - Ensure Grafana has access to CloudWatch, typically through an appropriate IAM access key.
   - Add CloudWatch as a data source.
   - Build a dashboard to query and visualize `S3ObjectCount` metrics.

### Testing & Validation

- **Lambda Execution**: Manually trigger the Lambda function to verify successful counts and metric publishing.
- **CloudWatch**: Access CloudWatch to review published metrics and confirm expected data.
- **Grafana**: Check the dashboard to ensure real-time updates reflect the bucket content accurately.

### Conclusion

This solution automates S3 bucket monitoring, enabling easy visualization and tracking of object counts over time. It exemplifies the use of serverless technologies and cloud-based monitoring tools to deliver efficient and scalable solutions.

