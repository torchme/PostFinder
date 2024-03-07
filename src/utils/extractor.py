from langchain.prompts import PromptTemplate


class Extractor:
    def __init__(self, llm):
        self.llm = llm
        self.template = PromptTemplate(input_variables=["query"], 
        template=
        '''Write the tags for the query below:
            ----------------------------------------
            Query: "{query}"
            ----------------------------------------
            Instruction:
            1) You must use language as in original query
            2) Do not duplicate the query in your response. 
            3) Do not use words from original query in your response, your tags must be new and unique
            4) Write the tags in the order of relevance, separated by commas, without any other characters.

            Examples:
            Query: 'Какой рецепт борща?'
            Answer: 'Кулинария, суп' 

            Query: 'Кто создал ChatGPT?' 
            Answer: 'AI, OpenAI, LLM' 

            Query: 'Что такое МЛ симулятор?'
            Answer: 'Машинное обучение, искусственный интеллект' ''')
    
    def add_features(self, query):
        features = self.llm.predict(self.template.format(query=query))
        query += f'\nТеги: {features}'
        
        return query
