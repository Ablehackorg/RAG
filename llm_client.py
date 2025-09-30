import os
import requests
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

class OllamaClient():
    def __init__(self):
        self.base_url = os.getcwd('OLLAMA_BASE_URL')
        self.model = os.getenv('OLLAMA_MODEL')
        self.api_url = f"{self.base_url}/api/generate"

        try:
            self.llm = Ollama(
                model=self.model,
                base_url=self.base_url,
                temperature = 0.7,
                top_p = 0.9,
                )

        except Exception as e:
            print(f"Error with loading llm {e}")
            self.llm = None

        self.rag_promt_template = PromptTemplate(
            input_variables=['question', 'context'],
            template="""
            Your are helpful data analayzer that answers question based on provided context.
            Use the following context to answer the question.
            If the answer cannot be fount in  the context, say so and don't try to make up an anaswer.
            If the context insufficient, mantion that additional information would be helpful.
            
            Context: 
            {context}
            
            Question: {question}
            
            Answer: Based on the provided context"""
        )
    def generate_response(self, question, contxet):
        if not question:
            return 'Please provide a valid question'

        try:
            promt = self.rag_promt_template.format(question=question, contxet=contxet)
            if self.llm is None:
                return 'LLM not initialized properly. Check Ollama!'
            else:
                response = self.llm.invoke(promt)
                if response:
                    return response
                else:
                    return "Sorry, I couldn't generate response. Try again or parapharase you question"

        except Exception as e:
            print(f"Error with generating response {e}")