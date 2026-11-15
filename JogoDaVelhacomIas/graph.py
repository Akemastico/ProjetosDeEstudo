from langchain.chat_models import BaseChatModel
from langgraph.graph import StateGraph
from typing import TypedDict,Literal
import os

class State(TypedDict):
    board: list[str]
    status: Literal["tied","o","x"]
    llm1: BaseChatModel
    llm2: BaseChatModel

#funcao para pegar os modelos

def GetModels():
    l1 = input("Qual vai ser a primeira ia?\n1-Qwen3:4b 2-Ollama3.2:3b")\
        
    output = {}
    match l1:
        case "1":
            output["llm1"] = "qwen3:4b"
            os.system("clear")
        case "2":
            output["llm1"] = "llama3.2:3b"
            os.system("clear")
        case _:
            raise RuntimeError(" TU NAO SABE ESCOLHER UM MODELO CERTO NAMORAL KJOKAOLPAKPLASKAKAPLAKAK")
    l2 = input("Qual vai ser a segunda ia ia?\n1-Qwen3:4b 2-Ollama3.2:3b")
    match l2:
        case "1":
            output["llm2"] = "qwen3:4b"
            os.system("clear")
        case "2":
            output["llm2"] = "llama3.2:3b"
            os.system("clear")
        case _:
            raise RuntimeError(" TU NAO SABE ESCOLHER UM MODELO CERTO NAMORAL KJOKAOLPAKPLASKAKAPLAKAK")
    return output

def configure(state:State) -> State :
    print("> config")
    models = GetModels()
    #models retorna {"llm1" : modelo} entao deve funcionar :p bleh
    if getattr(models,"llm1") and getattr(models,"llm2") : 
        return models
    raise RuntimeError("Erro em configure")

def call_llm(state:State) -> State:
    ...
    


            
    

    
    