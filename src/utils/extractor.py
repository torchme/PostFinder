from langchain.prompts import PromptTemplate
from src.config import config


class Extractor:
    def __init__(self, llm):
        self.llm = llm
        extract_template = config.get(['templates', 'extract'])
        self.template = PromptTemplate(
            input_variables=["query"], template=extract_template
        )

    def add_features(self, query):
        features = self.llm.predict(self.template.format(query=query))
        query += f"\nТеги: {features}"

        return query
