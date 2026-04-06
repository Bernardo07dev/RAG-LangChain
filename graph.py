from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from chatbot import call, response
from state import State
from util import S_M
from rich import print
from llm import llm, tools

model = llm.model
tool_node = ToolNode(tools)

def call_llm(state: State) -> dict:
    result = call(state)
    if result == "__end__":
        return END
    return {"messages": [result]}

def response_llm(state: State) -> dict:
    res = response(state)
    return {"messages": [res]}

def router(state: State):
    last = state["messages"][-1]

    if getattr(last, "tool_calls", None):
        return "tool_node"
    return "call_llm"

builder = StateGraph(State)
builder.add_node("call_llm", call_llm)
builder.add_node("response_llm", response_llm)
builder.add_node("tool_node", tool_node)
builder.set_entry_point("call_llm")
builder.add_edge("call_llm", "response_llm")
builder.add_edge("tool_node", "response_llm")
builder.add_conditional_edges("response_llm", router, {"tool_node": "tool_node", "call_llm": "call_llm"})

graph = builder.compile()
print(f"[bold blue]--------{str(model).upper()}--------[/bold blue]\n")
graph.invoke({"messages": [S_M]})
