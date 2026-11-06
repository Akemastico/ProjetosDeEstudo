from langgraph.graph.state import RunnableConfig
from graph import graphBuilder
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage
import os
from rich import print

#Definir config

SystemPrompt = "you are a helpful assistant"


config = RunnableConfig(configurable={"thread_id" : 1})

def main():
    graph = graphBuilder()
    all_messages: list[BaseMessage] = []
    while True:
        user_prompt = input("Diga A Pergunta Para O Modelo : ")
        if user_prompt in ["q","break","quit"]:
            os.system("clear")
        human_message = HumanMessage(user_prompt)
        current_loop_messages = [human_message]
        if not all_messages:
            current_loop_messages.insert(0, SystemMessage(SystemPrompt))
        
        result = graph.invoke({"messages" : current_loop_messages}, config=config)
        print("*" * 30)
        print("AI RESPONSE : ", result["messages"][-1].content)
        print("*" * 30)
        all_messages = result["messages"]
        
if __name__ == "__main__":
    main()
        
        
        
        
        