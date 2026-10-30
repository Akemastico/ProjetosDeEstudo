import os
import requests
from dotenv import load_dotenv
from ollama import chat

load_dotenv()
url = "http://api.weatherapi.com/v1/current.json"
key = os.environ.get('WEATHERAPIKEY')
model = "qwen2.5-coder:3b"


def getWeather(city: str):    
    response = requests.get(url, params={"key": key, "q": city})
    response.raise_for_status()
    data = response.json()['current']['temp_c']
    return f'Temperatura Atual em {city}: {data}°C'


weather_tool = {
    'type': 'function',
    'function': {
        'name': 'getWeather',
        'description': 'use it when the user wants a specific city current temperature in celsius',
        'parameters': {
            'type': 'object',
            'properties': {
                'city': {'type': 'string', 'description': 'the city name'},
            },
            'required': ['city'],
        },
    },
}

available_tools = {
    'getWeather': getWeather
}

def askllm(question: str):
    message = [{"role": "user", "content": question}]
    
    response = chat(model=model, messages=message, tools=[weather_tool])
    
   
    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            function_name = tool.function.name
            arguments = tool.function.arguments
            
            func_exec = available_tools[function_name]
            result = func_exec(**arguments)
            
            message.append(response.message)
            message.append({
                'role': 'tool',
                'content': str(result)  
            })
            
            
            final_response = chat(model=model, messages=message)
            return final_response.message.content

    return response.message.content


print(askllm("bom dia"))