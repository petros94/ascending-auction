from functools import reduce

import numpy as np
from numpy import arange
from pandas import DataFrame

from agents import Agent
from auction import AuctionAgent


def generate_random_agents(n_agents, max_deadline, max_duration, max_utility):
    agents = []

    for i in range(n_agents):
        duration = np.random.randint(max_duration)
        deadline = np.random.randint(duration, max_deadline)
        utility = np.random.randint(max_utility) * duration
        agent = Agent(i, deadline, utility, duration)

        agents.append(agent)

    return agents

def generate_random_auction_agents(n_agents, max_deadline, max_duration, max_utility):
    agents = []

    for i in range(n_agents):
        duration = np.random.randint(1, max_duration)
        deadline = np.random.randint(duration, max_deadline)
        utility = np.random.randint(1, max_utility)
        agent = AuctionAgent(i, deadline, utility, duration)

        agents.append(agent)

    return agents


def generate_configuration(n_agents, max_deadline, max_duration, max_utility, n_slots, entry_price):
    agents = generate_random_auction_agents(n_agents=n_agents,
                                            max_deadline=max_deadline,
                                            max_duration=max_duration,
                                            max_utility=max_utility)

    resource_allocation_board = DataFrame(
        {'slot_id': arange(n_slots), 'agent': [-1] * n_slots, 'bid': [entry_price] * n_slots})

    return agents, resource_allocation_board


def calculate_total_duration(agents):
    return reduce(lambda a, b: a+b, list(map(lambda a: a.duration, agents)))

def calculate_std_duration(agents):
    return np.array(list(map(lambda a: a.duration, agents))).std()