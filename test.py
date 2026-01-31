import json
#from Rag.retriever import Retriever
#from Rag.embedder import Embedder
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.Clients.GroqClient import GroqClient
from agent_pipeline.Agent.Clients.GeminiClient import GeminiClient
from agent_pipeline.Agent.Clients.OpenRouterClient import OpenRouterClient
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigate import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.element_store import ElementStore
from agent_pipeline.utils.logger import Logger
from agent_pipeline.Agent.Memory.webcontext import WebContext

session = BrowserManager(headless=False)

memory_manager = WebContext()

navigation_tools = NavigationTools(session)
element_store = ElementStore()
perception_tools = PerceptionTools(session, element_store,memory_manager)
action_tools = ActionTools(session, element_store)


Orchestrator = Agent(
    llm_client=OpenRouterClient(),
    system_prompt="""
        You are a single web automation agent responsible for perception, planning, and execution.
        Responsibilities:
        1. Use the snapshot tool to understand the current webpage.
        2. Identify relevant elements and reason using:
           - element id
           - type of field (input, button, dropdown, checkbox, date, option, etc.)
           - any relevant metadata required for interaction
        3. Detect if the website is multi-page and mention navigation requirements.
        4. Plan and execute actions using the available tools.
        5. Ensure element IDs used for actions exactly match those discovered via snapshot.
        6. Handle dropdowns with sequential clicks (open → select).
        7. Retry failed actions up to two times and stop on repeated failure.
        8. Do not enter infinite loops.
        9. Evaluate if the page is single or multi-page and plan navigation accordingly.
        10. If any detail is missing, make reasonable assumptions based on context or if there is no way to infer, leave it.

        Return concise, structured responses.
    """,
    tools=[
        perception_tools.take_snapshot,
        action_tools.click_elements,
        action_tools.type_in_elements,
        navigation_tools.open_page,
    ],
    memory_manager=memory_manager,
    max_steps=50,
    max_retries=10,
    reasoning=False,
    show_thinking=True,
)


logger = Logger()
"""
while True:
    user_input = input("YOU: ")
    if user_input.lower() == 'exit':
        break
    response = Orchestrator.run(user_input=user_input)
    logger.info(f"Agent Response: {response}")
    print("AGENT:", response['final_response'])
"""


while True:
    user_input = input("YOU: ")
    if user_input.lower() == 'exit':
        break
    response = Orchestrator.run(user_input=user_input)
    print("FULL RESPONSE:", json.dumps(response, indent=2))
    print("AGENT:", response['final_response'])

"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary
"""

#refactored prompt
"""
    Open this google form [https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog](https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog) and fill it. here are my personal details:
 My name is yadunandan, my email is yadunandanv08@gmail.com, phone: 6238922215, and i am a final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary. i heard about this job opening from linkedin. For now fill these details and skip the rest. submit the form after going through the different sections of the form.
    """

#navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
#print(perception_tools.take_snapshot())
#print(perception_tools.retriever.texts)
# navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
# perception_tools.take_snapshot()
# print(action_tools.click_elements(['13']))
# print(action_tools.click_elements(['16']))
# import time
# time.sleep(20)

#print("\n===================\n")
#print(perception_tools.retriever.metadata)
