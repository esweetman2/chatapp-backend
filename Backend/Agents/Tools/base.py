from abc import ABC, abstractmethod
import json
from Backend.Agents.Tools.GoogleSheets import GoogleSheets
from Backend.Agents.Tools.ExtractWebsite import fetch_page_text
from Backend.Agents.Tools.AccessData.TaskData import get_task, update_task
import json


tool_registry = {
    "extract_html_from_website": fetch_page_text,
    "read_google_sheet": GoogleSheets().read_google_sheet,
    "get_task": get_task,
    "update_task": update_task
}

class ToolStrategy(ABC):
    @abstractmethod
    def get_tools(self, llm_response):
        pass
    def _format_tools_for_response(self, tools_calls):
        pass

class FormatToolsStrategy(ABC):
    @abstractmethod
    def format_tools(self, tools):
        pass

class AgentToolsStrategy(ABC):
    @abstractmethod
    def get_agent_tools(self, tools):
        pass

class AgentTools(AgentToolsStrategy):
    def get_agent_tools(self, db, agent_id):
        try:
            tools = []
            agent_tools = db.get_agent_tool(agent_id=agent_id)
            # print("agent_tools: ", agent_tools)
            for i in agent_tools:
                tools.append(db.get_tools(tool_id=i.tool_id))

            return tools
        
        except Exception as e:
            print("Error fetching agent tools: ", str(e))
            return []

class FormatAgentTools(FormatToolsStrategy):
    def format_tools(self, tools):
        formatted_tools = []
        # print("Tools: ", tools)
        for tool in tools:
            _tool = {
                "type": tool.tool_type,
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            if "web_search" in tool.tool_type:
                del _tool['name']
                del _tool['description']
                del _tool['parameters']

            formatted_tools.append(_tool)
        # print(formatted_tools)
        return formatted_tools
    
    def format_tools_ai_tools_response(self, ai_tool_calls):
        input_list = []
        # print(ai_tool_calls)
        for tool in ai_tool_calls:
            tool_name = tool.name
            tool_args = json.loads(tool.arguments)
            if tool_name not in tool_registry:
                raise ValueError(f"Unknown tool: {tool_name}")
            print(tool_registry[tool_name])
            print(tool_args)
            result = tool_registry[tool_name](**tool_args)
            print("result: ", result)
            input_list.append({
                    "type": "function_call_output",
                    "call_id": tool.call_id,
                    "output": json.dumps({
                    tool_name: result
                    })
                })


            # if tool.name == "read_google_sheet":
            #     args = json.loads(tool.arguments)

            #     google_sheet_data = GoogleSheet.read_google_sheet(google_sheet_name=args["google_sheet_name"], worksheet=args["worksheet"])

            #     # 4. Provide function call results to the model
            #     input_list.append({
            #         "type": "function_call_output",
            #         "call_id": tool.call_id,
            #         "output": json.dumps({
            #         "read_google_sheet": google_sheet_data
            #         })
            #     })
            # formatted_tools.append(_tool)
        return input_list



class LLMResponseToolSelector(ToolStrategy):
    def __init__(self, llm_response):
        self.llm_response = llm_response

    def get_tools(self):
        tool_calls = []

        for item in self.llm_response:
            if item.type == "function_call":
                tool_calls.append(item)
        return tool_calls


class ToolFactory:
    def __init__(self, db, agent_id):
        # self.google_sheets = google_sheets
        # self.tool_selector = ToolSelector(llm_response)
        self.agent_tools = AgentTools().get_agent_tools(db=db, agent_id=agent_id)

    def create_agent_tools(self):
        # tools = self.tool_selector.get_tools()
        return FormatAgentTools().format_tools(self.agent_tools)
    
    def llm_response_tool_selector(self, llm_response):
        return LLMResponseToolSelector(llm_response=llm_response).get_tools()
    
    def llm_response_tools(self, llm_response_with_tools):
        return FormatAgentTools().format_tools_ai_tools_response(llm_response_with_tools)


