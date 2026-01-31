import json
#from Rag.retriever import Retriever
#from Rag.embedder import Embedder
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.Clients.GroqClient import GroqClient
from agent_pipeline.Agent.Clients.GeminiClient import GeminiClient
from agent_pipeline.Agent.Clients.OpenRouterClient import OpenRouterClient
from agent_pipeline.Agent.Clients.GithubClient import GitHubModelsClient
from agent_pipeline.Agent.Clients.a4fClient import A4FClient
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigate import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.element_store import ElementStore
from agent_pipeline.utils.logger import Logger
from Navigation.DomMemoryManager import DOMAwareMemoryManager

import time
import re


session = BrowserManager(headless=False)

memory_manager = WebContext()

navigation_tools = NavigationTools(session)
element_store = ElementStore()
planner_memory = DOMAwareMemoryManager()
executor_memory = DOMAwareMemoryManager()
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store)

logger = Logger()

PLANNER_SYSTEM_PROMPT = """
You are the **Planner**. You are the brain of the operation, responsible for Perception and Strategy.
>>>>>>> 87d0d3cf237e2d799a91b75e72699a7a3c9939f0

*** YOUR MEMORY CONSTRAINT (CRITICAL) ***
To save processing power, **OLD DOM SNAPSHOTS ARE AUTOMATICALLY MINIMIZED**.
You will often see `[PREVIOUS DOM SNAPSHOT MINIMIZED]` in your history.
1. **DO NOT** try to view the old page again.
2. **DO NOT** assume the page is empty because the history is minimized.
3. **TRUST THE LOGS:** If the history says "Success: Clicked Button", then you have ALREADY clicked it. Do not click it again. Move to the next step.

*** CORE RESTRICTIONS ***
1. You DO NOT execute actions directly. You must use the `execute_plan` tool.
2. Your goal is to navigate the browser to achieve the user's request.
3. You must be precise with element IDs found in the snapshot.

*** ANALYSIS & PLANNING PROTOCOL ***
1. **Analyze the Snapshot:** Map every relevant UI element to its specific `element_id`.
2. **Inference Logic:**
   - If user data is missing, make reasonable assumptions based on context.
   - If the page is empty, Open the page using tool`open_page`.
3. **Complex Interaction Handling:**
   - **Dropdowns:** Plan a sequence: (1) Click trigger -> (2) Click option.
   - **Multi-Page Forms:** If you see "Next/Submit", you MUST plan to click it.
   - **Verification:** After `execute_plan` returns "Success", call `take_snapshot` to verify the page changed.
4. **Termination:** Terminate execution when the goal is fully reached or is unreachable after multiple retries.
5. The executor has the following tools at its disposal: `click_elements`, `type_in_elements`, and `set_date`.
6. If the excutor reports failure, retry with a modified plan on the failed and unexecuted steps only. Donot repeat successful steps.
*** THE EXECUTION TOOL ***
You have a tool named `execute_plan`. It accepts a SINGLE argument: `plan`.
The `plan` argument must be a **JSON List** of actions.

**Plan Structure (Pass this list to the tool):**
[
  {
    "tool": "type_in_elements", 
    "args": {"actions": [{"element_id": "45", "text": "John Doe"}]}, 
    "description": "Fill Name"
  },
  {
    "tool": "click_elements", 
    "args": {"element_ids": ["99"]}, 
    "description": "Select Option"
  },
  {
    "tool": "set_date", 
    "args": {"element_id": "32", "date": "2000-01-01"}, 
    "description": "Set Date of Birth"
]
"""

EXECUTOR_SYSTEM_PROMPT = """
You are the **Executor**. You are a blind, precise execution unit.

*** INPUT ***
You will receive a plan (JSON List).

*** EXECUTION PROTOCOL ***
1. **Analyze History:** Before taking any action, check the `Scratchpad`.
   - If "Step 1" is marked SUCCESS in history, **SKIP IT** and move to Step 2.
   - **NEVER** repeat a successful action "just to be sure". 
   - Trust the history.

2. **Tool Failure:** - If a tool fails (Red Error), retry ONCE with corrected arguments. 
   - If it fails twice, STOP and report failure.

3. **Argument Correction:** - If the Plan uses a wrong argument name, use your intelligence to map it to the correct tool argument.

*** OUTPUT FORMAT ***
Return a single string summary:
"SUCCESS: [List of steps completed]" or "FAILURE: Stopped at Step X."
"""


def execute_plan(plan: str) -> str:
    """
    Executes a sequence of browser actions.
    
    Args:
        plan: A list of action dictionaries OR a JSON string representing that list.
              Example: [{"tool": "click_elements", "args": {...}}]
    """

    try:
        response = executor.run(user_input=plan)
        print("Executor Response:", response)
        return response['final_response']
    except Exception as e:
        raise ValueError(f"Failed to execute plan: {e}")


planner = Agent(
    llm_client=GitHubModelsClient(),
    system_prompt=PLANNER_SYSTEM_PROMPT,
    tools=[
        perception_tools.take_snapshot,
        navigation_tools.open_page,
        execute_plan,
    ],
    memory_manager=memory_manager,
    max_steps=50,
    max_retries=5,
    reasoning=True,
    show_thinking=True,
)

executor = Agent(
    llm_client=GroqClient(),
    system_prompt=EXECUTOR_SYSTEM_PROMPT,
    tools=[
        action_tools.click_elements,
        action_tools.type_in_elements,
        action_tools.set_date
    ],
    max_steps=10,
    max_retries=2,
    reasoning=False,
    show_thinking=False,
)


# while True:
#     user_input = input("YOU: ")
#     if user_input.lower() == 'exit':
#         break
#     response = planner.run(user_input=user_input)
#     logger.info(f"Agent Response: {response}")
#     print("AGENT:", response['final_response'])
    

"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, DOB: 08/11/2002,
phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary. I found this job on linkedin.
"""

#refactored prompt
"""
    Open this google form [https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog](https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog) and fill it. here are my personal details:
 My name is yadunandan, my email is yadunandanv08@gmail.com, phone: 6238922215, and i am a final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary. i heard about this job opening from linkedin. For now fill these details and skip the rest. submit the form after going through the different sections of the form.
    """

navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
print(perception_tools.take_snapshot())
# action_tools.click_elements(["21"])
# perception_tools.take_snapshot()
# action_tools.click_elements(["29"])
# perception_tools.take_snapshot()
