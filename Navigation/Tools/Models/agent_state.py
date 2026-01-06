class AgentState:
    def __init__(self, goal: str):
        self.goal = goal
        self.snapshot = None
        self.plan = None
        self.last_error = None
        self.done = False
        self.final_response = None
