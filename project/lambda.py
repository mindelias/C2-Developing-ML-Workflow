# Lambda Function 1: serializeImageData
import json
import boto3
import base64

s3 = boto3.client('s3')

def serialize_image_data(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']
    
    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png')
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data.decode('utf-8'),
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# Lambda Function 2: classifyImage
import json
import boto3
import base64

def classify_image(event, context):
    # Get the image data from the previous function
    body = event.get('body', event)
    image_data = body['image_data']
    
    # Decode the image data
    image = base64.b64decode(image_data)
    
    # Use boto3 SageMaker runtime (built into Lambda)
    runtime = boto3.client('sagemaker-runtime')
    
    # Make prediction using invoke_endpoint
    response = runtime.invoke_endpoint(
        EndpointName='scones-unlimited-2025-08-07-21-48-29-994',
        ContentType='image/png',
        Body=image
    )
    
    # Parse the response
    result = json.loads(response['Body'].read().decode())
    
    # Add inferences to our data
    body["inferences"] = result
    
    return {
        'statusCode': 200,
        'body': body
    }

# Lambda Function 3: filterInferences
import json

THRESHOLD = 0.93

def filter_inferences(event, context):
    
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