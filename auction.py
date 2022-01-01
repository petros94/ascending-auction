import time
from functools import reduce

import numpy as np
from pandas import DataFrame
from numpy import arange, argmax

from agents import Agent

class AuctionAgent(Agent):
    def __init__(self, agent_id, deadline, utility, duration):
        super().__init__(agent_id, deadline, utility, duration)
        self.allocated_slots = []
        self.dropout = False

    def bid(self, board, agents):
        if self.dropout:
            return

        alloc_board = board.get_allocations()
        min_bid = board.get_min_bid()

        alloc_slots = alloc_board.loc[alloc_board.agent == self.agent_id, 'slot_id']

        if 0 < len(self.allocated_slots) == len(alloc_slots):
            return

        # Generate potential slot subsets and valuations
        max_valuation = -1
        best_allocation = {}
        for i in range(0, self.deadline - self.duration + 1):

            slots = arange(i, i+self.duration)
            bids = []

            for j in range(i, i+self.duration):
                bid = alloc_board.loc[j, 'bid']

                if alloc_board.loc[j, 'agent'] != self.agent_id:
                    bid += min_bid

                bids.append(bid)

            valuation = self.utility - sum(bids)

            if valuation > max_valuation:
                best_allocation = {
                    'slots': slots,
                    'bids': bids,
                    'valuation': valuation
                }
                max_valuation = valuation

        # Exit if utility < 0
        if max_valuation < 0:
            self.allocated_slots = alloc_slots
            self.dropout = True
            return

        # Update board and self
        board.allocate_single_agent(self.agent_id, best_allocation['slots'], best_allocation['bids'])
        self.allocated_slots = best_allocation['slots']


class AuctionBoard:
    def __init__(self, resource_allocation, min_bid):
        self.resource_allocation = resource_allocation
        self.min_bid = min_bid
        # self.active_agents = []
        self.reallocations = 0

    def get_allocations(self):
        return self.resource_allocation

    def get_min_bid(self):
        return self.min_bid

    def allocate_single_agent(self, agent_id, slots, bids):
        # other_agents = self.resource_allocation.loc[slots, 'agent'].to_list()
        # for i in other_agents:
        #     if i >= 0 and i in self.active_agents:
        #         self.active_agents.remove(i)

        self.resource_allocation.loc[slots, 'agent'] = agent_id
        self.resource_allocation.loc[slots, 'bid'] = bids
        # self.active_agents.append(agent_id)
        self.reallocations += 1

    def allocate_slots(self, agents):
        iterations = 0
        while True:
            iterations += 1
            last_resource_allocation = self.get_allocations().bid.copy()

            for agent in agents:
                agent.bid(self, agents)

            if np.all(last_resource_allocation == self.get_allocations().bid):
                break

        return self.resource_allocation, reduce(lambda a, b: a+b, [i.utility if not i.dropout else 0 for i in agents])


if __name__ == "__main__":
    n_slots = 10
    entry_price = 3
    resource_allocation_board = DataFrame({'slot_id': arange(n_slots), 'agent': [-1]*n_slots, 'bid': [entry_price]*n_slots})
    board = AuctionBoard(resource_allocation_board, 0.25)

    agents = [
        AuctionAgent(agent_id=0, deadline=4, utility=10, duration=2),
        AuctionAgent(agent_id=1, deadline=3, utility=16, duration=2),
        AuctionAgent(agent_id=2, deadline=3, utility=6, duration=1),
        AuctionAgent(agent_id=3, deadline=8, utility=14.5, duration=4)
    ]

    print(board.allocate_slots(agents))





