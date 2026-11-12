"""
Lesson 10 Extension: Amazon Bedrock Provider Integration
Demonstrates calling Foundation Models (Claude 3.5 Sonnet / Llama 3) via boto3 and LiteLLM.
"""

import os

def call_bedrock_via_boto3():
    """Calls Amazon Bedrock using the official AWS SDK (boto3) Converse API."""
    try:
        import boto3
        # Initialize bedrock runtime client
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
        
        # Bedrock Converse API standardizes chat across Claude, Llama 3, Titan, and Mistral
        response = client.converse(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[
                {"role": "user", "content": [{"text": "Summarize the benefit of Amazon Bedrock for enterprise AI."}]}
            ],
            inferenceConfig={
                "maxTokens": 150,
                "temperature": 0.2
            }
        )
        print("Boto3 Bedrock Response:")
        print(response["output"]["message"]["content"][0]["text"])
    except Exception as e:
        print("Note: AWS credentials not configured or Bedrock access pending:", e)

def call_bedrock_via_litellm():
    """Calls Amazon Bedrock seamlessly through LiteLLM (unified provider abstraction)."""
    try:
        import litellm
        
        # LiteLLM automatically maps 'bedrock/<modelId>' using AWS credentials
        response = litellm.completion(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[
                {"role": "user", "content": "What is the difference between RAG and Fine-tuning?"}
            ]
        )
        print("\nLiteLLM Bedrock Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("Note: LiteLLM Bedrock execution requires AWS credentials:", e)

if __name__ == "__main__":
    print("Testing Amazon Bedrock integration patterns...")
    call_bedrock_via_boto3()
    call_bedrock_via_litellm()
