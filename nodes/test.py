
from typing import Annotated, Any, Literal, TypedDict,Sequence
from langchain_ollama import ChatOllama
from langgraph.graph import START, StateGraph, add_messages
from langgraph.graph.message import BaseMessage
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import RunnableConfig
from rich.markdown import Markdown

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    prompt: str
    answer: str
    
    
llm = ChatOllama(model="llama3.2:3b",keep_alive="30m")

def node_a(state: AgentState) -> AgentState:
    #CRIAR PROMPT
    global llm
    prompt = state["prompt"]
    try : 
        response = llm.invoke(prompt)
        ai_response = AIMessage(response.content)
        return {"answer" : response.content, "messages" : ai_response}
    except Exception:
        raise RuntimeError("Erro ao Responder a mensagem") from Exception

def node_b(state: AgentState) -> Literal["a","c"]:
    #AVALIACAO PROMPT
    global llm
    
    system_message = SystemMessage("you are a answer validator, answer with only YES OR NO followed by a explanation in this format, YES, its a good answer . NO, its not a good answer . YES or NO always in capital")
    context = [system_message]
    prompt = HumanMessage(state["answer"])
    context.append(prompt)
    try : 
        response = llm.invoke(context)
        if "YES" in response.content:
            print("Prompt Aprovado")
            return "c"
        elif "NO" in response.content:
            print("Prompt Recusado")
            return "a"
        else :
            raise RuntimeError("IA NAO RESPONDEU CERTO JESUISE")
        
    except Exception:
        raise RuntimeError("Erro na avaliacao da resposta")

def node_c(state:AgentState) -> AgentState :
    prompt = HumanMessage(state["prompt"])
    return {"messages" : prompt}

checkpointer = InMemorySaver()
builder = StateGraph(AgentState)

builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_node("c", node_c)

builder.add_edge(START,"a")
builder.add_conditional_edges("a", node_b,["a", "c"])
builder.add_edge("c", "__end__")

graph = builder.compile(checkpointer=checkpointer)
config = RunnableConfig(configurable={"thread_id" : 1})

if __name__ == "__main__":
    while True:
        user_input = input("Diga Alguma Pergunta para a IA : ")
        if user_input in ["quit","q","end","exit"] : break
        
        result = graph.invoke({"prompt" : user_input},config=config)
        context = result["messages"]
        print("*" * 30)
        print(context)
        print("*" * 30)
        print(f"RESPOSTA IA = {result["answer"]}")
        
        
        
        
    
    


    
    
    
    
    
            
        
    
    
           
    
    
    
    