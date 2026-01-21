ORCHESTRATOR_PROMPT = """
You are a reliable and intelligent assistant that answers user queries.

**User's Goal:**
{question}

**Available Tools:**
<tools>
{tools}
</tools>

**Instructions:**
1.  Carefully analyze the user's goal and the available tools.
2.  Review the "Scratchpad" which contains the history of your previous actions and their results.
3.  Decide on your next step.
4.  You MUST respond in ONE of the following formats:

IF THE USER QUERY REQUIRES NO THOUGT, PROVIDE FINAL ANSWER DIRECTLY.
USE TOOLS ONLY IF NECESSARY. DONOT USE TOOLS EVERYWHERE.

**Format 1: If you need to use a tool**
<thinking>Your reasoning on why you need to use this specific tool to progress towards the goal.</thinking>
<tool_call>
{{"name": "function-name", "arguments": {{"arg1": "value1", ...}}}}
</tool_call>

**Format 2: If you have enough information to answer the user's goal**
<thinking>Your reasoning on how you arrived at the final answer based on the scratchpad.</thinking>
<final_answer>The complete and final answer to the user's question.</final_answer>

**Scratchpad (Your Work History):**
{scratchpad}
"""


import os
import json
from google import genai
from dotenv import load_dotenv
from typing import List, Dict
import inspect
import asyncio

from agent_pipeline.Agent.AbstractLLM import AbstractLLMClient
from agent_pipeline.Tool_Execution.parse_tool_call import generate_available_tools, parse_tool_call
from agent_pipeline.utils.parser import extract_tagged_content
from agent_pipeline.utils.logger import Logger

logger = Logger()

load_dotenv()

class Agent:
    def __init__(self, llm_client: AbstractLLMClient, tools: List, max_iterations: int = 5, show_thinking: bool = True, system_prompt: str = None):
        self.llm_client = llm_client
        self.model_name = llm_client.model_name

        self.tools = tools
        self.function_map = {func.__name__: func for func in tools}
        self.max_iterations = max_iterations
        self.show_thinking = show_thinking
        self.system_prompt = system_prompt
        

    def _call_llm(self, prompt: str) -> str:

        messages = []

        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.llm_client.generate_response(prompt, messages)

        return response
    
    def run(self, user_input:str):
        history_log  = []
        available_tools_str = generate_available_tools(self.tools)

        WINDOW_SIZE = 8

        for i in range(self.max_iterations):

            if history_log:
                current_scratchpad = "\n".join(history_log[-WINDOW_SIZE:])
            else:
                current_scratchpad = ""
            prompt = ORCHESTRATOR_PROMPT.format(
                question=user_input,
                tools=available_tools_str,
                scratchpad=current_scratchpad
            )

            llm_response = self._call_llm(prompt)

            if self.show_thinking:
                thinking_process = extract_tagged_content(llm_response, "thinking")
                if thinking_process:
                    logger.thought(thinking_process)

            final_answer = extract_tagged_content(llm_response, "final_answer")
            if final_answer:
                return {"final_response": final_answer, "history": history_log}
            

            try:
                tool_call = parse_tool_call(llm_response)
                if tool_call and tool_call["name"] in self.function_map:
                    function_to_call = self.function_map[tool_call["name"]]
                    print(f"Calling tool: {tool_call['name']} with arguments {tool_call['arguments']}")
                    if inspect.iscoroutinefunction(function_to_call):
                        tool_result = asyncio.run(function_to_call(**tool_call["arguments"]))
                    else:
                        tool_result = function_to_call(**tool_call["arguments"])
                    
                    log_entry = (
                        f"Observation {i+1}: You used the tool '{tool_call['name']}' with arguments {tool_call['arguments']}.\n"
                        f"Tool Result: {tool_result}" # 
                    )
                    history_log.append(log_entry)

                else:
                    history_log.append(f"Observation {i+1}: You tried to call an invalid tool or the format was wrong.")


            except Exception as e:
                history_log.append(f"Observation {i+1}: An error occurred while trying to call a tool. Error: {e}")
                print(f"Error parsing tool call: {e}")

        return {
            "final_response": "I could not complete the task within the given number of steps.",
            "history": history_log
        }
    
