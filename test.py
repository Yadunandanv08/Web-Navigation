import json
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.Clients.GroqClient import GroqClient
from agent_pipeline.Agent.Clients.OpenRouterClient import OpenRouterClient
from agent_pipeline.Agent.Clients.GeminiClient import GeminiClient
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigation import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element import ElementStore
from agent_pipeline.utils.logger import Logger
from Navigation.DomMemoryManager import DOMAwareMemoryManager

session = BrowserManager(headless=False)
navigation_tools = NavigationTools(session)
element_store = ElementStore()
shared_memory = DOMAwareMemoryManager(history_window=4, scratchpad_window=6)  
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store, perception_tools,file_path="C:/Developer/FinalProject/nav2/sample_upload.txt")
logger = Logger()


# UNIFIED_SYSTEM_PROMPT = """
# You are a web navigation agent. You perceive pages and execute actions directly.

# **MEMORY CONSTRAINT**
# - Old DOM snapshots are minimized as `[PREV DOM]`
# - Trust execution logs - don't repeat successful actions

# **PROTOCOL**
# 1. If page is empty/unknown → `open_page`
# 2. To see current page → `take_snapshot`
# 3. To interact → use `click_elements`, `type_in_elements`, or `set_date` directly
# 4. After actions, the system auto-observes changes
# 5. Use `upload_file` to upload files directly via file input elements

# **RULES**
# - Use exact element IDs from snapshot
# - For dropdowns: click trigger for selecting, then select option
# - For multi-page forms: click Next/Submit after filling
# - Stop when goal achieved or clearly impossible


# """
UNIFIED_SYSTEM_PROMPT = """
You are a web navigation agent. You perceive pages and execute actions directly.
Complete the task using all the information and infer from data if possible, else skip.

**MEMORY CONSTRAINT**
- Old DOM snapshots are minimized as `[PREV DOM]`
- Trust execution logs - don't repeat successful actions

**PROTOCOL**
1. If page is empty/unknown → `open_page`
2. To see current page → `take_snapshot`
3. To interact → use `click_elements`, `type_in_elements`, or `set_date` directly
4. After actions, the system auto-observes changes

**CRITICAL RULES**
- **STRICT ID ENFORCEMENT:** Input arguments must use the EXACT `element_id` (e.g., "7", "12") from the current snapshot. **NEVER** invent string IDs like "fileUpload" or "submitBtn".
- **FILE UPLOADS:** Identify the visible **trigger button** (e.g., "Add file", "Upload Resume") in the snapshot. Pass **THAT** button's ID to `upload_file`. Do NOT use `click_elements` on it; `upload_file` handles the click automatically.
- For dropdowns: click trigger for selecting, then select option
- For multi-page forms: click Next/Submit after filling
- Stop when goal achieved or clearly impossible
"""

unified_agent = Agent(
    llm_client=GeminiClient(),  
    system_prompt=UNIFIED_SYSTEM_PROMPT,
    tools=[
        perception_tools.take_snapshot,
        navigation_tools.open_page,
        action_tools.click_elements,
        action_tools.type_in_elements,
        action_tools.set_date,
        action_tools.upload_file,
    ],
    max_steps=50,  
    max_retries=3,  
    reasoning=False,
    show_thinking=True,
    memory_manager=shared_memory
)


# while True:
#     user_input = input("YOU: ")
#     if user_input.lower() == 'exit':
#         break
    
#     response = unified_agent.run(user_input=user_input)
#     logger.info(f"Response: {response}")
#     print("AGENT:", response['final_response'])
    

"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, DOB: 08/11/2002,
phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary. I found this job on linkedin.
"""
"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSeIIOkuFqPagjWMam4HcxOLzgdtYfdWELNhtVombwUrEpXSew/viewform?usp=publish-editor and you will notice a field to upload resume. please upload the resume and submit the form.
"""

while True:
    user_input = input("YOU: ")
    if user_input.lower() == 'exit':
        break
    
    response = unified_agent.run(user_input=user_input)
    logger.info(f"Response: {response}")
    print("AGENT:", response['final_response'])

# navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSeIIOkuFqPagjWMam4HcxOLzgdtYfdWELNhtVombwUrEpXSew/viewform?usp=publish-editor")
# perception_tools.take_snapshot()
# print(action_tools.upload_file("7"))
# import time
# time.sleep (2000)
