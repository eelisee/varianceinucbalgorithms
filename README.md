# Introduction to Bandit Algorithms
Exploration-Exploitation Trade-Off of Bandit Algorithms in Comparison

This repository contains simulations of three bandit algorithms: Explore-then-Commit (ETC), epsilon-greedy, and Upper Confidence Bound (UCB). Below is a brief overview of each algorithm's functionality:

- **ETC (Explore-then-Commit)**: This algorithm initially explores all available arms for a certain number of rounds and then commits to the arm with the highest estimated reward.

- **Epsilon-Greedy**: The epsilon-greedy algorithm balances exploration and exploitation by choosing a random action with probability epsilon and the action with the highest estimated reward with probability 1-epsilon.

- **UCB (Upper Confidence Bound)**: UCB algorithm estimates the upper confidence bound for each arm's reward and selects the arm with the highest upper confidence bound for exploitation.

The arms in the bandit model are simulated using Bernoulli random variables. Specifically, the arms are designed to have expected rewards close to each other, as discussed in Chapter 1, to challenge the UCB algorithm's ability to differentiate between optimal and suboptimal arms.

Each algorithm is run for 100 rounds, and the results are stored in separate directories for different time steps. Additionally, there is a 'results_average' file for each algorithm, providing the average values for each time step based on 100 samples.

Visualizations and dashboards were created using Plotly and Dash. There are two dashboards available:

1. **Main Dashboard**: This dashboard contains three plots:
   - Total reward over the number of time steps for each algorithm (logarithmic scale).
   - Total regret over the number of time steps for each algorithm (logarithmic scale).
   - Number of optimal arm pulls over the number of time steps for each algorithm (logarithmic scale).

2. **Comparison Dashboard**: This dashboard compares the frequency of 0s and 1s drawn by each algorithm at time step 100. This comparison is essential as it reflects not only the influence of the optimal arm but also the potential positive influence of suboptimal arms.

The algorithms were rigorously cross-validated by examining metrics such as regret relative to the number of pulls of suboptimal arms and the frequency of 1s drawn compared to the total reward.

For further details on the algorithms, simulation setup, and visualizations, please refer to the corresponding sections in the associated research paper.







