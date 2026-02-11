import time
import json
import re
from test.linkedin import LinkedInTools
from test.resumeParser import parse_resume
from agent_pipeline.Agent.Agent import Agent
from agent_pipeline.Agent.Clients.GithubClient import GitHubModelsClient
from agent_pipeline.Agent.Clients.GeminiClient import GeminiClient # Or whichever you prefer
from Navigation.Tools.actions import ActionTools
from Navigation.Tools.perception import PerceptionTools
from Navigation.Tools.navigation import NavigationTools
from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element import ElementStore
from agent_pipeline.utils.logger import Logger
from Navigation.DomMemoryManager import DOMAwareMemoryManager

# --- CONFIGURATION ---
USER_CONTEXT = {
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
}

# --- INITIALIZATION ---
session = BrowserManager(headless=False)
navigation_tools = NavigationTools(session)
element_store = ElementStore()
perception_tools = PerceptionTools(session, element_store)
action_tools = ActionTools(session, element_store, perception_tools, file_path="Resume.pdf")
job_tools = LinkedInTools(element_store)
logger = Logger()

# Load Resume Context
resume_text = parse_resume("Resume.pdf")

# --- PROMPTS ---

# 1. WORKER AGENT PROMPT (The "Doer")
WORKER_PROMPT = """
You are a specialized Job Application Worker. Your ONLY goal is to apply to the currently selected job.

**USER DATA:**
{user_context}

**PROTOCOL:**
1. Check if "Easy Apply" is visible. If not, report "Not Easy Apply" and STOP.
2. Click "Easy Apply".
3. Fill the form using User Data.
   - **Comboboxes (Location/Experience):** TYPE the value (e.g. "Kerala"), WAIT, then CLICK the option.
   - **Radio Buttons:** FORCE CLICK them if standard click fails.
   - **Uploads:** Use `upload_file` for Resume.
4. Click "Next" / "Review" / "Submit".
5. **CRITICAL:** Do NOT stop until you see "Application sent" or have successfully submitted.

**ERROR RECOVERY:**
- If a click fails, assume it's an overlay and try again.
- If you see "Please enter a valid answer", check for skipped required fields.
"""

# 2. ORCHESTRATOR AGENT PROMPT (The "Boss")
ORCHESTRATOR_PROMPT = """
You are the Headhunter Orchestrator. You control the browser to find jobs and assign them to Workers.

**YOUR TOOLS:**
- `open_page(url)`: Go to LinkedIn.
- `click_elements(ids)`: Click filters (like "Easy Apply" button).
- `get_job_posting_ids(limit)`: Returns a list of job IDs on the current page.
- `apply_to_job_wrapper(job_id, job_title)`: **DELEGATE** the application to a Worker Agent.

**YOUR MISSION:**
1. Open "https://www.linkedin.com/jobs/search".
2. Take a snapshot to see the page.
3. **Filter Results:** Find and click the "Easy Apply" filter button.
4. **Get Jobs:** Use `get_job_posting_ids` to get the top 5 jobs.
5. **Loop:** For each job ID you found:
   - Call `apply_to_job_wrapper(job_id, job_title)`.
   - Read the result returned by the worker.
6. Stop when you have attempted 5 applications.
"""

# --- HELPER FUNCTIONS ---

def reset_ui():
    """
    Cleanup function to close any lingering modals before the next agent starts.
    This prevents the 'infinite loop' of agents getting stuck on the previous job's popup.
    """
    print("--- [SYSTEM] Cleaning UI State ---")
    try:
        # Refresh snapshot to see if a modal is open
        perception_tools.take_snapshot()
        
        # Look for a "Dismiss" or "Close" button (Usually an SVG or button with 'Dismiss' text)
        # This is a heuristic; you might need to adjust based on specific IDs found in your DOM
        targets = [el.id for el in element_store.all() if "Dismiss" in (el.name or "") or "Close" in (el.name or "")]
        
        if targets:
            print(f"Closing lingering modal (IDs: {targets})")
            action_tools.click_elements([targets[0]]) # Click the first one found
            time.sleep(1)
            
            # Check for "Discard" confirmation popup
            perception_tools.take_snapshot()
            discard_targets = [el.id for el in element_store.all() if "Discard" in (el.name or "")]
            if discard_targets:
                action_tools.click_elements([discard_targets[0]])
                time.sleep(1)
    except Exception as e:
        print(f"UI Reset warning: {e}")

# --- CUSTOM TOOL WRAPPER ---

def apply_to_job_wrapper(job_id: str, job_title: str) -> str:
    """
    Spawns a Worker Agent to handle the specific application logic for one job.
    """
    print(f"\n >>> [ORCHESTRATOR] Delegating Job: {job_title} (ID: {job_id})")
    
    # 1. Click the job listing to load the details pane
    action_tools.click_elements([job_id])
    time.sleep(3) # Give LinkedIn time to load the right pane
    
    # 2. Create the specialized Worker Agent
    # We create a fresh instance so it has clean memory
    worker_agent = Agent(
        llm_client=GeminiClient(), 
        tools=[
            perception_tools.take_snapshot,
            action_tools.click_elements,
            action_tools.type_in_elements,
            action_tools.upload_file
        ],
        system_prompt=WORKER_PROMPT.format(user_context=json.dumps(USER_CONTEXT)),
        max_steps=20, # Give it enough room for multi-page forms
        reasoning=True,
        show_thinking=True,
        memory_manager=DOMAwareMemoryManager(history_window=8, scratchpad_window=10)
    )
    
    # 3. Run the Worker
    try:
        result = worker_agent.run(f"Apply to the job: {job_title}")
        status = result.get('final_response', 'No response')
    except Exception as e:
        status = f"Worker Crashed: {str(e)}"
    
    print(f" <<< [WORKER FINISHED] Result: {status}")
    
    # 4. Mandatory Cleanup
    reset_ui()
    
    return status

# --- MAIN EXECUTION ---

# Define tools available to the Orchestrator
orchestrator_tools = [
    navigation_tools.open_page,
    perception_tools.take_snapshot,
    action_tools.click_elements, # Needed to click the "Easy Apply" filter
    job_tools.get_job_posting_ids,
    apply_to_job_wrapper # The Delegator Tool
]

# Create the Orchestrator Agent
orchestrator = Agent(
    llm_client=GeminiClient(),
    tools=orchestrator_tools,
    system_prompt=ORCHESTRATOR_PROMPT,
    max_steps=15, # Orchestrator needs fewer steps than workers
    reasoning=True,
    show_thinking=True
)



if __name__ == "__main__":
    
    while True:
        user_input = input("YOU: ")
        if user_input.lower() == 'exit':
            break
    
        try:
            response = orchestrator.run(user_input=user_input)
            logger.info(f"Response: {response}")
            print("AGENT:", response['final_response'])
        except KeyboardInterrupt:
            print("Stopped by user.")
    
