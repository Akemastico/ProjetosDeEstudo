import sqlite3 as sql
from langchain.tools import BaseTool,tool



def connection_pool():
    try :
        conn = sql.connect("/home/akemistico/Documentos/ProjetosDeEstudo/nodes/test3/database.db")
        conn.row_factory = sql.Row
        return conn
    except Exception as e:
        raise RuntimeError("Erro conexao com o banco")    
@tool    
def get_richest_people():
    conn = connection_pool()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT nome, rendabruta FROM pessoas "
            "ORDER BY rendabruta DESC LIMIT 10"
        )
        results = [(item["nome"],item["rendabruta"]) for item in cursor.fetchall()]
        return results
    except Exception as e:
        return e
    finally:
        conn.close()

@tool        
def get_oldest_people():
    conn = connection_pool()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT nome, idade FROM pessoas "
            "ORDER BY idade DESC LIMIT 10"
        )
        results = [(item["nome"],item["idade"]) for item in cursor.fetchall()]
        return results
    except Exception as e:
        return e
    finally:
        conn.close()
        
        
tools:list[BaseTool] = [get_oldest_people,get_richest_people]
tools_by_name = {tool.name:tool for tool in tools}

