import boto3
import json
from botocore.exceptions import ClientError

def call_llama3_1_aws(prompt):
    aws_region = ''
    access_key_id = ''
    secret_access_key = ''

    # Create a Bedrock Runtime client (not "bedrock", must be "bedrock-runtime")
    bedrock_runtime = boto3.client(
        'bedrock-runtime',
        region_name=aws_region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )

    model_id = ""

    native_request = {
        "prompt": prompt,
        "max_gen_len": 2048
    }

    request_body = json.dumps(native_request)

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=request_body,
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response['body'].read())
        return response_body.get('generation')

    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return None

# Example usage
if __name__ == "__main__":
    output = call_llama3_1_aws("Which Model are you?")
    if output:
        print("Model Response:", output)
