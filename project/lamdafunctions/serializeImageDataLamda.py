import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize input data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event.get('s3_key')
    bucket = event.get('s3_bucket') 

    if not bucket or not key:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing s3_bucket or s3_key", "event": event})
        }
    
    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

