import json
from test.linkedin import LinkedInTools
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.Clients.GroqClient import GroqClient
from agent_pipeline.Agent.Clients.OpenRouterClient import OpenRouterClient
from agent_pipeline.Agent.Clients.GeminiClient import GeminiClient
from agent_pipeline.Agent.Clients.GithubClient import GitHubModelsClient
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigation import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element import ElementStore
from agent_pipeline.utils.logger import Logger
from Navigation.DomMemoryManager import DOMAwareMemoryManager

from test.resumeParser import parse_resume

session = BrowserManager(headless=False)
navigation_tools = NavigationTools(session)
element_store = ElementStore()
shared_memory = DOMAwareMemoryManager(history_window=4, scratchpad_window=6)  
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store, perception_tools,file_path="Resume.pdf")
logger = Logger()

resume_text = ""
def get_resume_contents()-> str:
    """
    returns the content of the user's resume as a string.
    Can be used to infer for some details that are necessary to fill forms.
    Example: Name, Education, Skills, Date of Birth, Email, Phone Number, etc.
    """
    return resume_text

resume_text = parse_resume("Resume.pdf")

LINKED_AGENT_PROMPT="""
You are an expert Job Application Agent. You are applying for a job on behalf of the user.

**USER CONTEXT (IMMUTABLE TRUTH):**
    "name": "Sudheer Nandhan",
    "phone": "7874134312", 
    "phone_country_code": "India (+91)",
    "email": "mainproject3563@gmail.com",
    "current_location": "Kerala, India",
    "willing_to_relocate": "Yes",
    "total_experience_years": "0", 
    "current_ctc": "0",
    "expected_ctc": "1000000",
    "notice_period_months": "0",
    "skills": ["Python", "Java", "AWS", "Azure", "GCP", "Git", "Machine Learning"]

**GOAL:** You must complete the ENTIRE application process until the "Application sent" confirmation appears.

**DEFINITION OF DONE (CRITICAL):**
You are **FORBIDDEN** from outputting a <final_answer> until:
1. You have clicked "Submit application".
2. You see the text "Application sent" or a green checkmark indicating success.
3. You have dismissed the success popup.

**PROTOCOL:**
1. **Analyze:** Check the snapshot.
2. **Action:** - If "Easy Apply" -> Click it.
   - If "Next" or "Continue" or "Review" -> Click it.
   - If "Submit application" -> Click it.
   - If Form Fields -> Fill using USER CONTEXT.
3. **Multi-Page Handling:** - If you click "Next" and the page doesn't change, **CHECK FOR ERRORS** (red text) and fix them.
   - If you see "Please enter a valid answer", look for empty required fields (marked with *) or dropdowns you missed.

**CRITICAL RULES FOR FORM FILLING:**
1. **SMART DROPDOWN STRATEGY (Combobox vs Select):**
   - **Case A: Searchable Fields (Location, Job Title, Skills)**
     *Identified as:* `combobox` or `textbox` in snapshot.
     *Action:* 1. **Type** the value (e.g., "Kerala").
     2. **Wait** for the list to appear.
     3. **Click** the matching option OR press **Enter**.
   
   - **Case B: Fixed Dropdowns (Yes/No, Country Code)**
     *Identified as:* `listbox` or `select` or has a clear arrow icon.
     *Action:*
     1. **Click** the trigger.
     2. **Select** the option.

2. **PERSISTENCE:**
   - Do NOT stop after filling one page. 
   - Do NOT stop after uploading the resume.
   - You must keep looping (Snapshot -> Action) until the application is SUBMITTED.

3. **NUMERIC FIELDS (CTC/Experience):**
   - The user context provides "0" or "1000000". 
   - **RULE:** If the field asks for "Years", enter just the number (e.g., "2").
   - **RULE:** If the field asks for "Lacs", convert accordingly (e.g., "1000000" -> "10"). 
   - **ERROR PREVENTION:** Do not add symbols like "," or "$". Use pure decimals (e.g., "2.5").

4. **STRICT ID ENFORCEMENT:** - Use ONLY IDs from the *current* snapshot.

5. **ERRORS:**
   - If you get stuck on a page for >2 turns, try clicking the "Review" or "Next" button again, or check for missed fields.
"""

SYSTEM_PROMPT_TEMPLATE = """
You are an expert Job Application Agent. You are applying for a job on behalf of the user.

**USER CONTEXT (IMMUTABLE TRUTH):**
    "phone": "+91 7874134312",
    "current_location": "Kerala, India",
    "willing_to_relocate": "Yes",
    "total_experience_years": "0", # Use strings for easier form typing
    "current_ctc": "0",
    "expected_ctc": "1000000",
    "notice_period_months": "0",
    "skills": ["Python", "Java", "AWS", "Azure", "GCP", "Git", "Machine Learning"],
    "linkedin_profile": "https://www.linkedin.com/in/..."

**PROTOCOL:**
1. **Analyze:** Check the current page snapshot.
2. **Action:** - If "Easy Apply" is visible -> Click it.
   - If form fields are visible -> Fill them using USER CONTEXT.
   - If a file upload is needed -> Use `upload_file`.
   - If "Review" or "Submit" -> Click it.

**CRITICAL RULES FOR FORM FILLING:**
1. **DROPDOWNS:** - NEVER type into a dropdown. 
   - Step A: Click the dropdown trigger (e.g., "Phone country code").
   - Step B: WAIT for the list to appear (take a new snapshot).
   - Step C: Click the option that matches USER CONTEXT (e.g., "India (+91)").
   - *Failure Fix:* If the exact text isn't there, pick the closest logical match (e.g., "Yes" for relocation).
    -if there is a default value and if that value is correct then skip that field and move on to the next one 

2. **NUMERIC FIELDS (CTC/Experience):**
   - The user context provides "0" or "1000000". 
   - **RULE:** If the field asks for "Years", enter just the number (e.g., "2").
   - **RULE:** If the field asks for "Lacs", convert accordingly (e.g., "1000000" -> "10"). 
   - **ERROR PREVENTION:** Do not add symbols like "," or "$". Use pure decimals (e.g., "2.5").

3. **STRICT ID ENFORCEMENT:** - Use ONLY IDs from the *current* snapshot.

4. **UNKNOWN QUESTIONS:**
   - If a question is not in USER CONTEXT (e.g., "Do you have a driver's license?"), infer if possible using the get_resume_contents function.
   - If still unknown, default to "Yes" for eligibility questions and "0" for numeric fields to avoid blocking.
    - If the field or question is optional and if you dont know the answer, skip it
WORKFLOW:
    for each job, click easy apply, fill only phone number and continue using next button.
    upload resume, fill any additional fields if necessary and submit fianallys 
"""

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
-Phone number = +91 7874134312
"""
"""
unified_agent = Agent(
    llm_client = GitHubModelsClient(),
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
"""
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
"""
while True:
    user_input = input("YOU: ")
    if user_input.lower() == 'exit':
        break
    
    response = unified_agent.run(user_input=user_input)
    logger.info(f"Response: {response}")
    print("AGENT:", response['final_response'])
"""
"""
navigation_tools.open_page("https://docs.google.com/forms/d/e/1FAIpQLSeIIOkuFqPagjWMam4HcxOLzgdtYfdWELNhtVombwUrEpXSew/viewform?usp=publish-editor")
perception_tools.take_snapshot()
print(action_tools.upload_file("7"))
"""
"""
import time
navigation_tools.open_page("https://www.linkedin.com/jobs/search")

time.sleep(5)
perception_tools.take_snapshot()
action_tools.click_elements(['29'])
# 2. Extract job posting IDs using your new tool
job_tools = LinkedInTools(element_store)
postings = job_tools.get_job_posting_ids(limit=5)

print(postings)  # Debug: Check extracted postings

# Define the set of tools the "Application Agent" will need
application_tools = [
    perception_tools.take_snapshot,
    action_tools.click_elements,
    action_tools.type_in_elements,
    action_tools.upload_file,
    get_resume_contents
]

# 3. Iterate through postings
for post in postings:
    print(f"\n\n--- Starting Application for: {post['job_title']} ---\n\n")
    
    # Select the job to load the right-hand pane
    action_tools.click_elements([post['element_id']])
    time.sleep(3) # Wait for UI to stabilize
    
    # 4. Create a NEW Agent instance for THIS specific job
    # This wipes history/scratchpad for a fresh start
    app_agent = Agent(
        llm_client=GeminiClient(),  
        tools=application_tools,
        system_prompt=LINKED_AGENT_PROMPT,
        max_steps=25, # Give it enough steps to navigate multi-page forms
        reasoning=True,
        show_thinking=True,
        memory_manager=DOMAwareMemoryManager(history_window=6, scratchpad_window=8)
    )
    application_task = f"Apply for the current job: {post['job_title']}. Use 'Easy Apply' if available."
    result = app_agent.run(user_input=application_task)
    
    print(f"Result for {post['job_title']}: {result['final_response']}")
    print("-" * 50)
    print("\n\n\n")
"""
"""
import time
navigation_tools.open_page("https://www.linkedin.com/jobs/search")
time.sleep(5)
print(perception_tools.take_snapshot())
time.sleep(5)
filtering_agent = new Agent(
    llm_client=GroqClient(),
    tools=[],

)
time.sleep(20)
print(perception_tools.take_snapshot())
#time.sleep(5)
#print(action_tools.click_elements(['14']))
#time.sleep(3)
#perception_tools.take_snapshot()
#time.sleep(3)
time.sleep(400)
"""
