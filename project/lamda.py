# lamda Functions in one lamda.py file


# Lamda Function SerializingImageData
# This function will copy an object from S3, base64 encode it, and then return it to the step function as image_data in an event.

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


# Lamda Function classifyImageData
# This function takes the image output from the previous function, decodes it, and then pass inferences back to the the Step Function as an event.

import json
import boto3
import base64

runtime = boto3.client("sagemaker-runtime")

ENDPOINT = "image-classification--1760804763"

def lambda_handler(event, context):

    try:

        print("Event Receieved :", event)
        event_body = event.get("body")
        image_data = event_body.get("image_data")
        print(image_data)
        if not image_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing image_data", "event": event})

            }
        # Decode the image data
        image = base64.b64decode(image_data)
        print(image)

        # invoke the end point
    
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT,
            ContentType="application/x-image",
            Body=image
            ) 

        inferences = json.loads(response["Body"].read().decode('utf-8'))
    
        # We return the data back to the Step Function    
        event_body["inferences"] = inferences
        return {
            'statusCode': 200,
            'body': event_body
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'error': f"key error: {str(e)}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }


# Lamda Function filterInferences
# This function  filter low-confidence inferences. We Defined a threshold of 0.70 If the model any inference that is below this threshold will be filtered and alterted to operations as step function failure 

import json

THRESHOLD = 0.70

def lambda_handler(event, context):
    print("Received the Event:", event)

    # Get inferences from the event
    event_body = event.get('body')

    inferences = event_body.get('inferences')
    if inferences is None:
        return {
            'statusCode': 400,
            'error': "Missing 'inferences' key in event"
        }

    meets_threshold = max(inferences) >= THRESHOLD

    if not meets_threshold:
        raise Exception("THRESHOLD CONFIDENCE NOT MET")

    return {
        'statusCode': 200,
        'body': event_body
    }