from abc import ABC, abstractmethod

class SummaryStrategy(ABC):
    @abstractmethod
    def get_summary_agent(self) -> list[str]:
        pass
    def prepare_summary_agent(self, agent, summary):
        pass

class SummaryFactory(SummaryStrategy):
    def __init__(self, db):
        self.db = db

    def get_summary_agent(self):
        agents = self.db.get_agent()

        summarization_agent = None
        for i in agents:
            if i.agent_name == "Summarization Agent":
                summarization_agent = i 

        return summarization_agent.model_dump()
    
    def prepare_summary_agent(self, agent, summary):
        system_message = agent["system_message"]
        agent["system_message"] = f"""{system_message}
You MUST use the existing summary below and the chat historyto generate a new summary that takes into account theexisting summary as well as the message history.

Existing Summary: 
{summary.summary}
"""
        return agent

        