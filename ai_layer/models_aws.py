import os
import json
import boto3
import base64

from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.llms import Bedrock
from langchain_aws import ChatBedrock

class LLM(object):
    def __new__(cls, **kwargs):
        return Bedrock(
            **kwargs, 
            credentials_profile_name=os.getenv("AWS_PROFILE"),  
            region_name=os.getenv("AWS_REGION"),
            model_id=os.getenv('COMPLETION_MODEL')
        )

class ChatLLM(object):
    def __new__(cls, **kwargs):
        return ChatBedrock(
            **kwargs, 
            model_id=os.getenv('CHAT_MODEL'), 
            region_name=os.getenv("AWS_REGION")
        )

class Embeddings(object):
    def __new__(cls, **kwargs):
        return BedrockEmbeddings(
            **kwargs, 
            credentials_profile_name=os.getenv("AWS_PROFILE"), 
            region_name=os.getenv("AWS_REGION"),
            model_id=os.getenv('EMBEDDING_MODEL')
        )

class VisionLLM(object):
    def __new__(cls, **kwargs):
        return ChatBedrock(
            **kwargs, 
            model_id=os.getenv('VISION_MODEL'),
            region_name=os.getenv("AWS_REGION"), 
            max_tokens=2048
        )

def generate_image(prompt:str, seed:int=0)->str:
    bedrock_runtime_client = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_REGION") )

    body = {
        "text_prompts": [{"text": prompt}],
        "seed": seed,
        "cfg_scale": 10,
        "steps": 30,
    }

    # if style_preset:
    #     body["style_preset"] = style_preset

    response = bedrock_runtime_client.invoke_model(
        modelId=os.getenv('IMAGE_MODEL'), body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read())
    base64_image_data = response_body["artifacts"][0]["base64"]

    # Save the generated image to a local folder.
    i, output_dir = 1, "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    while os.path.exists(os.path.join(output_dir, f"stability_{i}.png")):
        i += 1

    image_data = base64.b64decode(base64_image_data)

    image_path = os.path.join(output_dir, f"stability_{i}.png")
    with open(image_path, "wb") as file:
        file.write(image_data)

    return image_path
