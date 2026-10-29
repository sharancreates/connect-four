# ALGORITHMS.md: Algorithmic Architecture & Mathematical Foundations

Explains the search algorithms, heuristics, and evaluation mechanics implemented across the Connect Four AI engine.
Source files reside in `connect4/agents/`, tests reside in `tests/`.

## 1. Algorithmic Modules

| File | Module Description |
|------|--------------------|
| `minimax_agent.py` | Vanilla depth-limited Minimax without pruning (state-space baseline). |
| `alphabeta_agent.py` | Minimax with Alpha-Beta pruning, center-out move ordering, and heuristic toggle. |
| `heuristic.py` | Evaluation function used at the depth limit (center control, open threes/twos, opponent threats across 69 windows). |
| `iterative_agent.py` | Iterative deepening on top of Alpha-Beta, with per-node time budgeting and graceful fallback. |
| `mcts_agent.py` | Monte Carlo Tree Search with UCT selection, random rollouts, and 1-ply tactical guards. |
| `tests/test_alphabeta.py` | Alpha-Beta move parity with Minimax, node reduction checks, immediate win/block verification. |
| `tests/test_heuristic.py` | 69-window heuristic evaluation verified against hand-crafted board states. |
| `tests/test_iterative.py` | Time budget compliance, board state safety, and depth progression verification. |
| `tests/test_mcts.py` | UCT child selection, rollout termination, and tactical guard checks. |

## 2. Minimax and Alpha-Beta Pruning

### 2.1 Theoretical Formulation
Minimax explores every possible legal game trajectory down to a fixed depth limit $d$. In a zero-sum game:
- MAX (Player $+1$) chooses actions maximizing utility: $\max_{a \in \mathcal{A}(s)} V(s')$
- MIN (Player $-1$) chooses actions minimizing utility: $\min_{a \in \mathcal{A}(s)} V(s')$

Alpha-Beta pruning tracks two scalar bounds during tree traversal:
- $\alpha$: the highest utility guaranteed to the maximizing player along the current path.
- $\beta$: the lowest utility guaranteed to the minimizing player along the current path.

**Pruning Conditions:**
- In a MAX node, if the return value satisfies $v \ge \beta$, the minimizing ancestor will never allow this branch, triggering an immediate cutoff.
- In a MIN node, if the return value satisfies $v \le \alpha$, the maximizing ancestor already has a superior alternative, triggering an immediate cutoff.

Alpha-Beta is mathematically guaranteed to return the exact same minimax value as exhaustive search while evaluating significantly fewer states (Knuth & Moore, 1975).

### 2.2 Move Ordering Optimization
Pruning efficiency depends heavily on the sequence in which successor moves are evaluated. Under optimal ordering (best move evaluated first at every node), the effective branching factor drops from $b$ to $b^* = \sqrt{b}$.

In our implementation, moves are evaluated center-out:
$$\text{Column Priority} = [3, 2, 4, 1, 5, 0, 6]$$
Central columns participate in far more potential winning lines (column 3 participates in 51 distinct 4-in-a-row windows), establishing tight $\alpha$-$\beta$ bounds early in the traversal.

### 2.3 Measured Search Space Reduction (`docs/results/depth_scaling.csv`)
In standardized depth-scaling benchmarks on an empty board:
- At depth $d = 3$: Minimax expands 399 nodes vs. 75 nodes for Alpha-Beta (81.2% reduction).
- At depth $d = 4$: Minimax expands 2,800 nodes vs. 172 nodes for Alpha-Beta (93.9% reduction).
- At depth $d = 5$: Minimax expands 19,607 nodes (633.9 ms) vs. 563 nodes (28.3 ms) for Alpha-Beta (**97.1% reduction, ~22× faster**).
- In a dense mid-game position at depth $d = 5$: Minimax expands 18,544 nodes vs. 1,624 nodes for Alpha-Beta (**91.2% reduction, ~10× faster**).

*Note: Nodes count every recursive call. Minimax was evaluated up to depth 5 only.*

---

## 3. 69-Window Heuristic Evaluator (`heuristic.py`)

When the search reaches depth limit $d = 0$ on a non-terminal state, utility is estimated using a precomputed evaluation matrix scanning all **69 winning 4-in-a-row windows**:
- **24 horizontal** windows ($6 \text{ rows} \times 4 \text{ windows/row}$)
- **21 vertical** windows ($7 \text{ columns} \times 3 \text{ windows/col}$)
- **24 diagonal** windows (12 with positive slope, 12 with negative slope)

### 3.1 Scoring Weights
| Window Pattern | Utility Weight | Rationale |
|---|---|---|
| Own disc in column 3 (Center) | $+3$ | Controls central columns with maximum connectivity (51 windows). |
| Own 3 discs $+ 1$ empty cell | $+5$ | Immediate offensive threat (potential 1-ply win). |
| Own 2 discs $+ 2$ empty cells | $+2$ | Emerging offensive alignment. |
| Opponent 3 discs $+ 1$ empty cell | $-6$ | Critical defensive threat; weighted higher to prioritize blocking. |
| Opponent 2 discs $+ 2$ empty cells | $-2$ | Emerging opponent alignment. |
| Contested window (both players present) | $0$ | Window can never yield a 4-in-a-row victory. |

Terminal scores ($\pm 100{,}000 \pm \text{depth}$) strictly dominate any heuristic evaluation, ensuring the agent always prefers immediate forced victories and delays unavoidable losses.

---

## 4. Iterative Deepening with Time Budget (`iterative_agent.py`)

Iterative deepening runs successive depth-bounded Alpha-Beta searches at depths $d = 1, 2, 3, \dots$ until a wall-clock deadline expires.
- **Anytime Property**: Always maintains a valid completed move from the last finished depth iteration.
- **Move Ordering Re-use**: The best move identified at depth $d-1$ is evaluated first at depth $d$, accelerating pruning.
- **State Integrity**: Deliberation executes on `board.copy()`; a timeout occurring mid-search safely unwinds without altering the live match state.
- **Measured Depth Reach (`docs/results/iterative_depth.csv`)**:
  - Empty board: reaches depth 5 at 0.05 s, depth 6 at 0.2 s, depth 7 at 0.5 s, and depth 8 at 1.0 s.
  - Mid-game position: reaches depth 3 at 0.05 s, depth 5 at 0.2 s, depth 5 at 0.5 s, and depth 6 at 1.0 s.

---

## 5. Monte Carlo Tree Search with UCT (`mcts_agent.py`)

MCTS constructs an asymmetric search tree guided by Monte Carlo simulations over four phases:
1. **Selection**: Starting from root, traverses existing tree nodes using the Upper Confidence Bound for Trees (UCT) formula:
   $$\text{UCT}(v_i) = \frac{Q(v_i)}{N(v_i)} + c \sqrt{\frac{2 \ln N(v)}{N(v_i)}}$$
   - Exploitation term: empirical win rate $\frac{Q(v_i)}{N(v_i)}$.
   - Exploration term: bonus scaled by relative visit frequencies.
   - **Exploration Constant**: In our code, $c = 1.414$ multiplies $\sqrt{\frac{2 \ln N}{n_i}}$, meaning the effective exploration coefficient is $c \sqrt{2} \approx 1.414 \times 1.4142 \approx 2.0$ (approximately $1.4\times$ standard theoretical UCB1).
2. **Expansion**: Instantiates a new child `MCTSNode` for an unvisited legal action.
3. **Simulation (Rollout)**: Fast stochastic playout to terminal outcome (win, loss, or draw).
4. **Backpropagation**: Playout reward propagated up the tree lineage, updating visit counts $N$ and value sums $Q$.

### 5.1 Tactical Guards
MCTS features a 1-ply tactical check at the root:
- If any legal move yields an immediate victory, that column is played immediately without simulation.
- If the opponent possesses an immediate winning threat, MCTS forces a block.
- Empirical validation (`docs/results/block_test.csv`): MCTS successfully blocks 20 of 20 times across budgets of 5, 20, 100, and 500 simulations.

---

## 6. Empirical Datasets (`docs/results/`)

All experimental results cited across documentation are persisted in structured CSV files under `docs/results/`:
1. `depth_scaling.csv`: Node expansions and single-run wall-clock timings across depths 1–9 on empty board and mid-game positions for Minimax (depths 1–5), Alpha-Beta, and Alpha-Beta + heuristic.
2. `iterative_depth.csv`: Depth completed under time limits ($0.05\text{ s}, 0.2\text{ s}, 0.5\text{ s}, 1.0\text{ s}$) across positions.
3. `mcts_vs_alphabeta.csv`: 10-game match outcomes (wins, draws, losses, average plies when lost) for MCTS budgets of 50, 200, 500, and 1000 simulations against Alpha-Beta ($d=4$).
4. `block_test.csv`: Immediate tactical threat response rates across MCTS budgets.
5. `tournament.csv`: 200-game round-robin tournament records (20 games per pair, alternating starting mover) across Random, Minimax ($d=3$), Alpha-Beta ($d=4$), Alpha-Beta ($d=6$), and MCTS ($N=500$).

---

## 7. Future Work & Board Representations

- **Bitboard Optimization**: The current board representation utilizes a 2D contiguous NumPy `int8` array. Implementing 64-bit binary bitboards (two `uint64` masks for Player 1 and Player 2) would enable bitwise gravity shifts and $O(1)$ four-in-a-row alignment detection, significantly increasing simulation throughput per second.
- **Transposition Tables**: Integrating Zobrist hashing with an LRU cache to store previously evaluated bounds and avoid re-searching transposed board permutations.
