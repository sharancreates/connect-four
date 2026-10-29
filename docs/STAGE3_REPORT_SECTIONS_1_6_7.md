# Adani University — Faculty of Engineering Sciences & Technology (FEST)
## Department of Artificial Intelligence & Machine Learning
### Course: ECSCT24301 — Foundation of Artificial Intelligence (Semester V)
#### Track A: Applied AI System Development — Connect Four AI Milestone Report

---

# Member 2 (Person B) Technical Deliverables: Sections 1, 6, 7 & References

**Project Title:** Adversarial Search vs. Monte Carlo Tree Search in Connect Four  
**Role:** Person B (Member 2: Engineering, GUI & Evaluation)  
**Partner:** Person A (Member 1: Algorithms & Core Logic)  
**Date:** October 2026  

---

## Section 1: Problem Formulation & Environment Characterization

### 1.1 Problem Statement & Background
Connect Four is a two-player, zero-sum, complete-information, deterministic, sequential-move board game played on a vertically suspended $6 \times 7$ grid (6 rows and 7 columns). Players alternate dropping colored discs (Player 1 / Red represented as $+1$; Player 2 / Yellow represented as $-1$) into one of seven columns. Discs fall by simulated gravity, occupying the lowest available cell within the chosen column. The terminal objective is to be the first player to align four of one’s own discs consecutively along a horizontal, vertical, or diagonal vector. If all 42 grid cells are filled without a four-in-a-row alignment, the game concludes in a draw.

Mathematically, Connect Four was proven by James D. Allen (1988) and independently by Victor Allis (1988) to be a *first-player win* under theoretical optimal play: Player 1 can force a victory on move 41 by opening in the central column (column 3, 0-indexed). However, computing optimal play in real-time under competitive thinking limits presents significant computational hardness due to the size of the state space.

### 1.2 Mathematical State Space & Game Tree Complexity
The mathematical properties of the standard $6 \times 7$ Connect Four environment are defined by:
1. **Upper-Bound State Space**: With 42 cells and 3 possible states per cell ($\{0, +1, -1\}$), the naive combinatorial state space is $3^{42} \approx 1.09 \times 10^{20}$.
2. **Reachable Legal State Space**: Factoring in gravity constraints (pieces cannot float above empty cells) and alternating turn counts ($|n_{\text{red}} - n_{\text{yellow}}| \le 1$), the exact number of reachable valid board positions is:
   $$|S_{\text{valid}}| = 4,531,985,219,092 \approx 4.53 \times 10^{12}$$
3. **Game Tree Complexity**: With an average branching factor $b \approx 4$ across the match and an average terminal game length of $d \approx 36$ plies, the size of the complete game tree is approximately:
   $$|T_{\text{game}}| \approx 10^{21} \text{ paths}$$

Because an exhaustive search of $10^{21}$ states is computationally intractable under practical latency budgets ($< 500\text{ ms}$ per move), game agents must employ either **depth-limited heuristic search** (Minimax with Alpha-Beta pruning) or **asymmetric statistical sampling** (Monte Carlo Tree Search with UCT).

### 1.3 PEAS Environment Specification
In accordance with Russell & Norvig’s AI agent framework, the Connect Four problem environment is formalized through the **PEAS** model:

| PEAS Dimension | Specification for Connect Four AI System |
|---|---|
| **Performance Measure (P)** | • **Win Rate**: Percentage of tournament games won against opponent agents.<br>• **Decision Latency**: Mean computation time per ply (target $\le 300\text{ ms}$).<br>• **Search Efficiency**: Node expansion minimization and effective branching factor $b^*$. |
| **Environment (E)** | • **Grid Dimensions**: $6 \text{ rows} \times 7 \text{ columns}$ discrete board containing 42 discrete cells.<br>• **State Representation**: 2D signed integer matrix $\mathbf{S} \in \{-1, 0, +1\}^{6 \times 7}$ stored as a contiguous NumPy `int8` array.<br>• **Turn Dynamic**: Strict alternating sequential turns governed by gravity physics. |
| **Actuators (A)** | • **Action Space**: Column selection $a \in \mathcal{A}(s) \subseteq \{0, 1, 2, 3, 4, 5, 6\}$ where top cell $\mathbf{S}[0, a] == 0$.<br>• **State Transition**: Deterministic disc drop $T(s, a) \rightarrow s'$ to row $r = \max \{i \mid \mathbf{S}[i, a] == 0\}$. |
| **Sensors (S)** | • **Full Observability**: Direct programmatic access to entire $6 \times 7$ grid buffer.<br>• **Turn Sensor**: Current active player identity ($p \in \{+1, -1\}$).<br>• **Legal Move Sensor**: Array of available non-full column indices.<br>• **Terminal Sensor**: Directional four-in-a-row detector and board fullness detector. |

### 1.4 Environment Characteristics
- **Fully Observable vs. Partially Observable**: **Fully Observable**. The complete board configuration is accessible to both players without hidden information or fog-of-war.
- **Deterministic vs. Stochastic**: **Deterministic**. Dropping a disc into column $c$ transitions the environment to exactly one predictable successor state with probability $P(s' \mid s, a) = 1.0$.
- **Static vs. Dynamic**: **Static** during deliberation. The game environment does not mutate while an agent computes its move.
- **Discrete vs. Continuous**: **Discrete**. Turns, grid coordinates, legal actions, and terminal outcomes are finite and discrete.
- **Sequential vs. Episodic**: **Sequential**. Every move directly influences all subsequent tactical board configurations throughout the episode.
- **Adversarial / Multi-Agent**: **Competitive Zero-Sum Multi-Agent**. The reward structure is strictly complementary ($R_1 = -R_2$), where Player 1’s win implies Player 2’s loss.

---

## Section 6: Comparative Empirical Evaluation & Experimental Results

### 6.1 Experimental Methodology & Setup
To ensure reproducible and unbiased evaluation, all empirical experiments were executed under standardized test protocols:
- **Environment**: Python 3.10+ runtime, Windows 64-bit OS.
- **Tournament Orchestration**: Matches were executed using `BenchmarkRunner` (`connect4/benchmark/runner.py`) and recorded in `docs/results/tournament.csv`.
- **First-Mover Bias Neutralization**: In each head-to-head match series ($N = 20$ games per pair), starting turns were strictly alternated (Player 1 as Red in 10 games, Player 2 as Yellow in 10 games).
- **Measurement Instrumentation**:
  - Wall-clock decision time measured via high-precision `time.perf_counter()`. Single-run timings are subject to system noise; node counts are exact.
  - Node and playout expansions tracked transparently using the `NodeCounter` callback interface. Nodes count every recursive call.

### 6.2 Quantitative Benchmark Results

#### Table 6.1: Round-Robin Tournament Standings (200 Games, 20 per pair, Alternating First Mover)
*Scoring convention: 1 point for a win, 0.5 points for a draw, 0 points for a loss. Total points out of 80 possible across 4 opponent pairings.*

| Agent Algorithm | Parameter Configuration | Points (out of 80) | Score % | Head-to-Head Pairings (W-D-L vs Opponents) |
|---|---|---|---|---|
| **Alpha-Beta** | Depth $d = 6$ | **57.0** | $71.3\%$ | vs Random: 20-0-0; vs Minimax (d=3): 10-10-0; vs AlphaBeta (d=4): 0-20-0; vs MCTS (N=500): 12-0-8 |
| **Alpha-Beta** | Depth $d = 4$ | **55.5** | $69.4\%$ | vs Random: 20-0-0; vs Minimax (d=3): 10-10-0; vs AlphaBeta (d=6): 0-20-0; vs MCTS (N=500): 10-1-9 |
| **MCTS (UCT)** | $N = 500 \text{ rollouts}$ | **52.5** | $65.6\%$ | vs Random: 20-0-0; vs Minimax (d=3): 15-0-5; vs AlphaBeta (d=4): 9-1-10; vs AlphaBeta (d=6): 8-0-12 |
| **Minimax** | Depth $d = 3$ | **35.0** | $43.8\%$ | vs Random: 20-0-0; vs AlphaBeta (d=4): 0-10-10; vs AlphaBeta (d=6): 0-10-10; vs MCTS (N=500): 5-0-15 |
| **Random Baseline** | Uniform Stochastic | **0.0** | $0.0\%$ | vs Random: N/A; vs all 4 competitive agents: 0-0-20 each (0-0-80 overall) |

> **Tournament Analysis Notes:**  
> 1. **Statistical Separation**: The top three agents (Alpha-Beta $d=6$, Alpha-Beta $d=4$, and MCTS $N=500$) are separated by only 4.5 points out of 80 and cannot be separated statistically with 20 games per pair.  
> 2. **Deterministic Pairings**: Minimax and Alpha-Beta are fully deterministic. Consequently, pairings between two deterministic agents produce identical games for a given starting mover (effectively 2 distinct games per pair across 20 iterations).  
> 3. **Defensive Parity**: All 20 games between Alpha-Beta ($d=4$) and Alpha-Beta ($d=6$) resulted in draws (0-20-0), demonstrating that depth 4 with heuristic evaluation is sufficient to hold a draw against depth 6 under alternating starts.

#### Table 6.2: Search Space Expansion & Pruning Efficiency (`docs/results/depth_scaling.csv`)
*Nodes count every recursive call. Minimax was evaluated up to depth 5 only.*

| Position | Search Depth ($d$) | Minimax Nodes | Minimax Time (ms) | Alpha-Beta Nodes | Alpha-Beta Time (ms) | Node Reduction (%) |
|---|---|---|---|---|---|---|
| **Empty Board** | $d = 1$ | 7 | 0.70 | 7 | 0.77 | 0.0% |
| **Empty Board** | $d = 2$ | 56 | 1.42 | 20 | 1.43 | 64.3% |
| **Empty Board** | $d = 3$ | 399 | 21.06 | 75 | 2.38 | 81.2% |
| **Empty Board** | $d = 4$ | 2,800 | 114.05 | 172 | 9.15 | 93.9% |
| **Empty Board** | $d = 5$ | 19,607 | 633.85 | 563 | 28.25 | **97.1%** (~22× faster) |
| **Empty Board** | $d = 6$ | — | — | 1,248 | 49.42 | — |
| **Empty Board** | $d = 7$ | — | — | 4,904 | 433.89 | — |
| **Empty Board** | $d = 8$ | — | — | 8,646 | 484.74 | — |
| **Empty Board** | $d = 9$ | — | — | 33,169 | 1551.63 | — |
| **Mid-Game** | $d = 1$ | 7 | 0.28 | 7 | 0.85 | 0.0% |
| **Mid-Game** | $d = 2$ | 56 | 5.48 | 20 | 1.44 | 64.3% |
| **Mid-Game** | $d = 3$ | 399 | 19.46 | 129 | 4.81 | 67.7% |
| **Mid-Game** | $d = 4$ | 2,715 | 104.37 | 263 | 11.41 | 90.3% |
| **Mid-Game** | $d = 5$ | 18,544 | 619.11 | 1,624 | 63.17 | **91.2%** (~10× faster) |
| **Mid-Game** | $d = 6$ | — | — | 2,967 | 114.13 | — |
| **Mid-Game** | $d = 7$ | — | — | 25,507 | 854.81 | — |
| **Mid-Game** | $d = 8$ | — | — | 45,346 | 1211.16 | — |
| **Mid-Game** | $d = 9$ | — | — | 385,217 | 9477.09 | — |

---

### 6.3 In-Depth Analysis of Publication Figures

#### Figure 1: Mean Move Latency vs. Search Depth
![Figure 1: Mean Move Latency vs Search Depth](figures/fig1_execution_time_vs_depth.png)

As demonstrated in **Figure 1**, Vanilla Minimax exhibits rapid exponential latency growth:
- On the empty board at depth $d = 5$, Minimax requires $633.85\text{ ms}$, whereas Alpha-Beta completes in $28.25\text{ ms}$ (approximately $22\times$ faster).
- In the mid-game position at depth $d = 5$, Minimax consumes $619.11\text{ ms}$ versus $63.17\text{ ms}$ for Alpha-Beta (approximately $10\times$ faster).
- For Alpha-Beta, search remains responsive through depth 6 ($49.42\text{ ms}$ empty, $114.13\text{ ms}$ mid-game). However, moving to depth 9 requires $1,551.6\text{ ms}$ on the empty board and escalates to $9,477.1\text{ ms}$ in the mid-game ($30,938.1\text{ ms}$ with the 69-window heuristic), illustrating the exponential scaling cliff where fixed-depth search exceeds interactive limits.

#### Figure 2: Search Tree Node Expansions (Logarithmic Scale)
![Figure 2: Search Space Expansion vs Depth](figures/fig2_nodes_expanded_log_scale.png)

**Figure 2** highlights the theoretical and empirical power of adversarial pruning plotted on a $\log_{10}$ semi-log scale across both positions:
- At depth $d = 5$ on the empty board, Vanilla Minimax expands $19,607$ nodes while Alpha-Beta expands only $563$ nodes—an empirical **$97.1\%$ reduction in search tree size**.
- In the mid-game position at depth $d = 5$, Minimax expands $18,544$ nodes compared to $1,624$ nodes for Alpha-Beta (**$91.2\%$ reduction**).
- Center-out move ordering (`[3, 2, 4, 1, 5, 0, 6]`) ensures central columns—which participate in 51 distinct 4-in-a-row winning lines—are evaluated first, establishing tight $\alpha$-$\beta$ cutoffs early in tree traversal.
- The effective branching factor for Alpha-Beta stabilizes between $b^* \approx 3.4$ (empty board) and $b^* \approx 4.3$ (mid-game), lying strictly between optimal $O(b^{d/2})$ ($\sqrt{7} \approx 2.65$) and worst-case $O(b^d)$ ($7.0$).

#### Figure 3: Head-to-Head Tournament Win-Rate Heatmap
![Figure 3: Head-to-Head Tournament Win-Rate Matrix](figures/fig3_tournament_winrate_heatmap.png)

**Figure 3** illustrates the complete round-robin tournament results ($N = 20$ games per pairing, alternating first mover) displaying `W-D-L` records and row-agent score percentages:
- **Top Tier Clustering**: Alpha-Beta ($d=6$, 57.0 pts), Alpha-Beta ($d=4$, 55.5 pts), and MCTS ($N=500$, 52.5 pts) form a tightly clustered top tier that cannot be separated with statistical significance.
- **Head-to-Head Balance**: Against MCTS ($N=500$), Alpha-Beta ($d=6$) won 12 games and lost 8 (60.0% score), while Alpha-Beta ($d=4$) won 10, drew 1, and lost 9 (52.5% score).
- **All-Draw Pairings**: Alpha-Beta ($d=4$) vs. Alpha-Beta ($d=6$) drew all 20 games (0-20-0, 50.0% score), demonstrating that both depths find identical drawing lines under deterministic play.
- **Minimax Baseline**: Minimax ($d=3$) defeated Random 20-0-0, secured 10 draws each against Alpha-Beta ($d=4$) and Alpha-Beta ($d=6$), and won 5 games against MCTS ($N=500$), finishing with 35.0 points.

#### Figure 6: MCTS Scaling vs. Alpha-Beta (d=4, Heuristic)
![Figure 6: MCTS Scaling vs Alpha-Beta](figures/fig6_mcts_strength.png)

**Figure 6** plots the performance of MCTS across simulation budgets ($N \in \{50, 200, 500, 1000\}$) against Alpha-Beta ($d=4$, heuristic) across 10 games per budget (`docs/results/mcts_vs_alphabeta.csv`):
- **Win Rate Trajectory**: MCTS won 0 of 10 games at $N=50$ and $N=200$ simulations, rising to 3 of 10 games at both $N=500$ and $N=1000$. Increasing the budget beyond 500 simulations did not yield additional wins in this 10-game sample.
- **Game Length Resistance**: Games lost by MCTS were significantly shorter at 50 simulations ($17.9$ plies on average) than at 200 or more simulations ($\approx 30.9$ plies). Beyond 200 simulations, the average game length remains flat.
- **Tactical Check**: In isolated single-threat blocking tests (`docs/results/block_test.csv`), MCTS successfully blocked immediate 1-ply winning threats in 20 of 20 trials across all budgets ($N \in \{5, 20, 100, 500\}$) due to its root-level tactical check.

---

### 6.4 Key Trade-off Analysis: Adversarial Search vs. Monte Carlo Tree Search

| Evaluation Dimension | Alpha-Beta Pruning (Minimax) | Monte Carlo Tree Search (UCT) |
|---|---|---|
| **Tactical Horizon** | **Guaranteed Defense up to depth $d$**. Evaluates all forced replies; immune to blunders within search horizon. | **Statistical Horizon**. Blocks 1-ply threats reliably via root tactical check, but may miss deeper multi-ply combinations without deep rollouts. |
| **Heuristic Dependency** | Highly dependent on handcrafted heuristic evaluation (e.g. 69-window weighting). Poor heuristics compromise move choice. | **Domain-Independent**. Can evaluate positions purely through random playout statistics without hand-tuned feature weights. |
| **Time Flexibility** | Rigid depth limits require Iterative Deepening to support hard time budgets. | **Naturally Anytime**. Can terminate search at any millisecond deadline and return the most-visited child node. |
| **Spatial Complexity** | **$O(d)$ Call Stack**. Minimal heap footprint; board mutated and reverted in-place via `make_move()` and `undo_move()`. | **$O(N)$ Tree Graph**. Dynamic node graph instantiated on the heap that grows linearly with simulation iterations. |

---

## Section 7: System Architecture, Modular Design & Engineering Rigor

### 7.1 Architecture & Separation of Concerns
The Connect Four system was engineered following strict Object-Oriented and SOLID architectural principles. The package hierarchy establishes clear boundaries between core game physics, search intelligence, benchmarking instrumentation, and presentation layers:

```
connect-four/
├── connect4/
│   ├── core/                  # Game Engine Layer
│   │   ├── board.py           # 6x7 NumPy grid, gravity drop, undo, win detection
│   │   └── __init__.py        # Exported constants (ROWS, COLS, PLAYER_1, PLAYER_2)
│   ├── agents/                # Search Intelligence Layer
│   │   ├── base.py            # Abstract Base Class (Agent contract)
│   │   ├── random_agent.py    # Uniform random baseline
│   │   ├── minimax_agent.py   # Vanilla depth-limited Minimax
│   │   ├── alphabeta_agent.py # Alpha-Beta pruning with center-out ordering
│   │   ├── iterative_agent.py # Iterative Deepening with deadline guard
│   │   ├── mcts_agent.py      # Monte Carlo Tree Search with UCT & tactical guards
│   │   └── heuristic.py       # Precomputed 69-window sliding evaluator
│   ├── benchmark/             # Evaluation & Instrumentation Layer
│   │   ├── instrumentation.py # MetricsTracker (time.perf_counter & NodeCounter)
│   │   ├── runner.py          # BenchmarkRunner multi-game tournament orchestrator
│   │   └── plotter.py         # Headless Matplotlib publication plotting suite
│   ├── gui/                   # Interactive Presentation Layer
│   │   ├── pygame_app.py      # 700x700px graphical Pygame interface with HUD
│   │   └── __init__.py        # Headless compatibility wrappers
│   └── cli/                   # Console Interface Layer
│       └── game_loop.py       # Rich CLI game runner
├── docs/                      # Technical Documentation & Deliverables
│   ├── figures/               # High-DPI publication figures (Fig 1, 2, 3, 6)
│   ├── results/               # Empirical benchmark CSV datasets
│   ├── PEAS_AND_PROBLEM_STATEMENT.md
│   ├── ALGORITHMS.md
│   └── STAGE3_REPORT_SECTIONS_1_6_7.md
├── tests/                     # Automated Pytest Suite (54 unit & integration tests)
├── main.py                    # Unified CLI entrypoint
├── gui_main.py                # Graphical GUI launcher (Human vs AI & AI vs AI)
├── benchmark_cli.py           # Automated tournament CLI runner
├── experiments_cli.py         # Scaling & failure-mode experimentation harness
└── plotter_cli.py             # Publication figures generator CLI
```

### 7.2 Profiling Rigor & Non-Intrusive Instrumentation
Measuring performance without distorting algorithm execution was a primary engineering objective:
1. **Wall-Clock Latency**: Utilizes `time.perf_counter()`, offering microsecond precision that measures real elapsed processor and system time.
2. **Node Expansion Transparency**: Search algorithms interact with an optional `NodeCounter` callback or internal expansion accumulator. Node increments execute in $O(1)$ constant time, introducing negligible overhead ($< 0.5\%$).

### 7.3 Graphical Interface (Pygame) Engineering
The graphical application (`Connect4Pygame`) was designed to provide an engaging, faculty-ready live demonstration interface:
- **Visual Design**: $700 \times 700\text{ px}$ dark-mode viewport ($600\text{ px}$ board grid $+ 100\text{ px}$ HUD banner) rendered at 60 FPS.
- **Winning Ray Overlay**: Detects the winning quartet via `Board.get_winning_coordinates()` and renders a dynamic neon emerald victory line connecting disc centers (`pygame.draw.line`) along with accented rings around each winning cell.
- **Last-Move Ring Indicator**: Renders an accented circular ring and center dot around the most recently dropped disc (`self.board.last_move`), allowing observers to effortlessly follow fast-paced AI play.
- **Interactive Playback Controls**:
  - `Spacebar`: Instantly pauses and resumes automated agent matches.
  - `Keys 1–9`: Dynamically adjusts AI decision delays from $1,200\text{ ms}$ (Level 1) down to $25\text{ ms}$ (Level 9).
  - Mode Flexibility: Supports both Human-vs-AI play (with mouse hover disc preview) and autonomous AI-vs-AI exhibition matches (`--mode ai-vs-ai`).
- **Headless Testing Architecture**: Configured with `SDL_VIDEODRIVER="dummy"` when `headless=True`, enabling automated integration testing in headless CI environments without requiring active video displays.

---

## References (APA 7th Edition)

1. Allen, J. D. (1988). A complete solution of Connect Four. *Heuristic Programming in Artificial Intelligence 1: The First Computer Olympiad*, 134–144.
2. Allis, L. V. (1988). *A knowledge-based approach of Connect-Four: The game is solved: White wins*. Master's thesis, Department of Mathematics and Computer Science, Vrije Universiteit Amsterdam.
3. Browne, C. B., Powley, E., Whitehouse, D., Lucas, S. M., Cowling, P. I., Rohlfshagen, P., Tavener, S., Perez, D., Samothrakis, S., & Colton, S. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games*, 4(1), 1–43. https://doi.org/10.1109/TCIAIG.2012.2186810
4. Knuth, D. E., & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence*, 6(4), 293–326. https://doi.org/10.1016/0004-3702(75)90019-3
5. Kocsis, L., & Szepesvári, C. (2006). Bandit based Monte-Carlo planning. *European Conference on Machine Learning*, 282–293. Springer, Berlin, Heidelberg. https://doi.org/10.1007/11871842_29
6. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
