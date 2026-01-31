import os
from google import genai
from dotenv import load_dotenv
from agent_pipeline.Tool_Execution.parse_tool_call import parse_tool_call, generate_available_tools

load_dotenv()

from agent_pipeline.utils.logger import Logger


TOOL_EXECUTION_PROMPT = """
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags. 
You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug 
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.
For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
Infer the tool parameters from user query as required. Donot make up parameters.

<tool_call>
{"name": <function-name>,"arguments": <args-dict>}
</tool_call>

If you do NOT need to call any tool to answer the user's question, respond directly without returning <tool_call> tags.
"""



class ToolAgent:
    def __init__(self, tools:list):
        self.client = genai.Client()
        self.model_name = os.getenv("GEMINI_MODEL")
        self.tools = tools

    def _tool_api_call(self, system_prompt: str, messages: list):
        api_history = [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "model", "parts": [{"text": "Understood. I will perform my task as instructed."}]}
        ]
        api_history.extend(messages)
        response = chat_completion(self, api_history)
        return response.text
    
    def build_prompt(self):
        available_tools = generate_available_tools(self.tools)
        return TOOL_EXECUTION_PROMPT + "\nHere are the available tools:\n" + available_tools

    
    def run_tools(self, user_input:str):
        PROMPT_TOOL = self.build_prompt()

        tool_chat_history = [
            {
                "role": "user",
                "parts": [{"text": PROMPT_TOOL}]
            },
            {
                "role": "model",
                "parts": [{"text": "Understood. I will perform my task as instructed."}]
            }
        ]
        user_msg = {
            "role": "user",
            "parts": [{"text": user_input}]
        }

        tool_chat_history.append(user_msg)

        output = self._tool_api_call(
            system_prompt=PROMPT_TOOL,
            messages=tool_chat_history
        )

        function_map = {func.__name__: func for func in self.tools}

        try:
            tool_call = parse_tool_call(output)

            if tool_call["name"] in function_map:
                result = function_map[tool_call["name"]](**tool_call["arguments"])
            
                tool_llm_response = self._tool_api_call(
                    system_prompt=f"The tool response is: {result}, Present this result to the user according to the question asked accurately in proper sentance. Treat tool answer as final.",
                    messages=user_input
                )
            else:
                tool_llm_response = f"Sorry, I do not have the tool named '{tool_call['name']}' to handle your request."
                result = None
        except Exception:
            tool_llm_response = output
            tool_call = None
            result = None

        return {
        "final_response": tool_llm_response,
        "tool_call": tool_call,
        "tool_result": result
        }
