from langchain.prompts import PromptTemplate
import yaml
from src.config import config_path
class Extractor:
    def __init__(self, llm):
        self.llm = llm
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            extract_template = config["templates"]["extract"]
        self.template = PromptTemplate(input_variables=["query"], 
                        template = extract_template)
    
    def add_features(self, query):
        features = self.llm.predict(self.template.format(query=query))
        query += f'\nТеги: {features}'
        
        return query
