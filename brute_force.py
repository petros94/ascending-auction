import itertools

import numpy as np
from numpy import arange
from pandas import DataFrame

from agents import Agent


class BruteForceBoard:
    def __init__(self, resource_allocation):
        self.resource_allocation = resource_allocation

    def get_allocations(self):
        return self.resource_allocation

    def allocate_slots(self, agents):
        global_optimal_value = -1
        global_optimal_allocation = None
        for L in range(len(agents)+1):
            for subset in itertools.combinations(agents, L):
                optimal_allocation, subset_optimal_value = self.optimal_allocation(subset, self.resource_allocation)
                if global_optimal_value < subset_optimal_value:
                    global_optimal_value = subset_optimal_value
                    global_optimal_allocation = optimal_allocation

        return global_optimal_allocation, global_optimal_value

    def optimal_allocation(self, agents, current_allocation):
        if len(agents) == 0:
            return current_allocation, 0

        current_agent = agents[0]
        remaining_agents = agents[1:] if len(agents) > 1 else []
        max_total_utility = 0
        best_allocation = current_allocation

        for k in range(0, current_agent.deadline-current_agent.duration+1):
            next_allocation = current_allocation.copy()

            if np.all(next_allocation.loc[k:k+current_agent.duration-1, "agent"] == -1):
                next_allocation.loc[k:k+current_agent.duration-1, "agent"] = current_agent.agent_id

                next_best_allocation, optimal_utility = self.optimal_allocation(remaining_agents, next_allocation)

                next_total_utility = current_agent.utility + optimal_utility

                if max_total_utility < next_total_utility:
                    max_total_utility = next_total_utility
                    best_allocation = next_best_allocation

        return best_allocation, max_total_utility

if __name__ == "__main__":
    agents = [
        Agent(agent_id=0, deadline=4, utility=10, duration=2),
        Agent(agent_id=1, deadline=3, utility=16, duration=2),
        Agent(agent_id=2, deadline=3, utility=6, duration=1),
        Agent(agent_id=3, deadline=8, utility=14.5, duration=4)
    ]

    n_slots = 10
    entry_price = 3
    resource_allocation_board = DataFrame({'slot_id': arange(n_slots), 'agent': [-1]*n_slots, 'bid': [entry_price]*n_slots})
    board = BruteForceBoard(resource_allocation_board)
    print(board.allocate_slots(agents))
