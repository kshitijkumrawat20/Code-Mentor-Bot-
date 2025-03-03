from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class QwenCoderModel:
    def __init__(self):
        self.llm = ChatOllama(model="qwen2.5-coder:0.5b")
        

    def generate_code(self, input: str) -> str:
        hi = self.llm.invoke("hi")
        print(hi)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant which is a pro coder."),
                ("human", "{Input}"),
            ]
        )

        chain = prompt | self.llm  

        response = chain.invoke(
            {
                "Input": input, 
            }
        )

        return response  
    
    
