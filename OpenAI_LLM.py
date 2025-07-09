from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import LLMInterface
class OpenAIWrapper(LLMInterface):
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0.0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

    def ask(self, question: str, context: str) -> str:
        prompt = f"{context}\n\nQuestion: {question}"
        response = self.llm([HumanMessage(content=prompt)])
        return response.content