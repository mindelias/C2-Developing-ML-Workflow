import json
import boto3
import base64
from sagemaker.predictor import Predictor
from sagemaker.serializers import IdentitySerializer
from sagemaker.deserializers import JSONDeserializer

# Fill this in with YOUR deployed model endpoint name
ENDPOINT = "scones-unlimited-2025-08-07-21-48-29-994"  # Use YOUR endpoint name!

def lambda_handler(event, context):

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