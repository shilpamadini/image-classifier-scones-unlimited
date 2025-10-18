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