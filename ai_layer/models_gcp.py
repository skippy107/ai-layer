from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import  ChatPromptTemplate
from langchain_google_vertexai import VertexAI, ChatVertexAI, VertexAIEmbeddings

from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel

import os
import base64

# vars for google platform
project_id = os.getenv('GOOGLE_PROJECT_ID')
region = os.getenv('GOOGLE_REGION')

aiplatform.init(project=f"{project_id}", location=f"{region}")

class LLM(object):
    def __new__(cls, **kwargs):
        return VertexAI(**kwargs, model_name=os.getenv('COMPLETION_MODEL'))

class ChatLLM(object):
    def __new__(cls, **kwargs):
        return ChatVertexAI(**kwargs, model_name=os.getenv('CHAT_MODEL'))

class Embeddings(object):
    def __new__(cls, **kwargs):
        return VertexAIEmbeddings(**kwargs, model_name=os.getenv('EMBEDDING_MODEL'))

class VisionLLM(object):
    def __new__(cls, **kwargs):
        return ChatVertexAI(**kwargs,  model_name=os.getenv('VISION_MODEL'))

def generate_image(prompt):

    generation_model = ImageGenerationModel.from_pretrained(os.getenv('IMAGE_GEN_MODEL'))

    response = generation_model.generate_images(prompt=prompt)

    return response.images[0]

def view_image(url:str,system_message:str=None,prompt:str=None):

    model = VisionLLM()

    if system_message is None:
        system_message = "You are a helpful assistant who specializes in analysing images."
    
    if prompt is None:
        prompt = "Describe the object pictured in as much detail as possible."

    if url.lower().startswith('http'):
        # url is a URL
        image_data = url

    else:
        # url is a file path
        file_type = url.lower().split('.')[-1]
        image_data = f"data:image/{file_type};base64,{encode_image(url)}"

    prompt = ChatPromptTemplate.from_messages([
        # SystemMessage( content=( system_message )),
        HumanMessage(content=[{
                    "type": "text", 
                    "text": system_message + '\n\n' + prompt 
                },
                {
                    "type": "image_url",
                    "image_url": {
                        # can be URL or base64 encoded string
                        # data:image/png;base64,abcd124
                        "url": image_data, 
                        "detail": "auto",
                    },
                }])
    ])

    chain = prompt | model

    response = chain.invoke({"input":url})

    return response


# Pass the image data to an encoding function.
def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string