import operator
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
