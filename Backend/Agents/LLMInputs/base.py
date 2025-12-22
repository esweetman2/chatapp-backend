from abc import ABC, abstractmethod

class InputsStrategy(ABC):
    @abstractmethod
    def get_inputs(self, prompt: str) -> str:
        pass

class MessagesHistory(InputsStrategy):
    # def __init__(self, db):
    #     self.db = db

    def get_inputs(self, messages) -> str:
        # Implementation for getting inputs with history from Database
        # messages = self.db.get_message(chat_id=chat_id)
        if messages:
            message_list = []
            for message in messages:
                message_list.append({
                    "role": message.role,
                    "content": message.message
                })
            return message_list
        return []

class LLMInputs(InputsStrategy):
    def __init__(self, messages):
        self.messages = messages

    def get_inputs(self, system_message: str, query: str, role: str):
        # print(self.messages)
        inputs = [
            {
                "role": "system", 
                "content": system_message
            },
        ]
        # messages = self._get_message_history()
        for message in self.messages:

            inputs.append({
                "role": message.role,
                "content": message.message,
            })
        inputs.append({
            "role": role,
            "content": query
        })

        return inputs

class SummaryInputs(InputsStrategy):
    def get_inputs(self, inputs, index):
        threshold = -10
        system_message = inputs[0]
        summary_messages = inputs[index:threshold]
        new_index = inputs.index(inputs[index:threshold][-1])
        print(inputs[new_index+1])
        print("new index: ", new_index)
        if index != 0:
            summary_messages.insert(0, system_message)
        # return {"summary_messages":summary_messages, "new_index": new_index}
        return {"summary_messages": summary_messages, "new_index": new_index + 1}

class LLMInputsFactory:
    def __init__(self, db):
        self.db = db
 
    def create_inputs_strategy(self, messages: list, system_message: str, query: str, role: str):
        # message_history = MessagesHistory().get_inputs(messages = messages)

        inputs = LLMInputs(messages=messages).get_inputs(system_message=system_message, query=query, role=role)
        
        return inputs
    
    def create_summary_inputs(self,inputs, index):
        return SummaryInputs().get_inputs(inputs, index)