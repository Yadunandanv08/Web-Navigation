from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.GroqClient import GroqClient
from agent_pipeline.Agent.GeminiClient import GeminiClient
from agent_pipeline.Agent.OpenRouterClient import OpenRouterClient
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigate import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element_store import ElementStore

session = BrowserManager(headless=False)
session.start()


navigation_tools = NavigationTools(session)
element_store = ElementStore()
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store)

tools = [
            navigation_tools.open_page, 
            navigation_tools.close_browser, 
            perception_tools.take_snapshot, 
            action_tools.click_element,
            action_tools.type_in_element,
            action_tools.press_key
        ]
agent = Agent(
    llm_client=OpenRouterClient(),
    tools=tools, 
    max_iterations=10, 
    show_thinking=True,
    system_prompt="You are a helpful AI assistant that helps users navigate the web using browser automation. Use the provided tools to open web pages, take snapshots of the accessibility tree, click elements, type into elements, and press keys as needed to fulfill user requests."  
    )

while True:
    user_query = input("You: ")
    if user_query.lower() == "exit":
        break
    result = agent.run(user_query)
    print(f"Agent: {result['final_response']}")