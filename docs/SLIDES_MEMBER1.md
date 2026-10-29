# Member 1 Slides: Algorithm Explanation & Complexity Analysis

Copy each slide into PowerPoint or Google Slides. "Say" lines are speaker notes.
Numbers come from `docs/results/` and Sections 4, 5 and 8 of the report. Two fixed positions were used: the empty board and an 8-ply mid-game position. Timings come from single runs and vary between runs; node counts are exact.

---

## Slide 1: Title and plan
- **Search Agents for Connect Four: Minimax, Alpha-Beta, Heuristic, Iterative Deepening**
- Member 1: Algorithms & Core Logic
- Plan: problem as search, Minimax, Alpha-Beta, heuristic, iterative deepening, complexity, comparison with MCTS
- Say: Two parts today: how the algorithms work, then what they cost.

## Slide 2: The game as a search problem
- State: 6x7 grid, player to move. Actions: columns that are not full (at most 7)
- Result: disc drops to the lowest empty row. Terminal: four in a row, or board full
- About 4.53 x 10^12 reachable positions, so exhaustive search is impossible in real time
- Say: Section 1 shows the size; the point here is that we must search to a limited depth and estimate.

## Slide 3: Minimax
- Two players: MAX (our agent) takes the largest value, MIN (opponent) takes the smallest
- Depth-limited: at depth 0 return the heuristic estimate
- Terminal scores: win +100000 + depth left, loss -100000 - depth left, draw 0
- Why "+ depth": prefers a quick win, delays a loss
- Cost: about 7 children per node, so 7^d nodes
- Say: Draw a small tree with 2 levels and show max and min on the board.

## Slide 4: Alpha-Beta pruning
- alpha = best value MAX is already sure of; beta = best value MIN is already sure of
- MAX node: if value >= beta, stop (MIN above will never allow this branch)
- MIN node: if value <= alpha, stop (MAX above already has better)
- Same answer as Minimax, only fewer nodes (Knuth and Moore, 1975)
- Say: Show a 3-branch example where the second branch is cut after one child.

## Slide 5: Making pruning effective
- Move ordering: center columns first [3, 2, 4, 1, 5, 0, 6]
- make_move / undo_move on one board: memory O(d), no copying
- Same node counting for Minimax and Alpha-Beta, so comparisons are fair
- Say: Best case O(b^(d/2)) needs the best move first; our ordering is a cheap approximation.

## Slide 6: Heuristic evaluation (69 windows)
| Pattern | Score |
|---|---|
| Own disc in center column | +3 |
| Own 3 + 1 empty | +5 |
| Own 2 + 2 empty | +2 |
| Opponent 3 + 1 empty | -6 |
| Opponent 2 + 2 empty | -2 |
| Mixed window | 0 |
- 24 horizontal + 21 vertical + 24 diagonal windows
- Opponent's three weighted a bit higher so the agent blocks early
- Limits: hand-tuned weights, overlapping windows, no threat-parity knowledge
- Say: Tested on hand-made boards (9 unit tests).

## Slide 7: Iterative deepening
- Search depth 1, 2, 3, ... until the time is over; play the move of the last finished depth
- Search runs on a board copy; best move of previous depth is tried first
- Always returns a legal move within the time limit

| Time limit | Empty board depth | Mid-game depth |
|---|---|---|
| 0.05 s | 5 | 3 |
| 0.2 s | 6 | 5 |
| 0.5 s | 7 | 5 |
| 1.0 s | 8 | 6 |
- Say: Depth reached depends on the position, not only on the clock.

## Slide 8: Complexity (theory)
| Algorithm | Time | Space |
|---|---|---|
| Minimax | O(b^d) | O(d) |
| Alpha-Beta, best ordering | O(b^(d/2)) | O(d) |
| Alpha-Beta, average | about O(b^(3d/4)) | O(d) |
| Alpha-Beta, worst | O(b^d) | O(d) |
| MCTS, N simulations | O(N x L) | O(N) |
- b = 7, so best-case effective branching factor is sqrt(7), about 2.65
- Say: L is the playout length, at most 42 moves.

## Slide 9: Measured pruning
| Position | Depth | Minimax nodes | Alpha-Beta nodes | Saved |
|---|---|---|---|---|
| Empty | 3 | 399 | 75 | 81.2% |
| Empty | 4 | 2,800 | 172 | 93.9% |
| Empty | 5 | 19,607 | 563 | 97.1% |
| Mid-game | 5 | 18,544 | 1,624 | 91.2% |
- Pruning grows with depth and is lower in tactical positions
- Add chart: docs/figures/fig1_execution_time_vs_depth.png or docs/figures/fig2_nodes_expanded_log_scale.png

## Slide 10: Effective branching factor and the depth cliff
- Minimax: b* about 7.2 (matches 7^d)
- Alpha-Beta: b* about 3.4 (empty) and 4.3 (mid-game): between best case 2.65 and worst case 7
- Mid-game, Alpha-Beta + heuristic: 31,833 nodes at depth 7, 73,986 at depth 8, 460,830 at depth 9 (about 31 s in one run)
- Say: Each extra ply costs about 4x on average, but unevenly (odd/even effect).

## Slide 11: Alpha-Beta vs MCTS
| | Alpha-Beta + iterative deepening | MCTS |
|---|---|---|
| Guarantee | Exact within searched depth | Statistical |
| Needs domain knowledge | Yes (heuristic) | No (apart from a tactical guard) |
| Time control | Needs iterative deepening | Stop any time |
| Memory | O(d) | O(N) |
- Block test: MCTS blocked a one-move threat 20/20 times at 5, 20, 100 and 500 simulations
- MCTS vs Alpha-Beta (depth 4, heuristic), 10 games each: 0 wins at 50 and 200 simulations, 3 wins at 500, 3 wins at 1000
- Be careful: 10 games is a small sample, results are indicative, not conclusive
- Add chart: docs/figures/fig6_mcts_strength.png

## Slide 12: Limitations and future work
- Exponential cost; horizon effect; hand-tuned heuristic; position-dependent time
- Next: better move ordering, transposition table, bitboards, tuned heuristic with threat parity
- MCTS: heuristic-guided playouts, tune exploration constant, reuse tree between moves

## Backup slide: Viva questions
- Why does value >= beta stop the loop in a max node?
- Why is the result of Alpha-Beta the same as Minimax?
- Best and worst case of Alpha-Beta; why does move ordering matter?
- Why is the opponent's three weighted -6 but ours +5?
- Why does iterative deepening not waste time?
- Why is the search run on a copy of the board?
- Why does a node count for MCTS not equal a node count for Alpha-Beta?
