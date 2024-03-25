from src.app.loader import llm
from langchain.prompts import PromptTemplate

a = llm.stream('Что такое борщ?')
print(list(a))