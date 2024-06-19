# ai_layer

The AI Layer Template provides a simple way to abstract AI primitives from your chain code.  By including this template in your application you can provide a standard set of primitives that your chain can use such as llm, chat_llm, retriever, sql_db and vectorstore.  This template provides a way to isolate the implementation details of each resource so you can port  your code to different providers more quickly.

## Environment Setup

The models in this layer can be configured to work with AWS, Azure or GCP. The `.env_template` file contains  environment variables which must be present in order for the package to work correctly.

## Usage

To use this package you should have an empty LangServe project created.  You can then use Poetry to install this package as follows:

`poetry add git+https://github.com/skippy107/ai-layer.git`

After adding the package, choose a platform and rename the model file to `models.py`.
