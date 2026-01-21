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
# from Navigation.playwright_tools import open_page, get_element, click_element, type_in_element, press_key

session = BrowserManager(headless=False)

navigation_tools = NavigationTools(session)
element_store = ElementStore()
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store)


# perception_agent = Agent(
#     llm_client=OpenRouterClient(model_name="xiaomi/mimo-v2-flash:free"),
#     tools = [perception_tools.take_snapshot],
#     max_iterations=25,
#     show_thinking=True,
#     system_prompt="""
#         You are the perception agent responsible for observing and interpreting the current web page.

#         You MUST use the take_snapshot tool to:
#         - Capture the latest accessibility tree
#         - Populate the ElementStore with interactive elements
#         - Identify elements needed for downstream actions

#         Your task is to return element_ids from the ElementStore, not selectors.

#         Rules:
#         - Call take_snapshot before making any claims
#         - Use element role and name to choose elements
#         - Prefer stable, clearly labeled interactive elements

#         If multiple elements match:
#         - Return multiple candidates
#         - Explain differences briefly
#         - Recommend the safest option

#         Response format:
#         status: SUCCESS | FAILURE(with reason)
#         outputs:
#         element_id: <string>
#         confidence: <0.0-1.0>
#         or
#         outputs:
#         candidates: [ {element_id, role, name} ]


#         If only observation is requested, provide a concise summary of the page content. 
#     """
# )

# execution_agent = Agent(
#     llm_client=GroqClient(),
#     tools = [
#                 navigation_tools.open_page,
#                 action_tools.click_element,    
#                 action_tools.type_in_element, 
#                 action_tools.press_key, 
#                 # action_tools.mark_checked, 
#                 action_tools.set_date
#             ],
#     max_iterations=25,
#     show_thinking=True,
#     system_prompt="""
#         You are the execution agent responsible for performing actions on the web page.

#         You can only act using the provided tools!

#         Rules:
#         - Only act when all required inputs are provided
#         - Do NOT guess element_ids
#         - Execute exactly the logical action per instruction
#         - Report the tool result faithfully

#         After execution:
#         - Return the success or failure information.

#         Response format:
#         status: SUCCESS | FAILURE
#         reason: <failure_reason if any>

#         """
# )

# def call_perception_agent(query: str):
#     """
#     Calls the perception agent with the given query.
#     """
#     result = perception_agent.run(query)
#     return result['final_response']

# def call_execution_agent(instruction: str, element_id: str=None, input_text: str = None):
#     """
#     Calls the execution agent with the given instruction(such as opening a page or performing an action) and or element_id.
#     """

#     tool_input = {
#         "instruction": instruction,
#         "element_id": element_id,
#         "input_text": input_text
#     }
#     result = execution_agent.run(tool_input)
#     return result['final_response']


# Orchestrator = Agent(
#     llm_client = OpenRouterClient(model_name="deepseek/deepseek-r1-0528:free"),
#     tools = [call_execution_agent, call_perception_agent],
#     max_iterations=25,
#     show_thinking=True,
#     system_prompt="""
#         You are the orchestrator agent for a multi-agent web navigation system.

#         Your responsibility is to:
#         - Understand the user goal
#         - Create a high-level plan
#         - Decide which agent to delegate to
#         - Track intermediate artifacts (plans, element_ids, failures)
#         - Route outputs between agents correctly
#         - Decide when to retry, replan, or stop

#         Available agents:
#         2. Perception Agent - observes the page and provides any required details, observations or returns element_ids of elements for required actions as needed.
#         3. Execution Agent - performs actions using provided element_ids or inputs

#         Before delegating, decide:
#         - Which agent is needed (perception, execution)
#         - What outputs are required from that agent
#         - What failure signals require replanning

#         Artifact handling rules:
#         - element_ids returned by Perception Agent must be passed unchanged to Execution Agent
#         - Failures must be classified using short reason codes

#         Failure handling:
#         - Retry a failed agent once with clarified instructions
#         - Never loop indefinitely on the same step
#         - Replan if repeated failures occur

#         Stop execution when:
#         - The user goal is achieved
#         - Maximum retries are exceeded

#         Agents must respond using:
#         status, reason (if failure), outputs (if success)

#         ### THE "REALITY GAP" PROTOCOL
#         1. **Thoughts ≠ Actions:** Describing an action in your thought process (e.g., "I will click the button") does NOT make it happen. 
#         2. **Tool Output is the Only Proof:** You can only confirm an action is complete when you receive a concrete output/log from the `call_execution_agent` tool.
#         3. **No Batch Hallucination:** If a plan requires multiple distinct interactions (e.g., filling 3 fields, clicking 2 links), you must execute them individually (or via a batch tool) and **wait for the tool output** for each.

#         ### COMPLETION CRITERIA
#         You are strictly FORBIDDEN from outputting a Final Response or claiming "Task Complete" until:
#         1. You have delegated the necessary actions to the Execution Agent.
#         2. You have received a "SUCCESS" or data payload return from the Execution Agent for those specific actions.

#     """
# )




Orchestrator = Agent(
    llm_client = OpenRouterClient(model_name="tngtech/deepseek-r1t2-chimera:free"),
    tools = [
        navigation_tools.open_page, 
        perception_tools.take_snapshot, 
        action_tools.click_element, 
        perception_tools.retrieve_element,
        action_tools.type_in_element, 
        action_tools.set_date,
        action_tools.execute_batch
    ],
    max_iterations=25,
    show_thinking=True,
    system_prompt="""
        You are a precise Web Navigation Agent. Follow this EXACT sequence:
        1. Call open_page.
        2. Call take_snapshot.
        3. IMMEDIATELY use the IDs from the snapshot to call execute_batch.
    
        CRITICAL: Do not describe your plan more than once. If you have the IDs, you MUST call execute_batch in your very next turn. 
        If you output <thinking> without a <tool_call> while you have work pending, you are failing the task.
    """
    #system_prompt="""
    #    You are a high-efficiency Web Navigation Agent.
   # 
   #     NO BLIND ACTIONS:
   #     1. Open & Map: Use open_page followed by take_snapshot. 
   #     2. Analyze the Summary: take_snapshot will return a list of labels and roles it found. Use this to understand the form's requirements (e.g., "I see it asks for Name, Age, and Gender").
   #     3. Targeted Retrieval: Use retrieve_element ONLY for the labels you confirmed exist in the summary. For example, if the summary shows "textbox: 'Full Name'", call retrieve_element(query="Full Name").
   #     4. Batch Execute: Once you have the IDs, use execute_batch to fill the fields.
   # """
    #system_prompt="""
#        You are a high-efficiency Web Navigation Agent. 
#
 #       ### STRATEGY FOR FORMS:
  #      1. **See:** Call `take_snapshot` to understand the page structure and see all available fields.
   #     2. **Retrieve:** Use `retrieve_element` for each field you need to fill to get their specific IDs.
    #    3. **Batch Execute:** Instead of calling 'type' five times, construct a list of actions and call `execute_batch`. 
     #      Example: 
      #     <tool_call>
       #    {"name": "execute_batch", "arguments": {"actions": [
        #       {"type": "type", "id": "5", "text": "John Doe"},
         #      {"type": "type", "id": "8", "text": "john@example.com"},
          #     {"type": "click", "id": "12"}
           #]}}
       #    </tool_call>
#
 #       This approach avoids the "reality gap" by ensuring you have the "map" (snapshot) before you act, and it saves massive amounts of tokens by grouping your "hands" (actions) together.
  #  """
    #system_prompt="""
     #       You are a high-efficiency Web Navigation Agent. Your goal is to complete tasks with the minimum number of snapshots to save tokens and time.

            ### OPERATIONAL PROTOCOL:
    #        1. **Explore (The Map):** After opening a page, call `take_snapshot` ONCE. This tool reads the entire page, stores interactive elements in a vector database, and returns a high-level summary of what fields and buttons exist.
    #        2. **Plan (The Route):** Based on the snapshot summary, create a mental list of every field you need to interact with (e.g., "I see a Name field, an Email field, and a Submit button").
    #        3. **Retrieve (The Focus):** Instead of taking new snapshots to "see" a field, use the `retrieve_element` tool. Provide a natural language query like "find the email input box" or "find the submit button". This will return the specific `element_id` you need.
     #       4. **Execute (The Action):** Use the retrieved `element_id` to perform actions like `type_in_element` or `click_element`.
     #       5. **Verify:** Only take a second snapshot if you believe the page has changed significantly (e.g., navigating to a new URL or a multi-page form).

            ### HANDLING LARGE FORMS:
      #      - Do not act blindly. Use the summary from the initial `take_snapshot` to understand the form's structure.
    #        - If the summary mentions many fields, retrieve the IDs for all of them first, then execute your actions in a batch-like sequence.
        
            ### GOAL:
    #        Complete the user's request accurately while treating `take_snapshot` as a last resort for updates.
    #   """
   # system_prompt="""
   #     You are a web navigation agent. You will be given a hogh level task by the user which u will accomplish 
   #     by using the provided tools to interact with web pages. Break the task down to smaller steps if needed 
   #     to complete the task successfully.
#
    #"""
)
#"""
while True:
    user_query = input("You: ")
    if user_query.lower() == "exit":
        break
    result = Orchestrator.run(user_query)
    print(f"Orchestrator: {result['final_response']}\n\n")
    print(f"[debug] history: {result['history']}\n\n")
#"""
"""
Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill it. im yadunandan, email:yadunandanv08@gmail.com, phone: 6238922215, final year student btech cs, i know python and java, aws, azure, gcp, good with git, and an ml engineer, i expect 1000000 salary

Open this google form https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog and fill my date of birth 3 jan 2004.
"""


#navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSe_nn_5k-5-GMe5h6J9lF_-G8wuluhGSGWh10frU_nOn7tDOQ/viewform?usp=dialog")
#print(perception_tools.take_snapshot())
#print(perception_tools.retriever.texts)

#print("\n===================\n")
#print(perception_tools.retriever.metadata)
