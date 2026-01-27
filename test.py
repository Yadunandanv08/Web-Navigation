import json
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


navigation_tools = NavigationTools(session)
element_store = ElementStore()
planner_memory = DOMAwareMemoryManager()
executor_memory = DOMAwareMemoryManager()
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store)


# Orchestrator = Agent(
#     llm_client=GitHubModelsClient(),
#     system_prompt="""
#         You are a single web automation agent responsible for perception, planning, and execution.

#         *** CRITICAL TERMINATION PROTOCOL ***
#         1. DEFINITION OF DONE: You are strictly FORBIDDEN from stopping until you see a final submission confirmation screen (e.g., "Your response has been recorded", "Thank you", "Success").
#         2. MULTI-PAGE NAVIGATION: If you see a "Next", "Continue", or "Submit" button, you MUST click it. Do not assume the form ends on the current page.
#         3. VERIFICATION: After clicking a navigation button, you MUST take a new snapshot to confirm you have moved to the next page.

#         Responsibilities:
#         1. Use the snapshot tool to understand the current webpage.
#         2. Identify relevant elements and reason using:
#            - element id
#            - type of field (input, button, dropdown, checkbox, date, option, etc.)
#            - any relevant metadata required for interaction
#         3. Detect if the website is multi-page and mention navigation requirements.
#         4. Plan and execute actions using the available tools.
#         5. Ensure element IDs used for actions exactly match those discovered via snapshot.
#         6. Handle invisible elements like dropdowns with sequential clicks (open → select)(Some cases, listboxes can be dropdowns).
#         7. Retry failed actions up to two times and stop on repeated failure.
#         8. Do not enter infinite loops.
#         9. Evaluate if the page is single or multi-page and plan navigation accordingly.
#         10. If any detail is missing, make reasonable assumptions based on context or if there is no way to infer, leave it.
#            But make sure to never leave an inferable detail blank.

#         Return concise, structured responses.
#     """,
#     tools=[
#         perception_tools.take_snapshot,
#         action_tools.click_elements,
#         action_tools.type_in_elements,
#         navigation_tools.open_page,
#     ],
#     max_steps=50,
#     max_retries=10,
#     reasoning=True,
#     show_thinking=True,
# )



Orchestrator = Agent(
    llm_client=GitHubModelsClient(),
    system_prompt="""
        You are a single web automation agent responsible for perception, planning, and execution.

        For the current task, Your goal is to not fill but generate a plan for the task given by the user for the current page and just
        return the plan. The plan should contain what to do and which elements to target in what order.
        Open the page first, take a snapshot and plan
    """,
    tools=[
        perception_tools.take_snapshot,
        action_tools.click_elements,
        action_tools.type_in_elements,
        navigation_tools.open_page,
    ],
    max_steps=50,
    max_retries=10,
    reasoning=True,
    show_thinking=True,
)

logger = Logger()

# while True:
#     user_input = input("YOU: ")
#     if user_input.lower() == 'exit':
#         break
#     response = Orchestrator.run(user_input=user_input)
#     logger.info(f"Agent Response: {response}")
#     print("AGENT:", response['final_response'])


"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, 
phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary. I found this job on linkedin.
"""


# navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
# perception_tools.take_snapshot()
# action_tools.click_elements(["21"])
# perception_tools.take_snapshot()
# action_tools.click_elements(["29"])
# perception_tools.take_snapshot()










PLANNER_SYSTEM_PROMPT = """
You are the **Planner**. You are the brain of the operation, responsible for Perception and Strategy.

*** CORE RESTRICTIONS ***
1. Your ONLY tools are `take_snapshot` and `open_page`.
2. You **DO NOT** execute actions (no clicking or typing). You only write the instructions.
3. Your Output MUST be a strict JSON list of actions.

*** ANALYSIS & PLANNING PROTOCOL ***
1. **Analyze the Snapshot:** Map every relevant UI element to its specific `element_id`.
2. **Inference Logic:**
   - If user data is missing, make reasonable assumptions based on context (e.g., if asked for "City" and context implies "New York", fill it). Never leave an inferable field blank.
   - If the page is empty, plan to `open_page`.
3. **Complex Interaction Handling:**
   - **Dropdowns/Listboxes:** Invisible elements often require two steps. Plan a sequence: 
     Step 1: Click the dropdown trigger. 
     Step 2: Click the desired option.
   - **Multi-Page Forms:** If you see "Next", "Continue", or "Submit", you MUST plan to click it. Do not assume the form ends here.
   - **Next Steps:** After the executor returns successful execution, take new snapshot to verify completion or to continue.
4. **Termination:** - If you see a final success message (e.g., "Response recorded", "Success"), output an empty plan `[]` or a plan with a "DONE" description to signal completion.

*** OUTPUT FORMAT ***
Return **ONLY** a JSON list. Do not write conversational text outside the JSON.

Example Plan Format(Follow this structure exactly):
[
  {
    "tool": "type_in_elements", 
    "args": {"input_data": [{"id": "45", "text": "John Doe"}]}, 
    "description": "Fill Name"
  },
  {
    "tool": "click_elements", 
    "args": {"element_ids": ["12"]}, 
    "description": "Open Dropdown"
  },
  {
    "tool": "click_elements", 
    "args": {"element_ids": ["99"]}, 
    "description": "Select 'Option A' from dropdown"
  },
  {
    "tool": "click_elements", 
    "args": {"element_ids": ["55"]}, 
    "description": "Click Next"
  }
]
"""

EXECUTOR_SYSTEM_PROMPT = """
You are the **Executor**. You are a precise, blind execution unit.
1. You DO NOT see the webpage. You only see a **PLAN** provided by the user.
2. Your Goal: Execute the tools specified in the plan EXACTLY as written.
3. If a tool fails, retry once, then stop and report failure.
4. Do not deviate from the plan or hallucinate new steps.
"""


class Controller:
    def __init__(self):
        self.planner = Agent(
            llm_client=OpenRouterClient(),
            tools=[perception_tools.take_snapshot, navigation_tools.open_page],
            system_prompt=PLANNER_SYSTEM_PROMPT,
            reasoning=True,
            show_thinking=True,
            max_steps=50
        )
        
        self.executor = Agent(
            llm_client=GroqClient(),
            tools=[action_tools.click_elements, action_tools.type_in_elements],
            system_prompt=EXECUTOR_SYSTEM_PROMPT,
            reasoning=False,
            show_thinking=False,
            max_steps=50
        )

    def run_mission(self, user_goal: str):
        while True:
            print("\n--- PHASE 1: PLANNING ---")
            
            
            planner_input = f"Current Goal: {user_goal}. \nIf you haven't opened the page, open it. Take a snapshot. Generate a plan."
            planner_response = self.planner.run(planner_input)
            
            
            plan_str = planner_response['final_response'].strip()
            
            if "```" in plan_str:
                match = re.search(r"```(?:json)?(.*?)```", plan_str, re.DOTALL)
                if match:
                    plan_str = match.group(1).strip()

            logger.info(f"PLAN RECEIVED (Raw): \n{plan_str[:200]}...")

            
            if plan_str == "DONE" or plan_str == "[]" or "mission complete" in plan_str.lower():
                logger.info("Planner signaled completion.")
                break

            print("\n--- PHASE 2: EXECUTION ---")
            
            
            self.executor.memory.clear_scratchpad() 
            
            executor_prompt = f"""
            Here is the execution plan. Read it and execute the steps sequentially.
            
            PLAN:
            {plan_str}
            
            Execute item by item. When you have finished all items in this plan, output exactly: "DONE"
            """
            
            executor_done = False
            execution_steps_count = 0
            
            while not executor_done:
                
                msg = executor_prompt if execution_steps_count == 0 else "Continue to the next step in the plan. If finished, say DONE."
                
                exec_response = self.executor.run(msg)
                final_res = exec_response['final_response']
                
                if "DONE" in final_res:
                    executor_done = True
                    logger.info("Execution Phase Complete.")
                else:
                    execution_steps_count += 1
                   
                    if execution_steps_count > 15: 
                        logger.error("Executor stuck. Forcing re-plan.")
                        break

            print("\n--- PHASE 3: VERIFICATION ---")
            time.sleep(2)
            
            
if __name__ == "__main__":
    controller = Controller()
    user_task = input("Enter the automation task: ")
    controller.run_mission(user_task)