from langgraph.graph.state import RunnableConfig
from graph import graphBuilder
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage
import os
from rich import print

#Definir config

SystemPrompt = "you are a helpful assistant"

def main():
    graph = graphBuilder()
    all_messages: list[BaseMessage] = []
    while True:
        user_prompt = input("Diga A Pergunta Para O Modelo : ")
        if user_prompt in ["q","break","quit"]:
            os.system("clear")
        model_choice = int(input('''
        1- Qwen4b
        2- llama3.2:3b\n'''))
        model_used = None
        
        match model_choice:
            case 1:
                model_used = "qwen3:4b-instruct"
            case 2:
                model_used = "qwen2.5-coder:3b"
            case _:
                raise RuntimeError("erro na escolha de modelo")
        
        config = RunnableConfig(
            run_name="my graph",
            configurable={"thread_id" : 1,"model_used" :model_used}
        )
        
        human_message = HumanMessage(user_prompt)
        current_loop_messages = [human_message]
        if not all_messages:
            current_loop_messages.insert(0, SystemMessage(SystemPrompt))
        
        result = graph.invoke({"messages" : current_loop_messages}, config=config)
        print("*" * 30)
        print("AI RESPONSE : ", result["messages"][-1])
        print("*" * 30)
        all_messages = result["messages"]
        
if __name__ == "__main__":
    main()
        
        
        
        
        