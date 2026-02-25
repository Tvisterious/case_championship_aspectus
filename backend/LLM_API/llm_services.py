'''ЗДЕСЬ БУДУТ ОБЩИЕ ФУНКЦИИ ДЛЯ РАБОТЫ LLM И ФУНКЦИИ ПОИСКА В СЕТИ'''

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#Настройка API
client = OpenAI(
  base_url="https://api.proxyapi.ru/openai/v1",
  api_key=os.getenv('NEURO_API'),
)

#ИИ + Подключение к интернет-источникам
def LLM_WEB(question:str)->str:
    responses = client.responses.create(
        model=os.getenv ('LLM_TYPE'),
        tools=[{
        "type": "web_search",
        "search_context_size": "low",
        "user_location": {
            "type": "approximate",
            "country": "RU",
            "city": "Moscow",
            "region": "Moscow"
        }
    }],
    input=question
    )
    return(responses.output_text)

#Просто ИИ без возможности подключаться к сети (для тестов)
def LLM(question:str)->str:
    responses = client.responses.create(
        model="gpt-4.1", 
        input=question
    )
    return(responses.output_text)