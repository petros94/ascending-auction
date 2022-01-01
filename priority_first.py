from functools import reduce

from numpy import arange, all
from pandas import DataFrame, factorize

from agents import Agent

class PriorityBoard:
    def __init__(self, resource_allocation):
        self.resource_allocation = resource_allocation

    def get_allocations(self):
        return self.resource_allocation

    def allocate_slots(self, agents):
        sorted_agents = sorted(agents, key=lambda x: x.utility, reverse=True)

        for agent in sorted_agents:

            for i in range(agent.deadline-agent.duration, -1, -1):
                slots = arange(i, i+agent.duration)

                if all(self.resource_allocation.loc[slots, 'agent'] == -1):
                    self.resource_allocation.loc[slots, 'agent'] = agent.agent_id
                    break

        _, active_agents = factorize(self.resource_allocation.loc[self.resource_allocation.agent != -1, 'agent'])
        return self.resource_allocation, reduce(lambda a, b: a+b, [agents[i].utility for i in active_agents])


if __name__ == "__main__":
    agents = [
        Agent(agent_id=0, deadline=4, utility=10, duration=2),
        Agent(agent_id=1, deadline=3, utility=16, duration=2),
        Agent(agent_id=2, deadline=3, utility=6, duration=1),
        Agent(agent_id=3, deadline=8, utility=14.5, duration=4)
    ]

    n_slots = 10
    entry_price = 3
    resource_allocation_board = DataFrame({'slot_id': arange(n_slots), 'agent': [-1]*n_slots})
    board = PriorityBoard(resource_allocation_board)
    print(board.allocate_slots(agents))