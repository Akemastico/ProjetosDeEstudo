from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field

#classe para output structure 
class OStructure(BaseModel):
    pos:int  = Field(ge=0, le=8)
    description:str = Field(description="a small reason for the move")
    
def load_llm(model:str = "qwen3:4b-instruct"):
    try : 
        llm = init_chat_model(model=model,model_provider="ollama") 
        sllm = llm.with_structured_output(OStructure)
        return sllm
     
    except Exception as e :
        raise RuntimeError(f"Erro : {e}")
    
    
    