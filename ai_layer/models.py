import os
from langchain_openai import ChatOpenAI, AzureOpenAI, AzureChatOpenAI, AzureOpenAIEmbeddings
from openai import AzureOpenAI as AZOpenAI

class LLM(object):
    def __new__(cls, **kwargs):
        return AzureOpenAI(**kwargs, azure_deployment=os.getenv('COMPLETION_MODEL'))

class ChatLLM(object):
    def __new__(cls, **kwargs):
        return AzureChatOpenAI(**kwargs, azure_deployment=os.getenv('CHAT_MODEL'))

class Embeddings(object):
    def __new__(cls, **kwargs):
        return AzureOpenAIEmbeddings(**kwargs, azure_deployment=os.getenv('EMBEDDING_MODEL'))

class VisionLLM(object):
    def __new__(cls, **kwargs):
        return ChatOpenAI(**kwargs, azure_deployment=os.getenv('VISION_MODEL'))

def generate_image(prompt):
    client = AZOpenAI(
        api_version=os.environ["OPENAI_API_VERSION"],  
        api_key=os.environ["AZURE_OPENAI_API_KEY"],  
        azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT']
    )

    result = client.images.generate(
        model=os.environ["IMAGE_MODEL"], # the name of your DALL-E 3 deployment
        prompt=prompt,
        n=1
    )

    return result