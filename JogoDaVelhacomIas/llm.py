from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field
from langchain_core.messages import SystemMessage
#classe para output structure 
class OStructure(BaseModel):
    pos:int  = Field(ge=0, le=8,description="pos for inserting your move in a 0-indexed grid,any number value means the pos is free")
    
def load_llm(model:str = "qwen3:4b-instruct"):
    try : 
        llm = init_chat_model(model=model,model_provider="ollama") 
        sllm = llm.with_structured_output(OStructure)
        return sllm
     
    except Exception as e :
        raise RuntimeError(f"Erro : {e}")
    


    