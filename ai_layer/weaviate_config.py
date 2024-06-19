import os

def config_provider(provider:str):
    #  create headers, vectorizers and generators

    # possible vectorizers are text2vec-openai, text2vec-aws, text2vec-palm, text2vec-cohere
    # see implementation details for each one here - https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules

    # possible generators (inference) are generative-openai, generative-aws, generative-cohere, generative-palm"
    # see implemenation details for each one here -https://weaviate.io/developers/weaviate/modules/reader-generator-modules

    additional_headers = {}
    module_config = {}
    vectorizer = ""

    if provider.lower() == "google":
        additional_headers={"X-Google-Vertex-Api-Key": os.getenv("VERTEX_API_KEY")}
        # for non vertex use this instead
        # additional_headers={"X-Google-Studio-Api-Key": os.getenv("STUDIO_API_KEY")}
        module_config={ "text2vec-palm": {
                            "projectId": os.getenv("GOOGLE_PROJECT_ID"),    # Only required if using Vertex AI. 
                            "apiEndpoint": os.getenv("GOOGLE_API_ENDPOINT"),# Defaults to "us-central1-aiplatform.googleapis.com".
                            "modelId": os.getenv("EMBEDDING_MODEL"),        # Optional.
                        },
                        "generative-palm":{
                            "projectId": os.getenv("GOOGLE_PROJECT_ID"), 
                            "apiEndpoint": os.getenv("GOOGLE_API_ENDPOINT"), 
                            "modelId": os.getenv("COMPLETION_MODEL")
                        }}
        vectorizer = "text2vec-palm"

    elif provider.lower() == "cohere":
        additional_headers={"X-Cohere-Api-Key": os.getenv("COHERE_API_KEY")}
        module_config={ "text2vec-cohere": {
                            "model": os.getenv("EMBEDDING_MODEL"),
                        },
                        "generative-cohere": {
                            "model": os.getenv("COMPLETION_MODEL"),  # Optional - Defaults to `command-xlarge-nightly`. 
                            # "temperatureProperty":  0.5, # Optional
                            # "maxTokensProperty": 1024,   # Optional
                            # "kProperty": 3,              # Optional
                        }}
        vectorizer = "text2vec-cohere"

    elif provider.lower() == "aws":
        additional_headers={"X-AWS-Access-Key": os.getenv("AWS_ACCESS_KEY")}
        additional_headers={"X-AWS-Secret-Key": os.getenv("AWS_SECRET_KEY")}
        module_config={ "text2vec-aws": {
                            "model": os.getenv("EMBEDDING_MODEL"),   # REQUIRED
                            "region": os.getenv("AWS_REGION")        # REQUIRED
                        },
                        "generative-aws": {
                            "model": os.getenv("COMPLETION_MODEL"),  # REQUIRED
                            "region": os.getenv("AWS_REGION")        # REQUIRED
                        }}
        vectorizer = "text2vec-aws"

    elif provider.lower() == "azure":
        additional_headers={"X-Azure-Api-Key": os.getenv("AZURE_OPENAI_API_KEY")}
        module_config={ "text2vec-openai": {
                            "resourceName": os.getenv("AZURE_RESOURCE"),
                            "deploymentId": os.getenv("EMBEDDING_MODEL"),
                        },
                        "generative-openai": {
                            "resourceName": os.getenv("AZURE_RESOURCE"),
                            "deploymentId": os.getenv("COMPLETION_MODEL"),
                        }}
        vectorizer = "text2vec-openai"

    elif provider.lower() == "openai":
        additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
        module_config={ "text2vec-openai": {
                            "model": os.getenv("EMBEDDING_MODEL"),
                        },
                        "generative-openai": {
                            "model": os.getenv("COMPLETION_MODEL"),  # Optional - Defaults to `command-xlarge-nightly`.
                            # "temperatureProperty":  0.5, # Optional
                            # "maxTokensProperty": 1024,   # Optional
                            # "kProperty": 3,              # Optional
                        }}
        vectorizer = "text2vec-openai"

    else:
        # default to Azure
        additional_headers={"X-Azure-Api-Key": os.getenv("AZURE_OPENAI_API_KEY")}
        module_config={ "text2vec-openai": {
                            "resourceName": os.getenv("AZURE_RESOURCE"),
                            "deploymentId": os.getenv("EMBEDDING_MODEL"),
                        },
                        "generative-openai": {
                            "resourceName": os.getenv("AZURE_RESOURCE"),
                            "deploymentId": os.getenv("COMPLETION_MODEL"),
                        }}
        vectorizer = "text2vec-openai"

    return vectorizer, module_config, additional_headers