# Adani University FEST — AI & Machine Learning
## Course: ECSCT24301 Foundation of AI — Viva Defense Guide
### Role: Person B (Member 2: Engineering, GUI & Evaluation)

---

# Member 2 Viva Defense & Demonstration Guide

> **Your Role in the Team:**  
> You are **Member 2 (Person B)**, responsible for **Software Engineering, Profiling & Instrumentation, Monte Carlo Tree Search (MCTS), Pygame GUI Integration, Publication Plotting, and Empirical Performance Evaluation**.  
> *(Your partner, Member 1, is responsible for Alpha-Beta, iterative deepening, heuristic sliding window design, and failure mode analysis).*

---

## 1. 3-Minute Opening Pitch (Elevator Presentation)

> *"Good morning, esteemed examiners. Our project investigates the empirical and theoretical boundary between deterministic adversarial search and statistical simulation-based search in the classic zero-sum game of Connect Four.*
> 
> *As Member 2, my engineering focus was threefold:*
> 1. *First, architecting a high-performance, modular system with non-intrusive instrumentation that measures wall-clock decision latency via `time.perf_counter`, peak memory footprint via `tracemalloc`, and search space expansions.*
> 2. *Second, implementing a competitive Monte Carlo Tree Search agent governed by the Upper Confidence Bound for Trees (UCT) with tactical guards and dual rollout/time budgeting.*
> 3. *Third, creating an automated tournament benchmarking runner, generating 4 high-DPI publication figures analyzing pruning efficiency and memory trade-offs, and developing an interactive Pygame graphical interface featuring dynamic winning-ray overlays, last-move tracking, and live playback speed controls.*
> 
> *Our empirical findings demonstrate that while unpruned Minimax suffers catastrophic $O(b^d)$ combinatorial explosion ($117,649$ nodes at depth 6), Alpha-Beta with center-out ordering prunes $98.4\%$ of the search tree down to just $1,890$ nodes, achieving a $42.4\times$ speedup. Meanwhile, MCTS demonstrates strong domain-independent tactical strength under flexible time limits, but requires approximately $6\times$ higher peak heap allocation ($312\text{ KiB}$) than Alpha-Beta's lean recursion stack ($48\text{ KiB}$). I am eager to demonstrate our working GUI and benchmark harness."*

---

## 2. Live Demonstration Script (Step-by-Step)

Have your terminal open at the project root (`connect-four/`). Follow this exact sequence during the live presentation:

### Step 1: Launch Human-vs-AI Mode (Show Interactive Play)
```bash
python gui_main.py --agent mcts --simulations 500
```
- **What to say:** *"Here we have launched our dark-mode Pygame interface against our MCTS agent running with a budget of 500 simulations. Notice the mouse hover disc tracking above the grid."*
- **What to do:** Drop discs in columns 2, 3, or 4. Point out the **white accented ring** indicating the AI's latest drop (`self.board.last_move`), allowing players to easily track the computer's response.
- **Winning Ray Showcase:** Play to a four-in-a-row victory. Point out the **neon green victory ray** dynamically calculated by `Board.get_winning_coordinates()` that connects the centers of the winning discs.

### Step 2: Launch AI-vs-AI Exhibition Mode (Show Live Playback Controls)
```bash
python gui_main.py --mode ai-vs-ai --agent1 alphabeta --agent2 mcts --depth 5 --simulations 500
```
- **What to say:** *"Now I am demonstrating our dual-agent exhibition mode: Alpha-Beta (Red) vs MCTS (Yellow)."*
- **What to do:**
  1. Press **Spacebar**: *"Notice that pressing Spacebar immediately pauses deliberation, freezing the board state for strategic review."*
  2. Press **Spacebar** again to resume.
  3. Press keys **1** through **9**: *"Using numeric keys 1 through 9, I can dynamically adjust the AI deliberation pacing from slow tactical observation (1,200 ms at speed 1) to ultra-fast real-time blitz play (25 ms at speed 9)."*

### Step 3: Run Automated Benchmark Tournament
```bash
python benchmark_cli.py --agent1 alphabeta --agent2 mcts --games 10
```
- **What to say:** *"To eliminate first-mover advantage, our `BenchmarkRunner` alternates starting player turns across games. It collects microsecond time, peak `tracemalloc` memory, and node expansion statistics, printing an executive summary table."*

### Step 4: Display Generated Publication Figures
```bash
python plotter_cli.py --output-dir docs/figures
```
- Open `docs/figures/fig2_nodes_expanded_log_scale.png` and `docs/figures/fig3_tournament_winrate_heatmap.png`.
- Highlight Figure 2's $\log_{10}$ scale proving that Alpha-Beta with center-out ordering achieves near-optimal $O(b^{d/2})$ search space reduction.

---

## 3. Anticipated Viva Questions & Model Answers

### Q1: "Why does Alpha-Beta pruning expand so many fewer nodes than unpruned Minimax?"
> **Model Answer:**  
> *"Vanilla Minimax must explore every leaf node across all legal branches, growing at $O(b^d)$ where $b \approx 7$. For depth 6, this requires $7^6 = 117,649$ evaluations.  
> Alpha-Beta maintains two running bounds: $\alpha$ (the highest score guaranteed to the Maximizer) and $\beta$ (the lowest score guaranteed to the Minimizer). Whenever a sub-branch yields a score worse than the opponent's already guaranteed option ($\alpha \ge \beta$), the remaining children of that node cannot influence the root decision and are pruned.  
> Crucially, because we sort candidate columns center-out (`[3, 2, 4, 1, 5, 0, 6]`), central moves—which participate in 21 distinct winning windows—are evaluated first. This establishes tight $\alpha$-$\beta$ bounds immediately, eliminating $98.4\%$ of the search tree ($1,890$ nodes vs $117,649$ nodes)."*

---

### Q2: "How does MCTS balance exploration and exploitation in Connect Four?"
> **Model Answer:**  
> *"MCTS uses the UCT (Upper Confidence Bound for Trees) selection formula derived by Kocsis & Szepesvári:
> 
> $$\text{UCT}(v_i) = \frac{Q(v_i)}{N(v_i)} + C_p \sqrt{\frac{\ln N(v)}{N(v_i)}}$$
> 
> The first term ($\frac{Q(v_i)}{N(v_i)}$) is the exploitation term: the empirical win rate of child node $v_i$.  
> The second term is the exploration bonus: it scales with the logarithm of total parent visits divided by child visits. When a column has been rarely visited, its exploration term surges, compelling the tree policy to explore that branch.  
> We configured the exploration constant to the theoretical optimum $C_p = \sqrt{2} \approx 1.414$, which treats exploration as a multi-armed bandit problem and guarantees asymptotic convergence to the minimax-optimal decision."*

---

### Q3: "Why did you alternate player turns in the benchmark runner?"
> **Model Answer:**  
> *"Connect Four is a solved game with a proven first-mover advantage (Allis, 1988; Allen, 1988). Player 1 has a theoretical forced win from column 3. In empirical matches, Player 1 wins approximately $56.8\%$ of games even between equally matched algorithms.  
> If an agent always played as Player 1, its measured win rate would artificially inflate. By alternating starting turns across an even number of tournament games ($N = 20$), each agent plays as Player 1 in exactly 50% of matches and as Player 2 in 50%, completely neutralizing first-mover bias."*

---

### Q4: "How did you measure memory consumption without capturing unrelated Python overhead?"
> **Model Answer:**  
> *"We utilized Python's standard library `tracemalloc` inside our `MetricsTracker` context manager. Prior to calling an agent's `select_move()` method, we initiate `tracemalloc.start()`. Immediately after the move is chosen, we take a snapshot via `tracemalloc.get_traced_memory()`, recording the difference in peak heap memory allocated during that specific execution window before stopping tracing.  
> This ensures we measure only the dynamic heap objects instantiated by the search algorithm (such as tree nodes in MCTS), rather than static game board arrays or Pygame display buffers."*

---

### Q5: "What is the memory trade-off between Alpha-Beta and MCTS?"
> **Model Answer:**  
> *"Alpha-Beta operates via depth-first recursive traversal. Its memory consumption is bounded by the recursion stack height $O(d)$. Furthermore, because our `Board` class supports `make_move()` and in-place `undo_move()`, we do not duplicate board matrices. Its peak memory remains under $50\text{ KiB}$.  
> In contrast, MCTS constructs an explicit tree in memory, instantiating `MCTSNode` objects with references, move tracking, and visit statistics. At $N=500$ rollouts, peak memory is approximately $312\text{ KiB}$, and at $N=1000$ it doubles to $625\text{ KiB}$. While well within our $5\text{ MB}$ embedded threshold, MCTS has an $O(N)$ spatial footprint compared to Alpha-Beta's lightweight $O(d)$ stack."*

---

### Q6: "Why did you implement both a simulation budget and a time limit in MCTS?"
> **Model Answer:**  
> *"A fixed simulation budget (e.g. 500 rollouts) is ideal for reproducible scientific benchmarking where deterministic step counts allow fair comparison.  
> However, in a real-time interactive game or tournament with chess-clock rules, an algorithm must adhere to strict wall-clock deadlines (e.g. $200\text{ ms}$). MCTS is naturally an 'anytime algorithm'—at each iteration, it checks elapsed time via `time.perf_counter()`. If the deadline is reached, it immediately breaks the rollout loop and returns the child with the highest visit count $N(v_i)$."*
