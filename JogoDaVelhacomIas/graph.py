from langchain.chat_models import BaseChatModel
from langgraph.graph import StateGraph
from typing import TypedDict,Literal
import os
from .utils import checkWinner,winMessage


class State(TypedDict):
    board: list[str]
    status: Literal["o","x"]
    llm1: BaseChatModel
    llm2: BaseChatModel

# Prompt para as jogadas
# (USADO PQ EU ACHO QUE SO ASSIM PARA ELE SABER JNHAJAKDSJDSJA)
# apesar que sepa eu podia colocar na description do field,mas ne
SYSTEMPROMPTFORX = "youre playing tic-tac-toe as X, the board is show in a flat 0-8 indexed array of strings"
SYSTEMPROMPTFORO = "youre playing tic-tac-toe as O, the board is show in a flat 0-8 indexed array of strings"

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
            raise RuntimeError(" TjU NAO SABE ESCOLHER UM MODELO CERTO NAMORAL KJOKAOLPAKPLASKAKAPLAKAK")
    return output

def configure(state:State) -> State :
    print("> config")
    models = GetModels()
    #models retorna {"llm1" : modelo} entao deve funcionar :p bleh 
    #NAO FUNCIONARIA PQ GETATTR serve para atributos em tempo de execucao
    #agora com get ele vai checar se tem essa chave no dicionario
    if models.get("llm1") and models.get("llm2") : 
        return models
    raise RuntimeError("Erro em configure")

def checkWin(state:State) -> Literal["__end__", "O","X"]:
    status = state["status"]
    if 0 not in state["board"]:
        return "__end__"
    winner = checkWinner(state["board"])
    if not winner:
        return "O" if status == "X" else "X"
    winMessage(winner)
    return "__end__"
    
        
    
    
        
        
    
    


            
    

    
    