# Python program for weighted job scheduling using Dynamic
# Programming and Binary Search

# Class to represent a job
from numpy import arange
from pandas import DataFrame


class Job:
    def __init__(self, start, finish, profit):
        self.start = start
        self.finish = finish
        self.profit = profit

class Agent:
    def __init__(self, agent_id, deadline, utility, duration):
        self.agent_id = agent_id
        self.deadline = deadline
        self.utility = utility
        self.duration = duration
        self.allocated_slots = []


# A Binary Search based function to find the latest job
# (before current job) that doesn't conflict with current
# job.  "index" is index of the current job.  This function
# returns -1 if all jobs before index conflict with it.
# The array jobs[] is sorted in increasing order of finish
# time.
def binarySearch(agent, start_index):
    # Initialize 'lo' and 'hi' for Binary Search
    lo = 0
    hi = start_index - 1

    # Perform binary Search iteratively
    while lo <= hi:
        mid = (lo + hi) // 2
        if agent[mid].deadline <= agent[start_index].deadline - agent[start_index].duration:
            if agent[mid + 1].deadline <= agent[start_index].deadline - agent[start_index].duration:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1

class WeightedJobSchedulingBoard:
    def __init__(self, resource_allocation):
        self.resource_allocation = resource_allocation

    def get_allocations(self):
        return self.resource_allocation

    def allocate_slots(self, agents):
        # self.resource_allocation.loc[slots, 'agent'] = agent_id
        # self.resource_allocation.loc[slots, 'bid'] = bids

        # Sort jobs according to deadline
        agents = sorted(agents, key=lambda j: j.deadline)

        # Create an array to store solutions of subproblems.  table[i]
        # stores the profit for jobs till arr[i] (including arr[i])
        n = len(agents)
        table = [0 for _ in range(n)]

        table[0] = agents[0].utility

        # Fill entries in table[] using recursive property
        for i in range(1, n):

            # Find profit including the current job
            inclProf = agents[i].utility
            l = binarySearch(agents, i)
            if (l != -1):
                inclProf += table[l]

            # Store maximum of including and excluding
            table[i] = max(inclProf, table[i - 1])

        s = []
        maxUtilities = table[n - 1]

        for i in range(n-1, -1, -1):
            if maxUtilities == table[i]:
                s.append(agents[i].agent_id)
                maxUtilities -= agents[i].utility

        return s, table[n - 1]

if __name__ == "__main__":
    # Driver code to test above function
    agents = [
        Agent(agent_id=0, deadline=4, utility=10, duration=2),
        Agent(agent_id=1, deadline=3, utility=16, duration=2),
        Agent(agent_id=2, deadline=3, utility=6, duration=1),
        Agent(agent_id=3, deadline=8, utility=14.5, duration=4)
    ]


    n_slots = 10
    entry_price = 3
    resource_allocation_board = DataFrame({'slot_id': arange(n_slots), 'agent': [-1]*n_slots, 'bid': [entry_price]*n_slots})
    board = WeightedJobSchedulingBoard(resource_allocation_board)
    print(board.allocate_slots(agents))