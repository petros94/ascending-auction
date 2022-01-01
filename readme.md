# Implementation of the Ascending Auction algorithm for Decentralized Scheduling

Task allocation is a common problem found in everyday life. Examples include organizing a project’s plan to meet specific 
deadlines or allocating CPU time for executing user programs.  The problem essentially boils down to orchestrating the 
allocation of a shared resource used to carry out tasks, in such a way that the value produced by completing these tasks is maximized.  

In this repo we examine the application of the ascending auction algorithm in solving a certain task allocation problem, known as the scheduling problem.

While optimality is not guaranteed, in our experiments we observed that most of times the algorithm converges to an adequate solution. 
Combined with the distributed nature and easy scaling, the algorithm stands as a strong alternative among others, in solving such type of problems.

You can read more about the algorithm in my paper included in the repo.

## The code

I recommend you to run the *demo.ipynb* notebook for testing out the code.

### Ascending Auction

The file *auction.py* contains the implementation of the ascending auction.

The *AuctionBoard* is like a literal task allocation board, which includes the current allocations of the tasks. 
Agents are informed from the board about the current allocation state, and communicate back their changes.
The specific board is passive, in a sense that all the scheduling logic is carried out by the agents and not the board.
Thus the solution is decentralized.

The *AuctionAgent* is a representation of the agents. The class contains a *bid* method which holds the bidding logic. 
Each agent can and should run on a separate machine.

### Priority First

The file *priority_first.py* contains the implementation of the priority first algorithm. 
It uses a greedy logic to allocate the tasks with the highest utility first, closest to their deadline.

### Weighted Job Schedule

The file *weighted_job_schedule.py* contains the implementation of the weighted job schedule algorithm. 
It uses dynamic programming to allocate the tasks avoiding overlaps.

### Brute Force

The file *brute_force.py* contains the implementation of the brute force algorithm. 
It is recommended to run this algorithm only for small problem sizes, since it tries all the potental allocations to find the best one.
It should be used for benchmarking only, to provide a baseline for comparison.

