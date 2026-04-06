from langgraph.graph import StateGraph, END
from chatbot import call, response
from state import State
from util import S_M
from rich import print
from llm import llm

model = llm.model

def call_llm(state: State):
    result = call(state)
    if result == "__end__":
        return END
    return {"messages": [result]}

def response_llm(state: State):
    res = response(state)
    return {"messages": [res]}

builder = StateGraph(State)
builder.add_node("call_llm", call_llm)
builder.add_node("response_llm", response_llm)
builder.set_entry_point("call_llm")
builder.add_edge("call_llm", "response_llm")
builder.set_finish_point("response_llm")

graph = builder.compile()
print(f"[bold blue]--------{str(model).upper()}--------[/bold blue]\n")
print(graph.invoke({"messages": [S_M]}))
