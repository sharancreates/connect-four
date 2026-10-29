# Adani University — Faculty of Engineering Sciences & Technology (FEST)
## Department of Artificial Intelligence & Machine Learning
### Course: ECSCT24301 — Foundation of Artificial Intelligence (Semester V)
#### Track A: Applied AI System Development — Connect Four AI Milestone Report

---

# Member 1 (Person A) Technical Deliverables: Sections 2, 3, 4, 5 & 8

**Project Title:** Adversarial Search vs. Monte Carlo Tree Search in Connect Four  
**Role:** Person A (Member 1: Algorithms & Core Logic)  
**Partner:** Person B (Member 2: Engineering, GUI & Evaluation)  
**Date:** October 2026  

> **Data note.** All measurements in Sections 4, 5 and 8 come from `experiments_cli.py` (results saved in `docs/results/`). They use two fixed positions: the **empty board** and a fixed **8-ply mid-game position** (moves `3, 3, 2, 4, 4, 2, 5, 3`). They are single-position measurements, so they differ from the tournament averages reported in Section 6. Node counts include every call of the max/min step (leaf and terminal nodes too), but not the root.

---

## Section 2: Formal Search-Problem Formulation & Algorithm Specification

### 2.1 Search Problem Definition
The environment characterization and the size of the state space are given in Section 1. Here the game is written as an adversarial search problem

$$\mathcal{P} = \langle S,\; s_0,\; \text{Player},\; \text{Actions},\; \text{Result},\; \text{Terminal},\; U \rangle$$

| Component | Definition | Implementation (`connect4/core/board.py`) |
|---|---|---|
| State $s \in S$ | $6 \times 7$ matrix over $\{-1, 0, +1\}$ plus the player to move | `Board.grid`, `Board.current_player` |
| Initial state $s_0$ | Empty board, Player 1 ($+1$, MAX) to move | `Board()` |
| $\text{Player}(s)$ | Alternates: $+1 \rightarrow -1 \rightarrow +1 \dots$ | toggled in `make_move` / `undo_move` |
| $\text{Actions}(s)$ | Columns whose top cell is empty, $\lvert\text{Actions}(s)\rvert \le 7$ | `get_legal_moves()` |
| $\text{Result}(s, a)$ | Disc falls to the lowest empty row of column $a$; turn passes | `make_move(a)` |
| $\text{Terminal}(s)$ | Four in a row for either player, or all 42 cells filled | `is_terminal()` |
| Utility $U(s, p)$ | $+1$ win, $-1$ loss, $0$ draw (scaled in the code, see 2.2) | `get_winner()` |

Searching from the point of view of one fixed agent $p$ (the player the agent controls), MAX nodes are the nodes where $p$ moves and MIN nodes are the opponent's turns.

### 2.2 Depth-Limited Minimax
The depth-limited Minimax value of a state $s$ with $d$ plies of lookahead left is

$$
V_d(s) =
\begin{cases}
U'(s, d) & \text{if } \text{Terminal}(s) \\
h(s, p) & \text{if } d = 0 \\
\max_{a \in \text{Actions}(s)} V_{d-1}(\text{Result}(s,a)) & \text{if } \text{Player}(s) = p \\
\min_{a \in \text{Actions}(s)} V_{d-1}(\text{Result}(s,a)) & \text{otherwise}
\end{cases}
$$

where $h$ is the heuristic of Section 3 and the scaled terminal utility is

$$
U'(s, d) = \begin{cases} +100000 + d & \text{agent wins} \\ -100000 - d & \text{agent loses} \\ 0 & \text{draw} \end{cases}
$$

The $\pm d$ term (remaining depth) makes the agent **prefer a quicker win** (more depth left when the win is found) and **delay a loss** as long as possible. The terminal values are far larger than any heuristic value, so a forced win or loss always dominates a positional estimate.

### 2.3 Alpha-Beta Pruning
Alpha-Beta computes the same value while carrying a window $(\alpha, \beta)$: $\alpha$ is the best value MAX can already guarantee on the current path and $\beta$ the best value MIN can already guarantee.

```
function MAX-VALUE(s, d, alpha, beta):
    if terminal(s):  return U'(s, d)
    if d == 0:       return h(s)
    v = -infinity
    for a in ORDER(actions(s)):               # center columns first
        v = max(v, MIN-VALUE(result(s, a), d-1, alpha, beta))
        if v >= beta:  return v               # MIN above will never allow this branch
        alpha = max(alpha, v)
    return v

function MIN-VALUE(s, d, alpha, beta):
    if terminal(s):  return U'(s, d)
    if d == 0:       return h(s)
    v = +infinity
    for a in ORDER(actions(s)):
        v = min(v, MAX-VALUE(result(s, a), d-1, alpha, beta))
        if v <= alpha:  return v              # MAX above already has something better
        beta = min(beta, v)
    return v
```

**Correctness (Knuth & Moore, 1975).** Calling `MAX-VALUE(s_0, d, -inf, +inf)` returns exactly $V_d(s_0)$. Sketch: a cutoff only happens when the current node's value can no longer change the value of any ancestor (if $v \ge \beta$ at a MAX node, its MIN parent already has a better option $\le \beta$, so the exact value of this node is irrelevant). Induction on depth shows every skipped subtree is irrelevant for the root value. This is why the project's test `test_alphabeta_vs_minimax_same_moves` expects both agents to choose the same move.

### 2.4 Implementation Design
- **Make/undo instead of copying.** Search mutates one board with `make_move` and `undo_move`, so memory is $O(d)$ and no board is allocated per node.
- **Move ordering.** Moves are sorted by distance from the center column, giving the order `[3, 2, 4, 1, 5, 0, 6]`. Good moves first means earlier cutoffs (Section 4).
- **Node counting.** One increment per call of the MAX/MIN step. Plain Minimax and Alpha-Beta count the same way, so their counts are directly comparable.
- **Shared interface.** Every agent implements `select_move(board) -> column` and exposes `nodes_expanded`, so the benchmark harness treats them identically.

| Class | File | Role |
|---|---|---|
| `MinimaxAgent` | `minimax_agent.py` | Baseline, no pruning, center-only evaluation |
| `AlphaBetaAgent` | `alphabeta_agent.py` | Pruning; `use_heuristic=True` switches on the Section 3 evaluation |
| `IterativeAlphaBetaAgent` | `iterative_agent.py` | Alpha-Beta + iterative deepening + time budget (always uses the heuristic) |

### 2.5 Iterative Deepening with a Time Budget
```
function ITERATIVE-SELECT(board, time_limit, max_depth):
    deadline = now() + time_limit;  best = first legal move
    for d = 1 .. max_depth:
        try:    move, score = ROOT-SEARCH(copy(board), d)     # checks the clock at every node
        except TimeUp:  break                                 # unfinished depth is discarded
        best = move;  depth_reached = d
        if score >= WIN:  break                               # forced win found
        move best to the front of the move list               # better ordering at depth d+1
    return best
```
Searching on a **copy** guarantees that a timeout in the middle of a search cannot leave the real board changed (checked by `test_board_is_unchanged_after_search`).

---

## Section 3: Heuristic Evaluation Function Design

### 3.1 Motivation
Depth-limited search must estimate the value of non-terminal states at the horizon. Connect Four is won by completing one of the **69 possible four-cell lines** (24 horizontal, 21 vertical, 24 diagonal), so the heuristic scores how close each line is to being completed by either player. This directly encodes the goal test and needs no learned parameters.

### 3.2 Definition
Let $W$ be the set of the 69 windows. For a window $w$ let $m$, $o$, $e$ be the number of cells of the agent, of the opponent and empty ($m + o + e = 4$). The evaluation from the point of view of player $p$ is

$$
h(s, p) = w_c \,\bigl(n^{p}_{\text{center}} - n^{-p}_{\text{center}}\bigr) + \sum_{w \in W} f(w)
$$

$$
f(w) =
\begin{cases}
+5 & m = 3,\; e = 1 \\
+2 & m = 2,\; e = 2 \\
-6 & o = 3,\; e = 1 \\
-2 & o = 2,\; e = 2 \\
0 & \text{otherwise (including every window with both colors)}
\end{cases}
\qquad w_c = 3
$$

| Feature | Weight | Reason |
|---|---|---|
| Disc in the center column | $+3$ / $-3$ | Center discs belong to the largest number of potential lines |
| Own open three | $+5$ | One move from winning |
| Own open two | $+2$ | Building potential |
| Opponent open three | $-6$ | Immediate threat that must be handled |
| Opponent open two | $-2$ | Developing threat |
| Mixed window | $0$ | Can never become four in a row |

### 3.3 Design Rationale
- **Defensive asymmetry.** The opponent's three ($-6$) is weighted slightly more than the agent's own three ($+5$). At the horizon the agent cannot see what happens next, so it is safer to overestimate the opponent's threats than its own.
- **Terminal dominance.** All heuristic values are tiny compared to $\pm 100000$, so search never trades a forced result for a positional gain.
- **Cheap evaluation.** The 69 windows are precomputed once (`WINDOWS` in `heuristic.py`); one evaluation reads at most $69 \times 4 = 276$ cells. The weights are named constants at the top of the file, so they can be tuned without touching the search code.

### 3.4 Validation
`tests/test_heuristic.py` checks the function on hand-built boards:

| Test | Property verified |
|---|---|
| `test_window_count` | Exactly 69 windows |
| `test_empty_board_scores_zero` | No bias on an empty board |
| `test_center_disc_better_than_edge` | Center control is rewarded |
| `test_perspective_flips_sign` | Swapping the player flips the sign (on a board without threats) |
| `test_open_three_beats_open_two` | Larger threats score higher |
| `test_opponent_three_is_negative` | Opponent threats lower the score |
| `test_blocked_three_worth_less_than_open_three` | A three blocked by an opponent disc is worth less |
| `test_vertical_three_counts`, `test_diagonal_three_counts` | All three directions are detected |

**Cost.** The heuristic is evaluated at every leaf (up to 276 cell reads), so it is expected to cost more per node. Single-run timings are noisy (for example empty board depth 9: 2,455.8 ms with the heuristic vs 1,551.6 ms without, but depth 8: 379.9 ms vs 484.7 ms), and node counts, which are deterministic, are the reliable comparison (Table 5.1).

**Effect on play.** In the Week 2 match of Alpha-Beta (depth 4) with the heuristic against Alpha-Beta (depth 4) with center-only evaluation, the heuristic agent won (34 turns). This is one game and only a demonstration; a statistically meaningful comparison needs many games with alternating sides.

### 3.5 Known Limitations
- Weights were chosen by hand, not tuned or learned.
- Overlapping windows count the same disc several times, so a strong disc is counted more than once.
- The function knows nothing about **threat parity** (which player is forced to play under a threat in a given row), a known important concept in Connect Four.
- Windows that need a disc to be placed on a not-yet-reachable cell are treated like reachable ones.

---

## Section 4: Minimax vs. Alpha-Beta Pruning and Iterative Deepening

### 4.1 Identical Decisions, Fewer Nodes
Alpha-Beta is an optimization, not an approximation. The automated tests confirm that Minimax and Alpha-Beta choose the same move on three different boards at depth 3 (`test_alphabeta_vs_minimax_same_moves`), that Alpha-Beta expands fewer nodes at depth 4 (`test_alphabeta_expands_fewer_nodes_than_minimax`), that it plays an immediate win, and that it blocks an immediate loss.

### 4.2 Measured Pruning Efficiency
Both agents use the same evaluation, so the node counts are comparable.

**Table 4.1 — Nodes per move, Minimax vs. Alpha-Beta (same evaluation)**

| Position | Depth | Minimax nodes | Alpha-Beta nodes | Nodes saved |
|---|---|---|---|---|
| Empty | 2 | 56 | 20 | 64.3% |
| Empty | 3 | 399 | 75 | 81.2% |
| Empty | 4 | 2,800 | 172 | 93.9% |
| Empty | 5 | 19,607 | 563 | 97.1% |
| Mid-game | 2 | 56 | 20 | 64.3% |
| Mid-game | 3 | 399 | 129 | 67.7% |
| Mid-game | 4 | 2,715 | 263 | 90.3% |
| Mid-game | 5 | 18,544 | 1,624 | 91.2% |

Observations:
1. At depth 1 nothing can be pruned (7 nodes each); pruning starts at depth 2.
2. **The saving grows with depth.** On the empty board, pruning removes 81.2% of the nodes at depth 3 and 97.1% at depth 5.
3. **Pruning depends on the position.** In the mid-game position the saving is lower (91.2% vs. 97.1% at depth 5), because positions with real threats leave fewer cutoffs available than the quiet opening.
4. Over a full 21-move-per-side game at depth 4 (Week 2 benchmark), Alpha-Beta used 1,726 nodes against 17,134 for Minimax (9.9x fewer) and 245 ms against 1,908 ms (7.8x faster).

### 4.3 Role of Move Ordering
Alpha-Beta cuts the most when the best move is examined first. The agent uses a fixed, cheap ordering (center columns first), which is correct often because the center is usually strong in Connect Four. A more advanced ordering (best move of the previous iteration, killer moves, or sorting by heuristic value) would cut more; iterative deepening already provides the "best move first" ordering at the root (Section 2.5).

### 4.4 Iterative Deepening Under a Time Budget
Fixed-depth search cannot guarantee a response time. Iterative deepening repeats the search with growing depth and plays the result of the last finished depth.

**Table 4.2 — Depth reached by `IterativeAlphaBetaAgent` (heuristic on)**

| Time limit | Empty board: depth / nodes | Mid-game: depth / nodes |
|---|---|---|
| 0.05 s | 5 / 903 | 3 / 460 |
| 0.20 s | 6 / 4,514 | 5 / 3,036 |
| 0.50 s | 7 / 12,137 | 5 / 4,101 |
| 1.00 s | 8 / 24,999 | 6 / 16,558 |

Observations:
1. The agent respects every budget (elapsed time was 0.050, 0.200, 0.500 and 1.000 s in the runs).
2. More time gives more depth, but **the depth reached depends strongly on the position**: with 1 s it reaches depth 8 on the empty board but only depth 6 in the mid-game position.
3. **The repeated shallow searches are cheap.** The cost of the last iteration dominates because the node count grows geometrically with depth (Section 5), so re-searching depths $1 \dots d-1$ adds only a fraction to the cost of depth $d$.

---

## Section 5: Theoretical vs. Empirical Complexity

### 5.1 Theoretical Complexity
Let $b$ be the branching factor ($\le 7$) and $d$ the search depth.

| Algorithm | Time | Space | Notes |
|---|---|---|---|
| Minimax | $O(b^d)$ | $O(d)$ with make/undo | Every node to depth $d$ is visited |
| Alpha-Beta, best ordering | $O(b^{d/2})$ | $O(d)$ | Effective branching factor $\sqrt{b} \approx 2.65$ for $b = 7$ (Knuth & Moore, 1975) |
| Alpha-Beta, average ordering | about $O(b^{3d/4})$ | $O(d)$ | Random ordering (Pearl, 1982) |
| Alpha-Beta, worst ordering | $O(b^d)$ | $O(d)$ | No cutoffs |
| Iterative deepening | same order as the last depth | $O(d)$ | Overhead factor about $b/(b-1)$ for a full tree |
| MCTS ($N$ simulations) | $O(N \cdot L)$ | $O(N)$ | $L \le 42$ is the playout length; tree grows by one node per simulation |

### 5.2 Empirical Growth
**Table 5.1 — Time and nodes per move versus depth (`experiments_cli.py --experiment depth`)**

| Position | Agent | Depth | Nodes | Time (ms) |
|---|---|---|---|---|
| Empty | Minimax | 3 / 4 / 5 | 399 / 2,800 / 19,607 | 21.1 / 114.1 / 633.9 |
| Empty | Alpha-Beta | 3 / 4 / 5 / 6 / 7 / 8 / 9 | 75 / 172 / 563 / 1,248 / 4,904 / 8,646 / 33,169 | 2.4 / 9.2 / 28.3 / 49.4 / 433.9 / 484.7 / 1551.6 |
| Empty | Alpha-Beta + heuristic | 3 / 4 / 5 / 6 / 7 / 8 / 9 | 75 / 174 / 626 / 1,282 / 5,085 / 9,795 / 35,597 | 7.0 / 12.6 / 57.5 / 100.5 / 321.3 / 379.9 / 2455.8 |
| Mid-game | Minimax | 3 / 4 / 5 | 399 / 2,715 / 18,544 | 19.5 / 104.4 / 619.1 |
| Mid-game | Alpha-Beta | 3 / 4 / 7 / 8 / 9 | 129 / 263 / 25,507 / 45,346 / 385,217 | 4.8 / 11.4 / 854.8 / 1211.2 / 9477.1 |
| Mid-game | Alpha-Beta + heuristic | 3 / 4 / 5 / 6 / 7 / 8 / 9 | 151 / 396 / 1,969 / 4,747 / 31,833 / 73,986 / 460,830 | 11.2 / 22.0 / 104.5 / 195.0 / 1455.9 / 2689.3 / 30938.1 |

*(Figure 1 and Figure 2, `docs/figures/fig1_execution_time_vs_depth.png` and `docs/figures/fig2_nodes_expanded_log_scale.png`, plot move latency and search tree node expansions against depth for empty and mid-game positions.)*

### 5.3 Effective Branching Factor
The effective branching factor is estimated as $b^* \approx N^{1/d}$ where $N$ is the total node count.

| Agent | Position | Depth | $b^*$ |
|---|---|---|---|
| Minimax | Empty | 5 | 7.22 |
| Minimax | Mid-game | 4 | 7.22 |
| Alpha-Beta | Empty | 7 | 3.37 |
| Alpha-Beta | Mid-game | 7 | 4.26 |
| Alpha-Beta | Mid-game | 9 | 4.19 |
| Alpha-Beta + heuristic | Empty | 7 | 3.38 |
| Alpha-Beta + heuristic | Mid-game | 7 | 4.40 |
| Alpha-Beta + heuristic | Mid-game | 9 | 4.27 |

Comparison with theory:
1. **Minimax matches $O(b^d)$.** $b^*$ is slightly above 7 because the node count includes all levels (the geometric sum $1 + 7 + 7^2 + \dots$ is larger than $7^d$); every extra ply multiplies the cost by about 7.
2. **Alpha-Beta lies between the best and worst case.** Its $b^*$ of 3.4 to 4.4 is far below 7 but above the best-case $\sqrt{7} \approx 2.65$. The reason is that the fixed center-first ordering is good but not perfect.
3. **Quiet positions prune better than tactical ones.** $b^*$ is 3.4 on the empty board and 4.3 to 4.4 in the mid-game position.
4. **Growth is not smooth.** On the empty board the cost ratio between consecutive depths is 3.3 (4 to 5 is $172 \to 563$), 2.2 ($563 \to 1{,}248$) and 3.9 ($1{,}248 \to 4{,}904$). The alternating ratio is consistent with an odd/even depth effect in Alpha-Beta pruning; this is an observation from one position, not a tested explanation. Similarly, the cost ratio between consecutive depths in the mid-game position is uneven (for example 1.8x from depth 7 to 8 and 8.5x from depth 8 to 9 for plain Alpha-Beta).

### 5.4 Throughput and Space
- **Throughput.** Alpha-Beta processes about 26,000 nodes per second in this Python implementation (for example 1,624 nodes in 63.2 ms at depth 5 mid-game, ~25,700 nodes/s; 4,904 nodes in 433.9 ms at depth 7 on empty board, ~11,300 nodes/s); with the heuristic about 17,500 to 25,000 nodes per second. A compiled implementation with bitboards would be much faster, but the node counts, which do not depend on the language, would stay the same.
- **Space.** Minimax and Alpha-Beta store only the current path ($O(d)$), thanks to `make_move` / `undo_move`. MCTS stores an explicit tree graph ((N)$) that grows with the simulation budget.
- **Where each method becomes impractical.** In the mid-game position, Alpha-Beta with the heuristic takes 1.46 s at depth 7, 2.69 s at depth 8, and jumps to 30.94 s per move at depth 9 (460,830 nodes) (one run; times vary between runs), confirming the exponential cliff where unassisted fixed-depth search exceeds interactive time limits. Plain Alpha-Beta at depth 9 on the same position takes 9.48 s (385,217 nodes).

---

## Section 8: Error Analysis, Failure Modes & Limitations

### 8.1 Alpha-Beta: Failure Modes
**(a) Exponential cost limits the depth.** Section 5 shows each extra ply costs a factor of about 4 on average (from 1.8x to 8.5x per ply in the mid-game position, Table 5.1) even with pruning. With a fixed depth the response time can become unpredictable; in the mid-game position depth 7 with the heuristic already takes 1.46 s per move.

**(b) Time budgets are position dependent.** Iterative deepening reaches depth 8 in 1 s on the empty board but only depth 6 in the mid-game position (Table 4.2). With 0.05 s the mid-game search only reaches depth 3, so the agent plays a much shallower game under tight clocks.

**(c) Horizon effect.** A threat that materializes just beyond the search depth is invisible. The heuristic tries to reduce this by penalizing opponent threes (Section 3), but it can only approximate what deeper search would find.

**(d) Heuristic weaknesses.** Hand-tuned weights, double counting of overlapping windows, and no knowledge of threat parity (Section 3.5) mean that two positions with equal scores can have very different real values.

**(e) Timeout handling.** When the clock expires, the unfinished iteration is discarded and the move from the last finished depth is played, so a legal move is always returned; the clock is checked at every node, which adds a small overhead. Searching on a board copy keeps the real game state safe (tested).

### 8.2 MCTS: Failure Modes
**(a) Immediate tactics are handled by a guard, not by search.** In the block test (the opponent has three in a row with the fourth cell playable), MCTS chose the blocking column in **20 of 20 runs for every budget tested (5, 20, 100 and 500 simulations)**, and Alpha-Beta at depth 2 also blocked. So single-move tactics are not a weakness of this MCTS implementation, which has a tactical check for one-move wins and blocks. Whether it fails against two-move traps (double threats) was not tested directly; Section 6 reports occasional failures of that kind against deep Alpha-Beta.

**(b) Strength depends on the simulation budget.** Against Alpha-Beta (depth 4, heuristic), with the sides alternated each game:

**Table 8.1 — MCTS vs. Alpha-Beta (depth 4, heuristic)**

| Simulations | Games | MCTS wins | Draws | MCTS losses | Average length of lost games (plies) |
|---|---|---|---|---|---|
| 50 | 10 | 0 | 0 | 10 | 17.9 |
| 200 | 10 | 0 | 0 | 10 | 30.9 |
| 500 | 10 | 3 | 0 | 7 | 29.9 |
| 1000 | 10 | 3 | 0 | 7 | 30.9 |

*(Figure 6, `docs/figures/fig6_mcts_strength.png`, shows the same results.)*

Lost games are much shorter at 50 simulations (17.9 plies) than at 200 or more (about 30 plies); beyond 200 simulations the average length stays flat. MCTS wins 3 of 10 games at both 500 and 1000 simulations and none at 50 or 200, so raising the budget from 500 to 1000 did not help in this run. With 10 games per budget these counts have wide uncertainty (3 of 10 is consistent with a true win rate from roughly 7% to 65%), Alpha-Beta is deterministic, and the MCTS seeds are reused across budgets, so the results are indicative, not conclusive. The block test (Section 8.2a) shows MCTS handles one-move tactics, so these losses are not explained by missed single-move threats.

**(c) Noisy evaluation at low budgets.** With few simulations, each child receives only a handful of random playouts, so its win-rate estimate has high variance and the most-visited move can be chosen by chance.

**(d) Memory grows with the budget.** The tree is stored in memory and grows with the number of simulations ((N)$ dynamic tree nodes), unlike Alpha-Beta.

### 8.3 Comparative Summary
| Aspect | Alpha-Beta (+ iterative deepening) | MCTS |
|---|---|---|
| Guarantee | Exact within the searched depth | Statistical, improves with simulations |
| Main weakness | Exponential cost, horizon effect, hand-made heuristic | High variance at small budgets |
| Time control | Needs iterative deepening | Naturally stoppable at any time |
| Depends on domain knowledge | Yes (heuristic) | No (random playouts), apart from the tactical guard |

### 8.4 Threats to Validity
- **Few positions.** Sections 4 and 5 use two fixed positions; other positions will give different node counts, as the empty vs. mid-game results already show.
- **Few games.** Win/loss counts from 4 to 10 games per setting have wide uncertainty. Alpha-Beta is deterministic and MCTS is seeded, so repeated games are not independent samples of randomness.
- **Different units.** One "node" for Alpha-Beta is one search call; one "node" for MCTS is one simulation. They are shown in the same column of the benchmark tables for convenience, but they are not directly equivalent work.
- **Language speed.** Times were measured in Python on one machine; the ratios between algorithms are more reliable than the absolute milliseconds.

### 8.5 Improvements and Future Work
1. **Better move ordering:** order moves by heuristic value or by the previous iteration's best move at every node.
2. **Transposition table:** the same position is reached by different move orders and is currently searched again each time.
3. **Faster board representation** (bitboards) to raise nodes per second by an order of magnitude.
4. **Tuned heuristic:** tune weights from game data and add threat-parity features.
5. **Stronger MCTS:** heuristic-guided playouts, tuning the exploration constant, and reusing the tree between moves.

### 8.6 Reproducibility
```
python -m pytest tests/ -v
python experiments_cli.py --experiment depth --plot
python experiments_cli.py --experiment iterative
python experiments_cli.py --experiment block
python experiments_cli.py --experiment mcts --games 10 --budgets 50 200 500 1000 --plot
```
Raw results are stored in `docs/results/` (`depth_scaling.csv`, `iterative_depth.csv`, `block_test.csv`, `mcts_vs_alphabeta.csv`).

---

## Additional References (APA 7th Edition)
1. Korf, R. E. (1985). Depth-first iterative-deepening: An optimal admissible tree search. *Artificial Intelligence*, 27(1), 97–109. https://doi.org/10.1016/0004-3702(85)90084-0
2. Pearl, J. (1982). The solution for the branching factor of the alpha-beta pruning algorithm and its optimality. *Communications of the ACM*, 25(8), 559–564. https://doi.org/10.1145/358589.358616

*(Knuth & Moore, 1975; Russell & Norvig; Browne et al., 2012; Kocsis & Szepesvári, 2006; Allen, 1988 and Allis, 1988 are already listed in the references of Sections 1, 6 and 7.)*
