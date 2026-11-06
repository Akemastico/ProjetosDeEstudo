from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage,AIMessage,ToolMessage
from typing import Literal,Annotated,Sequence,TypedDict
from langgraph.graph import add_messages
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.constants import START,END
from langgraph.checkpoint.memory import InMemorySaver
from tools import tools,tools_by_name

# Definir o agento stato!!!!

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]
   
# funcao para retornar llm ja com tools

def load_llm():
    try : 
        llm = init_chat_model(
    model="qwen3:4b-instruct",
    model_provider="ollama",
    base_url="http://127.0.0.1:11434",
    temperature=0.2,
    reasoning=False,
)
        llm_with_tools = llm.bind_tools(tools)
        return llm_with_tools
    except Exception as e:
        raise RuntimeError("Erro ao carregar llm") from e 
        
# Mensagem para a ia (PODE CHAMAR TOOLS)
    
def node_a(state:AgentState) -> AgentState:
    print("> call")
    response = load_llm().invoke(state["messages"])
    return {"messages" : [response]}

# Tool Node para caso a ia chame    

def tool_node(state:AgentState) -> AgentState:
    print("tool > ")
    last_message = state["messages"][-1]
    if not isinstance(last_message,AIMessage) or not getattr(last_message,"tool_calls",None):
        return state
    call = last_message.tool_calls[-1]
    name,id,args = call["name"],call["id"],call["args"]
    try :
        content = tools_by_name[name].invoke(args)
    except (KeyError, IndexError, TypeError,ValueError) as error:
        content = f"Please, fix your mistakes: {error}"
    tool_message = ToolMessage(content,tool_call_id=id)
    return {"messages": [tool_message]}
    
#definir router para caso exista uma chamada tool

def router(state:AgentState) -> Literal["__end__","tool"]:
    print("> router")
    llm_response = state["messages"][-1]
    
    if getattr(llm_response,"tool_calls",None):
        return "tool"
    return "__end__"

def graphBuilder() -> CompiledStateGraph[AgentState,None,AgentState,AgentState]:
    
    checkpointer = InMemorySaver()
    
    builder = StateGraph(AgentState)
    builder.add_node("a", node_a)
    builder.add_node("tool", tool_node)
    builder.add_node("router", router)

    builder.add_edge(START,"a")
    builder.add_conditional_edges("a",router,["tool",END])
    builder.add_edge("tool", "a")
    graph = builder.compile(checkpointer=checkpointer)
    return graph