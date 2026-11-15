from time import sleep

# CHECA SE TEM ALGUMA POSICAO GANHADORA E RETORNA O VALOR
def checkWinner(grid:list[str]):
    wpos = ((0,1,2),(3,4,5),(6,7,8),  (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))
    for a,b,c in wpos:
        if grid[a] == grid[b] == grid[c]:
            return grid[a]
    return 0


def winMessage(win:str):
    mes = f"PARABENS {win.upper()} VOCE GANHOU KAKAKAKAKA"
    for i in mes:
        sleep(0.1)
        print(i,end="",flush=True)
            