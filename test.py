import json
from Rag.retriever import Retriever
from Rag.embedder import Embedder
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.GroqClient import GroqClient
from agent_pipeline.Agent.GeminiClient import GeminiClient
from agent_pipeline.Agent.OpenRouterClient import OpenRouterClient
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigate import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.element_store import ElementStore

session = BrowserManager(headless=False)

navigation_tools = NavigationTools(session)
element_store = ElementStore()
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store)


agent = Agent(
    llm_client=OpenRouterClient(),
    system_prompt="You are a helpful assistant that helps users navigate the web and perform actions on web pages.",
    tools=[
        navigation_tools.open_page, 
        perception_tools.take_snapshot, 
        action_tools.click_elements, 
        perception_tools.retrieve_element,
        action_tools.type_in_elements, 
        action_tools.set_date,
        action_tools.execute_batch

    ],
    max_iterations=25,
    max_retries=2,
    reasoning=False,
    show_thinking=True,
)

while True:
    user_query = input("You: ")
    if user_query.lower() == "exit":
        break
    result = agent.run(user_query)
    print(f"Agent: {result['final_response']}")
    print(f"[DEBUG] History Log:{json.dumps(result['history'], indent=2)}")



"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary

Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill my date of birth 3 jan 2004.
"""


#navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
#print(perception_tools.take_snapshot())
#print(perception_tools.retriever.texts)
# navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
# print(perception_tools.take_snapshot())

#print("\n===================\n")
#print(perception_tools.retriever.metadata)
