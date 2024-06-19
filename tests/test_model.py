from ai_layer import LLM, ChatLLM
from langchain_core.messages import HumanMessage, SystemMessage

from langchain.globals import set_verbose, set_debug

# instantiate the LLMs
llm = LLM(temperature=0)
chat_llm = ChatLLM(temperature=0)

print(llm.invoke('tell me a joke'))

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content="What is the purpose of model regularization?"),
]

response = chat_llm.invoke(messages)

print(response.content)