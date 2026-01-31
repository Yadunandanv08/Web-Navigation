import inspect
import asyncio
from typing import List, Optional
from agent_pipeline.Tool_Execution.parse_tool_call import generate_available_tools, parse_tool_call
from agent_pipeline.utils.parser import extract_tagged_content
from agent_pipeline.utils.logger import Logger
from agent_pipeline.Agent.Abstactions.AbstractMemory import MemoryManager
from agent_pipeline.Agent.Memory.standard import SlidingWindowMemory

logger = Logger()

BASE_INSTRUCTIONS = """
You are a precise agent.

**Previous Conversation:**
__CHAT_HISTORY__

**Current User Goal:**
__QUESTION__

**Available Tools:**
<tools>
__TOOLS__
</tools>

**Scratchpad (Current Task Progress):**
__SCRATCHPAD__

**CRITICAL RULES:**
1. Analyze the goal, history, and tools.
2. Review the Scratchpad to see what has already been done.
3. **DO NOT** output any conversational text. Use ONLY the tags below.
4. **DECISION PROTOCOL:**
   - If you need to use a tool -> Use **Format 1 (Tool Call)**.
   - If you have completed the instruction or need to stop -> Use **Format 2 (Final Answer)**.
   - **NEVER** use both in the same response.

__FORMAT_INSTRUCTIONS__
"""

REASONING_INSTRUCTIONS = """
**Format 1: If you need to use a tool**
<thinking>
Brief reasoning on why you need this tool.
</thinking>
<tool_call>
{"name": "function-name", "arguments": { ... }}
</tool_call>
*Note: Do NOT wrap the JSON in markdown code blocks (```).*

**Format 2: Final Answer (Mission Complete or Question Answered)**
<thinking>
Reasoning on how you arrived at the answer.
</thinking>
<final_answer>The specific answer or instruction.</final_answer>
"""

DIRECT_INSTRUCTIONS = """
**Format 1: Tool Call**
<tool_call>
{"name": "function-name", "arguments": { ... }}
</tool_call>

**Format 2: Final Answer**
<final_answer>The answer.</final_answer>
"""

class Agent:
    def __init__(self, llm_client, tools, memory_manager: Optional[MemoryManager] = None, max_steps=5, max_retries=2, reasoning=True, show_thinking=True, system_prompt=None):
        self.llm_client = llm_client
        self.tools = tools
        self.function_map = {func.__name__: func for func in tools}
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.reasoning = reasoning
        self.show_thinking = show_thinking
        self.system_prompt = system_prompt
        
        if memory_manager:
            self.memory = memory_manager
        else:
            self.memory = SlidingWindowMemory(history_window=6, scratchpad_window=10)

    def _call_llm(self, prompt: str) -> str:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.llm_client.generate_response(messages)
    
    def run(self, user_input: str): 
        
        if self.tools:
            available_tools_str = generate_available_tools(self.tools)
        else:
            available_tools_str = "No tools available."

        if self.reasoning:
            current_format = REASONING_INSTRUCTIONS
        else:
            current_format = DIRECT_INSTRUCTIONS

        for i in range(self.max_steps):
            
            history_str = self.memory.get_context()
            current_scratchpad = self.memory.get_scratchpad()
            
<<<<<<< HEAD
            prompt = BASE_INSTRUCTIONS.format(
                chat_history=history_str,
                question=user_input, 
                tools=available_tools_str, 
                scratchpad=current_scratchpad,
                format_instructions=current_format,
                max_retries=self.max_retries,
                max_iterations=self.max_iterations,
            )
=======
            prompt = BASE_INSTRUCTIONS.replace("__CHAT_HISTORY__", history_str) \
                                      .replace("__QUESTION__", user_input) \
                                      .replace("__TOOLS__", available_tools_str) \
                                      .replace("__SCRATCHPAD__", current_scratchpad) \
                                      .replace("__FORMAT_INSTRUCTIONS__", current_format)
>>>>>>> 87d0d3cf237e2d799a91b75e72699a7a3c9939f0

            llm_response = self._call_llm(prompt)
            if not llm_response or not llm_response.strip():
                self.memory.add_scratchpad_entry(f"Observation {i+1}: Error. You returned an empty response. Please output a valid <tool_call> or <final_answer>.")
                continue

            if self.show_thinking:
                thinking_process = extract_tagged_content(llm_response, "thinking")
                if thinking_process:
                    logger.thought(thinking_process)

            final_answer = extract_tagged_content(llm_response, "final_answer")
            if final_answer:
                self.memory.add_message("User", user_input)
                self.memory.add_message("Assistant", final_answer)
                return {
                    "final_response": final_answer, 
                    "history": self.memory.get_raw_scratchpad()
                }

            try:
                tool_call = parse_tool_call(llm_response)
                
                if tool_call:
                    if tool_call["name"] in self.function_map:
                        function_to_call = self.function_map[tool_call["name"]]
                        print(f"Calling tool: {tool_call['name']} with arguments {tool_call['arguments']}")
                        
                        if inspect.iscoroutinefunction(function_to_call):
                            tool_result = asyncio.run(function_to_call(**tool_call["arguments"]))
                        else:
                            tool_result = function_to_call(**tool_call["arguments"])
                        
                        log_entry = (
                            f"Observation {i+1}: You used tool '{tool_call['name']}' with args {tool_call['arguments']}.\n"
                            f"Result: {tool_result}" 
                        )
                        self.memory.add_scratchpad_entry(log_entry)
                    else:
                        self.memory.add_scratchpad_entry(f"Observation {i+1}: Error. Tool '{tool_call['name']}' not found.")
                
                else:
                    self.memory.add_scratchpad_entry(f"Observation {i+1}: Error. Unrecognized format. Please ensure you use <tool_call> or <final_answer> tags.")
                    continue

            except Exception as e:
                self.memory.add_scratchpad_entry(f"Observation {i+1}: Execution Error: {e}")
        
        failure_msg = "I could not complete the task within the given steps."
        
        self.memory.add_message("User", user_input)
        self.memory.add_message("Assistant", failure_msg)

        return {
            "final_response": failure_msg,
            "history": self.memory.get_raw_scratchpad()
        }