from typing import Annotated, Literal,TypedDict,Sequence,List
from langchain import messages
from langgraph.graph import START,END,StateGraph, add_messages
from langgraph.graph.message import BaseMessage
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,ToolCall
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import RunnableConfig
from rich import print
from tools import tools,tools_by_name


llm = init_chat_model("ollama:llama3.2:3b")

# Definir AgentState 

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    tools_used: list[ToolCall]
    
def node_a(state:AgentState) -> AgentState:
    try:
        llmTools = llm.bind_tools(tools)
        response = llmTools.invoke(state["messages"])
        if isinstance(response,AIMessage) and getattr(response,"tool_calls"):
            call = response.tool_calls[-1]
            return {"tools_used" : call}
        else :
            return {"messages" : response.content}
    except Exception as e:
        raise RuntimeError("Erro Node A") from e
    
def node_b_conditional(state:AgentState) -> Literal["a","c"]:
    calls = state["tools_used"]
    if calls:
        item = calls[0]
        name,args,id = item["name"],item["args"],item["id"]
        
        try : 
            res
    
     
    
    
    

    

