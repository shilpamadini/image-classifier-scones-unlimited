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

