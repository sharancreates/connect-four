# ALGORITHMS.md: Member 1 (Algorithms & Core Logic)

Explains the search code added in Week 2 so that anyone on the team can follow it.
Files live in `connect4/agents/`, tests live in `tests/`.

## 1. What was added

| File | What it does |
|------|--------------|
| `alphabeta_agent.py` | Minimax + Alpha-Beta pruning. Same scoring as `minimax_agent.py`, so node counts compare fairly. |
| `heuristic.py` | Evaluation function used at the depth limit (center control, open threes/twos, opponent threats). |
| `iterative_agent.py` | Iterative deepening on top of Alpha-Beta, with a time budget per move. |
| `tests/test_alphabeta.py` | Same move as Minimax, fewer nodes, takes a win, blocks a loss. |
| `tests/test_heuristic.py` | Heuristic checked on hand-made boards. |
| `tests/test_iterative.py` | Time limit respected, board unchanged, takes an immediate win. |

## 2. Alpha-Beta pruning

### Theory
Minimax looks at every move of both players down to the depth limit.
Alpha-Beta keeps two numbers while searching:
- `alpha`: best score the maximizing player (us) is already sure of
- `beta`: best score the minimizing player (opponent) is already sure of

If `value >= beta` in a max node, the opponent will never allow this branch, so the remaining moves are skipped.
If `value <= alpha` in a min node, we already have something better elsewhere, so the remaining moves are skipped.
The final move is the same as Minimax, only the number of nodes is smaller.
Moves are tried center-first, because good moves first means more pruning.

### Result (depth 4, one full game, Minimax vs Alpha-Beta)

| | Plain Minimax | Alpha-Beta |
|---|---|---|
| Total nodes | 17,134 | 1,726 |
| Total time | 1907.86 ms | 245.33 ms |

About 9.9x fewer nodes and 7.8x less time.

## 3. Heuristic evaluation (`heuristic.py`)

Used when the depth limit is reached and the game is not finished.
It looks at all 69 windows of 4 cells (24 horizontal, 21 vertical, 24 diagonal).

| Pattern | Score |
|---------|-------|
| Each own disc in the center column | +3 |
| Window with 3 own discs and 1 empty | +5 |
| Window with 2 own discs and 2 empty | +2 |
| Window with 3 opponent discs and 1 empty | -6 |
| Window with 2 opponent discs and 2 empty | -2 |
| Window with both players' discs | 0 (can never become 4) |

The opponent's three is weighted higher than our own three so the agent blocks threats early.
All weights are constants at the top of the file, so they are easy to tune.
Terminal scores (win = 100000, loss = -100000) are always far larger than any heuristic score.

## 4. Iterative deepening (`iterative_agent.py`)

### Theory
Search depth 1, then depth 2, then depth 3 and so on, until the time budget is over.
The move from the last finished depth is played. This gives an answer at any time limit.
Re-searching shallow depths looks wasteful, but the deepest level costs far more than all the shallow ones together.
The best move of the previous depth is tried first at the next depth, which improves pruning.
The search stops early if a forced win is found.

### Details worth remembering
- The clock is checked at every node. When time runs out a `TimeUp` exception stops the search.
- The search runs on `board.copy()`, so a timeout in the middle cannot leave the real board changed.
- `depth_reached` stores the last depth that finished in time.

## 5. How to run

```
python -m pytest tests/ -v
python main.py --mode agent-vs-agent --agent1 minimax --agent2 alphabeta --depth1 4 --depth2 4
python main.py --mode agent-vs-agent --agent1 alphabeta --agent2 iterative --depth1 4 --time2 1.0
```

## 6. Results with heuristic and iterative deepening

| Match | Agent 1 (X) | Agent 2 (O) | Winner | Turns | P1 Time (ms) | P1 Nodes | P2 Time (ms) | P2 Nodes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| (a) Heuristic impact | AlphaBeta (d=4, center-only) | AlphaBeta (d=4, heuristic) | **Agent 2 (O)** | 34 | 167.06 | 1,766 | 402.53 | 2,441 |
| (b) Iterative deepening | AlphaBeta (d=4, center-only) | Iterative (d=10, 1.0s budget) | **Agent 2 (O)** | 20 | 108.58 | 1,499 | 7119.36 | 60,920 |
| (c) Baseline sanity check | Random | Iterative (d=10, 0.5s budget) | **Agent 2 (O)** | 8 | 0.13 | 4 | 1019.73 | 8,789 |

Enabling the 69-window heuristic evaluation allows Alpha-Beta to evaluate tactical disc alignments across all orientations, leading to a win over the center-only agent in 34 turns. With iterative deepening and a 1.0s per-move budget, the agent explores deeper plies (over 60,000 nodes total while adhering strictly to time constraints), decisively defeating the fixed depth-4 agent in 20 turns. Against random play, the iterative deepening agent rapidly spots winning patterns and seals victory in only 8 turns.

## 7. Viva questions to be ready for

- Why does `value >= beta` stop the loop in a max node?
- Why is the result of Alpha-Beta the same as Minimax?
- What is the best case and worst case of Alpha-Beta, and why does move ordering matter?
- Why is the opponent's open three weighted -6 but our own +5?
- Why does iterative deepening not waste time?
- Why is the search run on a copy of the board?

## 8. Week 3 additions (scaling and error analysis)

Week 3 focused on systematic complexity profiling, failure-mode analysis, and head-to-head benchmarking between heuristic Alpha-Beta search and statistical Monte Carlo Tree Search:

- **Experimentation Harness (`experiments_cli.py`):**
  A dedicated testing harness to run automated depth-scaling benchmarks (depths 3 to 9), iterative deepening deadline rollbacks, one-move tactical block tests, and MCTS simulation budget sweeps (50, 200, 500, 1000 rollouts).
- **Empirical Datasets (`docs/results/`):**
  Outputs are persisted as structured CSVs: `depth_scaling.csv`, `iterative_scaling.csv`, `mcts_budget_scaling.csv`, and `ordering_comparison.csv`.
- **Academic Milestone Report (`docs/STAGE3_REPORT_SECTIONS_2_3_4_5_8.md`):**
  Contains formal mathematical specifications, depth-growth measurements, effective branching factor calculations ($b^* \approx N^{1/d}$ between 3.4 and 4.4), empirical throughput, and comprehensive error analysis covering tactical horizon effects, single-move guards, and budget sensitivity.
- **Viva Defense Slides (`docs/SLIDES_MEMBER1.md`):**
  Slide-by-slide presentation outline and speaker notes covering problem formulation, search algorithms, heuristic design, empirical complexity, and comparative failure modes.

