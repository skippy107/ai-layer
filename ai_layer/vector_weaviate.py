from ai_layer.models import Embeddings
from weaviate_config import config_provider

import os
############################################################
# TODO:
# Change to match the vectorstore you want to use. Be sure to
# import the native module as well as the matching LangChain
# module

import weaviate
from langchain_community.vectorstores import Weaviate

############################################################
# TODO:
# Choose a provider for embedding and inference

PROVIDER = "OPENAI" # or "AZURE" or "AWS" or "COHERE" or "GOOGLE"

############################################################
# TODO:
# Change this function in <vectorstore>_config.py to do any setup for your vectorstore
# provider that may be required.  <vectorstore> = weaviate, qdrant, pinecone, chroma, etc.

vectorizer, module_config, additional_headers = config_provider(PROVIDER)

class VectorStoreClient(object):
    def __new__(cls, **kwargs):
        '''
        This is the default VectorStoreClient class. It will return an instance of a native vectorstore client.  The default vector store is Weaviate.
        
        '''
        ############################################################
        # TODO:
        # Return the client for your vectorstore. 
        return weaviate.Client(url=os.getenv('VS_URL'), additional_headers=additional_headers, **kwargs)

class VectorStore(object):
    def __new__(cls, collection_name: str, **kwargs):
        '''
        This is the default VectorStore class. It will return an instance of a LangChain vectorstore.  The default vector store is Weaviate.
        
        The only required argument is `collection_name` which must already exist.

        Optionally you can provide `attributes` in the form of a list of strings.  These will be used to surface metadata when querying the vectorstore. If you omit the `attributes` list then all search results will have no metadata, even if the metatdata is present on the vector.

        Example with attributes:

        VectorStore(VectorStoreClient(), collection_name, 'text', Embeddings(), attributes=['sku'])

        
        Use MakeCollection to create an empty vector collection.
        
        '''
        ############################################################
        # TODO:
        # Change to match the vectorstore you want to use. note this 
        # is a LangChain class and not a native class.

        return Weaviate(VectorStoreClient(), collection_name, 'text', Embeddings(),**kwargs)

class CollectionClass(object):
    def __new__(cls, collection_name: str, description: str = 'Default class description'):
        '''
        This class generates an object needed by Weaviate to create new collections. 
        
        The only required argument is `collection_name`.
        '''
        this_class =  {   
            "class": collection_name,
            "description": description,
            ############################################################
            # TODO:
            # For Weaviate, set the vector distance function to match your needs

            "vectorIndexConfig": {
                "distance": "cosine",
            },
            "vectorIndexType": "hnsw",
            "vectorizer": vectorizer,
            "moduleConfig": module_config,
            "properties": [
            {
            "name": "text",
            "dataType": ["text"],
            "description": "text content of the document",
            },
            ]

        }

        return this_class

def make_collection(collection_name: str, description: str = 'Default class description'):

    client = VectorStoreClient()

    ############################################################
    # TODO:
    # Change to match the native vectorstore logic for creating a
    # collection.

    this_class = CollectionClass(collection_name, description)

    try:
        if client.schema.exists(collection_name):
            client.schema.delete_class(collection_name)

        client.schema.create_class(this_class)

        response = True
    except:
        response = False

    return response

def drop_collection(collection_name: str):

        client = VectorStoreClient()

        ############################################################
        # TODO:
        # Change to match the native vectorstore logic for deleting a
        # collection.

        try:
            client.collections.delete(collection_name)

            response = True
        except:
            response = False

        return response
