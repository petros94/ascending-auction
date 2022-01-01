from numpy import arange, sum, argmax

class Agent:
    def __init__(self, agent_id, deadline, utility, duration):
        self.agent_id = agent_id
        self.deadline = deadline
        self.utility = utility
        self.duration = duration
        self.allocated_slots = []