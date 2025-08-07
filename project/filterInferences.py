import json

THRESHOLD = 0.93

def lambda_handler(event, context):
    
    # Get the data from previous function
    body = event.get('body', event)
    inferences = body['inferences']
    
    # Find the highest confidence score
    max_confidence = max(inferences)
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max_confidence > THRESHOLD
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        return {
            'statusCode': 200,
            'body': body
        }
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")