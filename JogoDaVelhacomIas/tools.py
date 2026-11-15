from langchain.tools import tool, BaseTool

@tool 
def JogadaX(pos:int,grid:list):
    ''' X PLAY
        USE THIS IN X TURN
        THE GRID IS A 0-8 INDEX SIMULATING A 3X3 GRID
        
        ARGS:
        pos: INTEGER
    '''
    if grid[pos] in ["X","O"]:
        return "invalid"
    grid[pos] = "X"
    return grid

@tool 
def JogadaO(pos:int,grid:list):
    ''' O PLAY
        USE THIS IN O TURN
        THE GRID IS A 0-8 INDEX SIMULATING A 3X3 GRID
        
        ARGS:
        pos: INTEGER
    '''
    if grid[pos] in ["X","O"]:
        return "invalid"
    grid[pos] = "X"
    return grid


def checkWinner(grid:list[str]):
    wpos = ((0,1,2),(3,4,5),(6,7,8),  (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))
    for a,b,c in wpos:
        if grid[a] == grid[b] == grid[c]:
            return grid[a]
    return 0


tools:list[BaseTool] = [JogadaO,JogadaX]
            


    
    