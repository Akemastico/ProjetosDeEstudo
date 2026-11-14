
from langchain.tools import tool,BaseTool

@tool
def soma(a:float,b:float):
    '''
    A FUNCTION THAT RETURN THE SUM OF TWO NUMBERS
    
    ARGS:
    A: FLOAT
    B: FLOAT'''
    return a+b

@tool
def subtracao(a:float,b:float):
    '''
        A FUNCTION THAT RETURN THE SUBTRACTION OF TWO NUMBERS
        
        ARGS:
        A: FLOAT
        B: FLOAT'''
    return a-b

@tool
def multiply(a:float,b:float):
    '''
            A FUNCTION THAT RETURN THE MULTIPLICATION OF TWO NUMBERS
            
            ARGS:
            A: FLOAT
            B: FLOAT'''
    return a*b

@tool
def division(a:float,b:float):
    '''
            A FUNCTION THAT RETURN THE DIVISION OF TWO NUMBERS
            B CANT BE 0 
            ARGS:
            A: FLOAT
            B: FLOAT'''
    if b == 0:
        raise ZeroDivisionError("Nao e possivel dividir por zero")
    return a/b

tools:list[BaseTool] = [soma,subtracao,multiply,division]
tools_by_name = {tool.name:tool for tool in tools}


    
      
     