from ai_layer.models import Embeddings

import os
import chromadb

from langchain_community.vectorstores import Chroma

INDEX_NAME='Imagedata'
METADATA_KEYS=['sku']

def IndexName():
    return  INDEX_NAME

def MetadataKeys():
    return  METADATA_KEYS

class VectorStoreClient(object):
    def __new__(cls, **kwargs):

        client = chromadb.HttpClient( host=os.getenv("VS_URL"))

        return client

class VectorStore(object):
    def __new__(cls, collection_name: str, **kwargs):

        return Chroma(client=VectorStoreClient(), collection_name=collection_name, embedding_function=Embeddings(),**kwargs)

class MakeCollection(object):
    def __new__(cls, collection_name: str, description: str = 'Default class description'):
        client = VectorStoreClient()

        collections = client.list_collections()
        for coll in collections:
            if coll["name"] == collection_name:
                client.delete_collection(collection_name)

        client.create_collection(collection_name)

        return True

def make_collection(collection_name: str, description: str = 'Default class description'):

    client = VectorStoreClient()

    ############################################################
    # TODO:
    # Change to match the native vectorstore logic for creating a
    # collection.

    try:
        collections = client.list_collections()
        for coll in collections:
            if coll["name"] == collection_name:
                client.delete_collection(collection_name)

        client.create_collection(collection_name)
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
            collections = client.list_collections()
            for coll in collections:
                if coll["name"] == collection_name:
                    client.delete_collection(collection_name)
            response = True
        except:
            response = False

        return response