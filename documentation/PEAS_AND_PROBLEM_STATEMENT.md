# Connect Four AI: PEAS Characterization and Problem Formulation

**Course:** ECSCT24301 – Foundation of AI  
**Academic Year:** 2026–27  
**Department:** Computer Science and Engineering (AI-ML), FEST, Adani University  
**Track:** Track A – Applied AI System Development (Game Playing & Adversarial Search)  
**Deliverable:** Week 1 Draft – PEAS Characterization, Problem Statement & Academic Formulation  
**Author:** Team Member 2 (Engineering, GUI & Evaluation)

---

## 1. Problem Statement & Motivation

Board games with large but finite state spaces are a classical proving ground for adversarial search in Artificial Intelligence. The foundational techniques used to solve them—minimax reasoning, alpha-beta pruning, depth-limited heuristic evaluation, and simulation-based search—underlie modern real-world decision systems ranging from superhuman game agents (such as Deep Blue and AlphaGo) to resource-constrained planning under competitive adversaries (e.g., cybersecurity red/blue-team simulations, automated market trading, and strategic negotiation).

This project investigates the design, implementation, and empirical comparison of autonomous decision-making agents for **Connect Four**, a two-player, zero-sum, perfect-information, turn-based board game. Played on a standard vertical 6x7 grid, Connect Four presents an estimated state-space complexity of approximately $4.53 \times 10^{12}$ reachable positions and a game-tree complexity of roughly $10^{21}$. 

While the game mechanics are mathematically transparent, exhaustive brute-force search is computationally intractable beyond shallow depths in real-time play. Consequently, this domain motivates the study of:
1. **Depth-limited adversarial search with heuristic evaluation**, comparing raw Minimax against Alpha-Beta pruning to measure pruning efficiency and state-space collapse.
2. **Statistically driven simulation search**, utilizing Monte Carlo Tree Search (MCTS) with the Upper Confidence Bound applied to Trees (UCT) selection policy.

The primary operational objective of this project is to benchmark the fundamental trade-off between **exact search optimality with heuristic bias** (Alpha-Beta) and **statistical simulation-based approximation** (MCTS) under identical thinking-time and resource constraints.

---

## 2. Agent & Environment Characterization (PEAS)

| Element | Specification |
| :--- | :--- |
| **Performance Measure** | - **Win Rate**: Percentage of victories against baseline and rival agents over multi-game trials.<br>- **Move Quality**: Correlation of chosen moves with deep-search ground truth.<br>- **Decision Latency**: Average and peak wall-clock computation time per move (milliseconds).<br>- **Search Efficiency**: Number of states/nodes expanded (Minimax) or playout simulations performed (MCTS).<br>- **Memory Footprint**: Peak and active RAM allocated during search (`tracemalloc`). |
| **Environment** | A discrete, two-player, zero-sum, turn-based board game played on a standard vertical $6 \times 7$ grid. The state space is bounded, deterministic, static (agents have allocated decision time budgets without external clock drift during contemplation), and sequential. |
| **Actuators** | Column drop action $a \in \{0, 1, 2, 3, 4, 5, 6\}$ indicating the selected non-full column where the player's disc is released, executed via the game engine or interactive interface. |
| **Sensors** | Full read access to the current 2D board state matrix ($6 \times 7$ array containing player pieces: 0 for empty, 1 for Player 1, -1 for Player 2), turn indicator, and history of past moves. |

### Environment Properties Analysis

- **Fully Observable**: At any turn $t$, the agent has complete perceptual access to the exact position of all discs on the board. There is no hidden information or fog-of-war.
- **Deterministic**: An action (dropping a disc into column $c$) always transitions the environment into the exact predictable resulting state governed strictly by gravity; there is no stochastic transition probability.
- **Sequential**: Current decisions dynamically constrain and shape all downstream board configurations and tactical threats throughout the game.
- **Static**: The board state remains completely unchanged while an agent computes its move; time does not alter the board state independently.
- **Discrete**: The state space (grid positions), action space (columns $0 \dots 6$), and turn cycles are finite and distinct.
- **Known Rules**: All transition dynamics, legal move preconditions, and terminal conditions are completely defined and known *a priori*.
- **Adversarial (Multi-Agent)**: The environment involves two competing agents whose utilities are polar opposites ($+1$ vs. $-1$), requiring adversarial game-theoretic reasoning rather than classical single-agent planning.

---

## 3. Formal State-Space Formulation

| Component | Definition |
| :--- | :--- |
| **Initial State ($S_0$)** | An empty $6 \times 7$ board represented by a zero matrix $S_0 \in \{0\}^{6 \times 7}$, with Player 1 (Maximizer) designated to make the opening move. |
| **Action Set ($A(s)$)** | The set of legal columns where a disc can be placed: $A(s) = \{c \in \{0, \dots, 6\} \mid \text{row } 0 \text{ of column } c \text{ is empty}\}$. Branching factor $b \le 7$, monotonically decreasing as columns become full. |
| **Transition Model ($T(s, a)$)** | Dropping a disc into column $a$ occupies the lowest unoccupied row $r$ ($5 \ge r \ge 0$) of column $a$ with the current player's piece, subsequently toggling the active player turn: $\text{Turn}' = -\text{Turn}$. |
| **Goal Test / Terminal Test ($Terminal(s)$)** | True if four adjacent pieces of the same player align horizontally, vertically, or diagonally, OR if all 42 cells are filled with no four-in-a-row (a draw). |
| **Path / Utility Cost ($Utility(s, p)$)** | Connect Four is not a path-cost search; rather, terminal utility values are evaluated: <br>• $+1.0$: Win for player $p$<br>• $-1.0$: Loss for player $p$<br>• $0.0$: Draw |

---

## 4. Algorithmic Approaches & Evaluation Hypotheses

1. **Baseline Agents**:
   - **Random Agent**: Uniformly samples from legal actions $A(s)$. Serves as the sanity floor.
   - **Plain Minimax (No Pruning)**: Exhaustive depth-limited search evaluating the full game tree down to fixed depth $d$. Measures raw state-space explosion $O(b^d)$.
2. **Advanced Solvers**:
   - **Minimax with Alpha-Beta Pruning**: Employs branch pruning ($\alpha \ge \beta$), move ordering (center-column bias), and a weighted heuristic evaluation function. Expected theoretical complexity approaches $O(b^{d/2})$ under optimal move ordering.
   - **Monte Carlo Tree Search (MCTS)**: Uses the Upper Confidence Bound applied to Trees ($UCT = \bar{X}_j + 2 C_p \sqrt{\frac{2 \ln n}{n_j}}$), random rollout policies, and backpropagation to prioritize statistically promising branches without requiring hand-crafted heuristic formulas.

---

## 5. References (APA Format)

- Browne, C. B., Powley, E., Whitehouse, D., Lucas, S. M., Cowling, P. I., Rohlfshagen, P., Tavener, S., Perez, D., Samothrakis, S., & Colton, S. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games*, 4(1), 1–43.
- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. [Chapter 5: Adversarial Search and Games].
- Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai, M., Guez, A., Lanctot, M., Sifre, L., Dhar, S., Lillicrap, T., Graepel, T., & Hassabis, D. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*, 362(6419), 1140–1144.
