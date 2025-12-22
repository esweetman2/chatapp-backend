from abc import ABC, abstractmethod
import json
import tiktoken

class ContextStrategy(ABC):
    @abstractmethod
    def manage_context_window(self,llm_model_details: dict, total_tokens: int):
        pass

class LLMContextStrategy(ABC):
    def get_llm_model_details(self, model_id: int):
        pass

class LLMModelTokensUsage(ABC):
    @abstractmethod
    def get_tokens_used(self, messages: list):
        pass

class GetLLMModelDetails(LLMContextStrategy):
    def __init__(self, db):
        self.db = db

    def get_llm_model_details(self, model_id: int):
        llm_model_details = self.db.get_model(model_id)
        return llm_model_details

class LLMModelTokens(LLMModelTokensUsage):

    def get_tokens_used(messages: list, agent_model: str):
        try:
            encoding = tiktoken.encoding_for_model(agent_model)
            token_ids = encoding.encode(json.dumps(messages))
            return len(token_ids)
        except:
            return 0

class ManageContextWindow(ContextStrategy):

    def manage_context_window( llm_model_details: dict, total_tokens: int):
        output_tokens = llm_model_details.output_tokens
        context_window = llm_model_details.context_window

        threshold = context_window - output_tokens

        if total_tokens > threshold:
            return True
        return False
    

class ContextWindowFactory:
    def __init__(self, db):
        self.db = db

    def context_window_checker(self, model_id:int, messages: list, agent_model: str):

        llm_details = GetLLMModelDetails(db=self.db).get_llm_model_details(model_id=model_id)

        total_tokens = LLMModelTokens.get_tokens_used(messages=messages, agent_model=agent_model)

        context_window_check = ManageContextWindow.manage_context_window(llm_model_details=llm_details, total_tokens=total_tokens)
        return context_window_check
