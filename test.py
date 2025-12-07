from Navigation.playwright_tools import open_page, click_element, type_in_element, press_key, get_element
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.GroqClient import GroqClient
from agent_pipeline.Agent.GeminiClient import GeminiClient
from agent_pipeline.Agent.OpenRouterClient import OpenRouterClient

tools = [open_page, click_element, type_in_element, press_key, get_element]
agent = Agent(
    llm_client=OpenRouterClient(),
    tools=tools, 
    max_iterations=10, 
    show_thinking=True,
    system_prompt="You are a helpful AI assistant."  
    )

while True:
    user_query = input("You: ")
    if user_query.lower() == "exit":
        break
    result = agent.run(user_query)
    print(f"Agent: {result['final_response']}")