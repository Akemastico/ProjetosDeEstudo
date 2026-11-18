from time import sleep
import sys

EMPTY = "."

# CHECA SE TEM ALGUMA POSICAO GANHADORA E RETORNA O VALOR
def checkWinner(grid:list[str]) -> str | None:
    wpos = ((0,1,2),(3,4,5),(6,7,8),  (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))
    for a,b,c in wpos:
        if grid[a] == grid[b] == grid[c] != EMPTY:
            return grid[a]
        
    return None


def winMessage(win:str):
    mes = f"PARABENS {win.upper()} VOCE GANHOU KAKAKAKAKA"
    for i in mes:
        sleep(0.1)
        print(i,end="",flush=True)
        
        
def validMove(grid:list[str],pos:int):
    if not 0 <= pos <= 8:
        return False
    return grid[pos] == EMPTY


def checkTie(grid:list[str]):
    print(grid)
    if not EMPTY in grid:
        mes = "O JOGO EMPATOU ! ! ! ! ! ! ! ! ! !"
        for i in mes:
            print(i,end=" ",flush=True)
        return True
    return False


def countMove(board:list[str]):
    n = len([i for i in board if i in ["O", "X"]])
    return n