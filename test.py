import json
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.GroqClient import GroqClient
from agent_pipeline.Agent.GeminiClient import GeminiClient
from agent_pipeline.Agent.OpenRouterClient import OpenRouterClient
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigate import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.element_store import ElementStore
from agent_pipeline.utils.logger import Logger

session = BrowserManager(headless=False)


navigation_tools = NavigationTools(session)
element_store = ElementStore()
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store)


Perceptor = Agent(
    llm_client=OpenRouterClient(),
    system_prompt="""
        Use the snapshot tool to take a snapshot of the current webpage and return the relevant information about the page.
        Answer by returing the relevant element id, type of field and relevant info in a consice manner.
        If general information about the page is needed, take a snapshot and return all the relevant info and ids.
    """,
    tools=[
        perception_tools.take_snapshot
    ],
    max_steps=25,
    max_retries=2,
    reasoning=False,
    show_thinking=True,
)

Executor = Agent(
    llm_client=OpenRouterClient(),
    system_prompt="""
        Use the tools to interact with the webpage as per the user instructions.
        When the tool returns a success message, proceed to the next step(status: ok is success).
        If failure, retry twice according to the error and afreturn failure if still not successful.
        Donot run infinite loops.
    """,
    tools=[
        action_tools.click_elements,
        action_tools.type_in_elements,
        navigation_tools.open_page,
    ],
    max_steps=25,
    max_retries=2,
    reasoning=False,
    show_thinking=True,
)
logger = Logger()
def call_perception_agent(query: str):
    """
    Calls the perception agent with the given query.
    """
    try:
        response = Perceptor.run(user_input=query)
        logger.info("Perception Agent Response: " + json.dumps(response, indent=2))
        return response['final_response']
    except Exception as e:
        print("Error in perception agent:", str(e))
        return f"Error in perception agent: {str(e)}"
    
def call_executor_agent(query: str):
    """
    Calls the executor agent with the given list of actions. Actions can include opening a webpage with a URL, clicking on elements or a list of elements,
    typing text into elements([{id1:text},{id2:text}]) etc.
    """
    try:
        response = Executor.run(user_input=query)
        logger.info("Executor Agent Response: " + json.dumps(response, indent=2))
        return response['final_response']
    except Exception as e:
        print("Error in executor agent:", str(e))
        return f"Error in executor agent: {str(e)}"

Orchestrator = Agent(
    llm_client=OpenRouterClient(),
    system_prompt="""
        You are an orchestrator agent that coordinates between the perception and executor agents to fulfill
        user requests related to web navigation and interaction.
        Delegate tasks to the perception agent when information about the webpage is needed,
        and to the executor agent for performing actions on the webpage.
        Ensure that the instructuions given to the agents are clear and concise.
        The arguments to be passed to the executor should contain exact element ids as provided by the perception agent
        and the type of action to be performed on the element.
    """,
    tools=[
        call_executor_agent,
        call_perception_agent
    ],
    max_steps=50,
    max_retries=2,
    reasoning=False,
    show_thinking=True,
)




while True:
    user_input = input("YOU: ")
    if user_input.lower() == 'exit':
        break
    response = Orchestrator.run(user_input=user_input)
    print("AGENT:", response['final_response'])












"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary

Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill my date of birth 3 jan 2004.
"""


# navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
# print(perception_tools.take_snapshot())

