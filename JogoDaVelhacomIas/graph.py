
from langgraph.graph import StateGraph, add_messages
from typing import  TypedDict,Literal

from langchain_core.messages import SystemMessage
from llm import load_llm
from utils import checkWinner, countMove,winMessage,validMove,checkTie, EMPTY
import os


class State(TypedDict):
    board: list[str]
    llm1: str
    llm2: str

# Prompt para as jogadas
# (USADO PQ EU ACHO QUE SO ASSIM PARA ELE SABER JNHAJAKDSJDSJA)
# apesar que sepa eu podia colocar na description do field,mas ne
SYSTEMPROMPTFORX = (
    "You are playing tic-tac-toe as X. The board has 9 cells indexed 0 to 8, "
    "shown as index:value, where '.' means a free cell. "
    "Reply with the index of a FREE cell. Never pick a cell that has X or O."
)

SYSTEMPROMPTFORO = (
    "You are playing tic-tac-toe as O. The board has 9 cells indexed 0 to 8, "
    "shown as index:value, where '.' means a free cell. "
    "Reply with the index of a FREE cell. Never pick a cell that has X or O."
)


def boardText(board: list[str]) -> str:
    """Renderiza o tabuleiro com indice e lista as casas livres."""
    linhas = [
        " ".join(f"{i}:{board[i]}" for i in range(linha * 3, linha * 3 + 3))
        for linha in range(3)
    ]
    livres = ", ".join(str(i) for i, casa in enumerate(board) if casa == EMPTY)
    return "\n".join(linhas) + "\nfree cells: " + livres

#funcao para pegar os modelos
def GetModels():
    l1 = input("Qual vai ser a primeira ia?\n1-Qwen3:4b 2-Ollama3.2:3b\n")\
        
    output = {}
    match l1:
        case "1":
            output["llm1"] = "qwen3:4b-instruct"
            os.system("clear")
        case "2":
            output["llm1"] = "llama3.2:3b"
            os.system("clear")
        case _:
            raise RuntimeError(" TU NAO SABE ESCOLHER UM MODELO CERTO NAMORAL KJOKAOLPAKPLASKAKAPLAKAK")
    l2 = input("Qual vai ser a segunda ia ia?\n1-Qwen3:4b 2-Ollama3.2:3b\n")
    match l2:
        case "1":
            output["llm2"] = "qwen3:4b-instruct"
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


def printBoard(state:State) -> State:
    board = state["board"]
        
    os.system('clear')
    print("".join(board[:3]))
    print("".join(board[3:6]))
    print("".join(board[6:]))
    
    return {}


def Router(state:State) -> Literal["__end__", "oturn","xturn"]:
    
    board = state["board"]
    
    winner = checkWinner(board)
    if winner is not None:
        winMessage(winner)
        return "__end__"
    
    if checkTie(board):
        return "__end__"
    
    return "xturn" if countMove(state["board"]) % 2 == 0 else "oturn"

    
def oTurn(state:State) -> State:
    print("o > ")
    grid = state["board"]
    
    message = []
    message.append(SystemMessage(SYSTEMPROMPTFORO))
    message.append(boardText(grid))
    
    
    response = load_llm(state["llm1"]).invoke(message)
    pos = response.pos
    try : 
        if validMove(grid,pos) :
            grid[pos] = "O"
            print("opos > ", pos)
            return {"board" : grid}
        print("invalido")
    except Exception as e:
        raise RuntimeError("Erro na chamada O TURN") from e


def xTurn(state:State) -> State:
    print("x > ")
    grid = state["board"]
    
    message = []
    message.append(SystemMessage(SYSTEMPROMPTFORX))
    message.append(boardText(grid))
    
    response = load_llm(state["llm2"]).invoke(message)
    pos = response.pos
    try : 
        if validMove(grid,pos):
            grid[pos] = "X"
            print("xpos > ",pos)
            return {"board" : grid}
        print("invalido")
    except Exception as e:
        raise RuntimeError("Erro na chamada X TURN") from e


def buildGraph():
    build = StateGraph(State)
    
    build.add_node("configure", configure)
    build.add_node("oturn", oTurn)
    build.add_node("xturn", xTurn)
    build.add_node("printboard", printBoard)
    
    build.add_edge("__start__","configure")
    build.add_edge("configure","printboard")
    build.add_conditional_edges("printboard",Router,["oturn","xturn","__end__"])
    build.add_edge("xturn","printboard")
    build.add_edge("oturn","printboard")     
    graph = build.compile()
    return graph
    
    
    
    
    
    
    
    
        
    
    
        
        
    
    


            
    

    
    