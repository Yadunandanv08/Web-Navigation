import json
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.Clients.GroqClient import GroqClient
from agent_pipeline.Agent.Clients.OpenRouterClient import OpenRouterClient
from agent_pipeline.Agent.Clients.GeminiClient import GeminiClient
from nav2.Tools.actions import ActionTools
from nav2.Tools.perception import PerceptionTools
from nav2.Tools.navigation import NavigationTools
from nav2.Browser.manager import BrowserManager
from nav2.Tools.Models.element import ElementStore
from agent_pipeline.utils.logger import Logger
from nav2.DomMemoryManager import DOMAwareMemoryManager

session = BrowserManager(headless=False)
navigation_tools = NavigationTools(session)
element_store = ElementStore()
shared_memory = DOMAwareMemoryManager(history_window=4, scratchpad_window=6)  
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store, perception_tools)
logger = Logger()


UNIFIED_SYSTEM_PROMPT = """
You are a web navigation agent. You perceive pages and execute actions directly.

**MEMORY CONSTRAINT**
- Old DOM snapshots are minimized as `[PREV DOM]`
- Trust execution logs - don't repeat successful actions

**PROTOCOL**
1. If page is empty/unknown → `open_page`
2. To see current page → `take_snapshot`
3. To interact → use `click_elements`, `type_in_elements`, or `set_date` directly
4. After actions, the system auto-observes changes

**RULES**
- Use exact element IDs from snapshot
- For dropdowns: click trigger for selecting, then select option
- For multi-page forms: click Next/Submit after filling
- Stop when goal achieved or clearly impossible


"""


unified_agent = Agent(
    llm_client=OpenRouterClient(),  
    system_prompt=UNIFIED_SYSTEM_PROMPT,
    tools=[
        perception_tools.take_snapshot,
        navigation_tools.open_page,
        action_tools.click_elements,
        action_tools.type_in_elements,
        action_tools.set_date,
    ],
    max_steps=50,  
    max_retries=3,  
    reasoning=False,
    show_thinking=False,
    memory_manager=shared_memory
)


while True:
    user_input = input("YOU: ")
    if user_input.lower() == 'exit':
        break
    
    response = unified_agent.run(user_input=user_input)
    logger.info(f"Response: {response}")
    print("AGENT:", response['final_response'])
    

"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, DOB: 08/11/2002,
phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary. I found this job on linkedin.
"""


# navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
# print(perception_tools.take_snapshot())
# print(action_tools.set_date("8", "2002-11-08"))

# import time
# time.sleep(2000)


# # add tool
# def add_number_list(numbers: list[str]) -> int:
#     """Adds a list of numbers and returns the sum."""
#     #converst list of strings to list of integers
#     numbers = [int(num) for num in numbers]
#     return sum(numbers)

# testagent = Agent(
#     llm_client=GroqClient(),
#     tools=[add_number_list],
#     max_steps=5,
#     reasoning=False,
#     show_thinking=True
# )

# while True:
#     user_input = input("YOU: ")
#     if user_input.lower() == 'exit':
#         break
    
#     response = testagent.run(user_input=user_input)
#     logger.info(f"Response: {response}")
#     print("AGENT:", response['final_response'])