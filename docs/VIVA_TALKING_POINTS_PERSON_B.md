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
> 1. *First, architecting a high-performance, modular system with non-intrusive instrumentation that measures wall-clock decision latency via `time.perf_counter` and exact search space expansions via transparent node counting.*
> 2. *Second, implementing a competitive Monte Carlo Tree Search agent governed by the Upper Confidence Bound for Trees (UCT) with root-level tactical checks and dual rollout/time budgeting.*
> 3. *Third, creating an automated tournament benchmarking runner, generating high-DPI publication figures analyzing pruning efficiency and tournament dynamics, and developing an interactive Pygame graphical interface featuring dynamic winning-ray overlays, last-move tracking, and live playback speed controls.*
> 
> *Our empirical findings demonstrate the power of adversarial pruning: on an empty board at depth 5, unpruned Minimax requires 19,607 node expansions and 633.9 ms, while Alpha-Beta with center-out ordering expands just 563 nodes and completes in 28.3 ms—a 97.1% reduction in search space and an approximately 22x speedup. In mid-game positions, pruning achieves a 91.2% node reduction (1,624 nodes vs 18,544 nodes). Meanwhile, MCTS demonstrates strong domain-independent tactical strength under flexible time limits, scaling resistance as simulation budgets increase. In our 200-game round-robin tournament, Alpha-Beta (d=6, 57 pts), Alpha-Beta (d=4, 55.5 pts), and MCTS (N=500, 52.5 pts) form a tightly clustered top tier that cannot be separated statistically. I am eager to demonstrate our working GUI and benchmark harness."*

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
- **What to say:** *"To eliminate first-mover advantage, our `BenchmarkRunner` alternates starting player turns across games. It collects microsecond time and node expansion statistics, printing an executive summary table."*

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
> *"Vanilla Minimax must explore every leaf node across all legal branches, growing at $O(b^d)$ where $b \approx 7$. In our empirical benchmarks, Minimax was evaluated up to depth 5 where it expanded 19,607 nodes on an empty board and 18,544 nodes in a mid-game position.  
> Alpha-Beta maintains two running bounds: $\alpha$ (the highest score guaranteed to the Maximizer) and $\beta$ (the lowest score guaranteed to the Minimizer). Whenever a sub-branch yields a score worse than the opponent's already guaranteed option ($\alpha \ge \beta$), the remaining children of that node cannot influence the root decision and are pruned.  
> Crucially, because we sort candidate columns center-out (`[3, 2, 4, 1, 5, 0, 6]`), central moves—which participate in 51 distinct winning windows—are evaluated first. This establishes tight $\alpha$-$\beta$ bounds immediately, eliminating 97.1% of the search tree on an empty board (563 nodes vs 19,607 nodes) and 91.2% in the mid-game (1,624 nodes vs 18,544 nodes)."*

---

### Q2: "How does MCTS balance exploration and exploitation in Connect Four?"
> **Model Answer:**  
> *"Our MCTS implementation evaluates child nodes using the UCT (Upper Confidence Bound for Trees) formula:
> 
> $$\text{UCT}(v_i) = \frac{Q(v_i)}{N(v_i)} + c \sqrt{\frac{2 \ln N(v)}{N(v_i)}}$$
> 
> The first term ($\frac{Q(v_i)}{N(v_i)}$) is the exploitation term: the empirical win rate of child node $v_i$.  
> The second term is the exploration bonus, which scales with the logarithm of total parent visits divided by child visits.  
> In our codebase, the parameter $c$ is set to $1.414$ multiplying $\sqrt{\frac{2 \ln N}{n_i}}$. Honestly stated, the effective exploration multiplier is $c \sqrt{2} \approx 1.414 \times 1.4142 \approx 2.0$, which is approximately $1.4\times$ the standard theoretical UCB1 constant. This provides robust exploration across wide Connect Four branches while the root tactical guard prevents immediate tactical oversights."*

---

### Q3: "Why did you alternate player turns in the benchmark runner?"
> **Model Answer:**  
> *"Connect Four is a solved game with a proven first-mover advantage under optimal play (Allen, 1988; Allis, 1988), where Player 1 can force a win from column 3.  
> If an agent always played as Player 1, its measured win rate would be artificially inflated by turn order rather than algorithmic quality. By alternating starting turns across an even number of tournament games ($N = 20$), each agent plays as Player 1 in exactly 50% of matches and as Player 2 in 50%, neutralizing first-mover bias."*

---

### Q4: "What is the memory and spatial trade-off between Alpha-Beta and MCTS?"
> **Model Answer:**  
> *"Alpha-Beta operates via depth-first recursive traversal. Its spatial complexity is strictly bounded by the recursion stack height $O(d)$. Furthermore, because our `Board` class supports `make_move()` and in-place `undo_move()`, we do not duplicate board matrices at each node.  
> In contrast, MCTS constructs an explicit tree graph on the heap, instantiating `MCTSNode` objects with references, move tracking, and visit statistics that grow linearly with the simulation budget ($O(N)$). While Alpha-Beta uses negligible stack space, MCTS requires dynamic node allocation proportional to the number of rollouts."*

---

### Q5: "Why did you implement both a simulation budget and a time limit in MCTS?"
> **Model Answer:**  
> *"A fixed simulation budget (e.g. 500 rollouts) is ideal for reproducible scientific benchmarking where deterministic step counts allow fair comparison.  
> However, in a real-time interactive game or tournament with chess-clock rules, an algorithm must adhere to strict wall-clock deadlines (e.g. $200\text{ ms}$). MCTS is naturally an 'anytime algorithm'—at each iteration, it checks elapsed time via `time.perf_counter()`. If the deadline is reached, it immediately breaks the rollout loop and returns the child with the highest visit count $N(v_i)$."*

---

## 4. Honest Limitations & Scientific Integrity

When questioned by examiners on the boundaries of our study, we state our experimental limitations transparently:
1. **Single-Run Timings**: All reported execution times in `depth_scaling.csv` are single-run wall-clock measurements subject to background OS scheduling jitter and system noise; only node expansion counts are deterministic and exact.
2. **20 Games per Pair**: With 20 games per matchup in the round-robin tournament, statistical confidence intervals remain relatively wide; the top three agents (Alpha-Beta d=6, Alpha-Beta d=4, and MCTS N=500) cannot be separated with statistical significance.
3. **Deterministic Repeats**: Minimax and Alpha-Beta are fully deterministic algorithms. Consequently, pairings between two deterministic agents simply repeat the exact same game twice (once for each starting player across the 20 games), yielding only 2 unique game trajectories.
4. **No Memory or Per-Move-Time Measurement for MCTS**: Peak heap memory footprint and per-move deliberation time for MCTS were not instrumented during tournament play, so claims are restricted strictly to asymptotic $O(N)$ vs. $O(d)$ spatial complexity.
5. **Heuristic Benefit Not Tested in Play**: While the 69-window heuristic was evaluated on tactical benchmark positions and depth scaling, the isolated win-rate impact of heuristic weights versus pure center-ordering was not tested in head-to-head tournament play.
