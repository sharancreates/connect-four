<div align="center">

# 🔴🟡 CONNECT FOUR AI
### *Adversarial Search meets Monte Carlo Tree Search*

[![Tests](https://img.shields.io/badge/Test%20Suite-54%2F54%20Passing-10B981?style=for-the-badge&logo=pytest&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Pygame](https://img.shields.io/badge/GUI-Pygame%20Interactive-E11D48?style=for-the-badge&logo=gamemaker&logoColor=white)]()
[![Course](https://img.shields.io/badge/Course-ECSCT24301-8B5CF6?style=for-the-badge)]()
[![Adani University](https://img.shields.io/badge/Adani%20University-FEST%20AI--ML-DC2626?style=for-the-badge)]()

<br>

```text
       ___                                _     ___                 
      / __\___  _ __  _ __   ___  ___  __| |_  / __\___  _   _ _ __ 
     / /  / _ \| '_ \| '_ \ / _ \/ __|/ _` (_) / _\/ _ \| | | | '__|
    / /__| (_) | | | | | | |  __/ (__| (_| |_ / / | (_) | |_| | |   
    \____/\___/|_| |_|_| |_|\___|\___|\__,_(_)\_/   \___/ \__,_|_|   
                     [ 🔴 ⚪ ⚪ ⚪ ⚪ ⚪ 🟡 ]
```

<p align="center">
  <b>A research-grade adversarial game engine benchmarking exact heuristic minimax reasoning against statistical Monte Carlo rollouts on a standard 6×7 grid.</b>
</p>

[🎮 Quickstart](#-quickstart--gameplay-modes) •
[🧠 Algorithmic Models](#-algorithmic-models) •
[📊 Benchmark Results](#-empirical-benchmarks--results) •
[✨ Pygame GUI](#-graphical-interface) •
[👥 Team Distribution](#-team-work-distribution)

---

</div>

## 🌌 The Mission

In a discrete $6 \times 7$ grid with $\approx 4.53 \times 10^{12}$ reachable positions and over $10^{21}$ possible game tree paths, Connect Four provides an ideal proving ground for AI reasoning. Exhaustive brute-force search is computationally intractable in real time, exposing a fundamental question in Artificial Intelligence:

> **When under strict thinking-time and compute constraints, does depth-bounded heuristic pruning (Alpha-Beta) outperform statistical simulation-based approximation (MCTS with UCT)?**

This project investigates, implements, and benchmarks both paradigms head-to-head under standardized tournament protocols and experimental harnesses.

---

## 👥 Team Work Distribution (3-Week Sprint)

> **Course:** ECSCT24301 – Foundation of AI (Track A: Applied AI System Development)  
> **Team of 2:** Responsibilities partitioned across algorithmic core and systems evaluation.

| Role | Member | Responsibilities | Status |
| :--- | :--- | :--- | :---: |
| **Member 1** | *Algorithms & Core Logic* | Alpha-Beta pruning, 69-window heuristic evaluation, iterative deepening with time budgeting, theoretical formulation (`docs/ALGORITHMS.md`), empirical depth scaling and failure-mode analysis, Stage 3 report sections (2, 3, 4, 5, 8), slide outline. | ✅ **Week 1, 2 & 3 Complete** |
| **Member 2** | *Engineering, GUI & Evaluation* | Modular repository scaffolding, PEAS formulation, performance instrumentation (`time.perf_counter`, `NodeCounter`), CLI & Pygame GUI, MCTS with UCT, automated tournament benchmark harness, publication figures generator, Stage 3 report sections (1, 6, 7), viva guide. | ✅ **Week 1, 2 & 3 Complete** |

### 📋 Week 3 Milestone Status (All Deliverables Complete)
#### Member 1 (Person A) Deliverables
- [x] **Scaling Experiments (`experiments_cli.py`)**: Depth-scaling complexity benchmarks for Minimax and Alpha-Beta up to depth 9 across empty and mid-game positions.
- [x] **Empirical Metrics & Plotting**: Persisted experimental data in `docs/results/` (`depth_scaling.csv`, `iterative_depth.csv`, `mcts_vs_alphabeta.csv`, `block_test.csv`) and generated charts in `docs/figures/` (`fig1`, `fig2`, `fig3`, `fig6`).
- [x] **Error & Failure-Mode Analysis**: Evaluated tactical horizon effects, one-move tactical guards, and MCTS simulation budget curves (50, 200, 500, 1000 rollouts).
- [x] **Academic Report Sections**: Authored Sections 2, 3, 4, 5, and 8 in `docs/STAGE3_REPORT_SECTIONS_2_3_4_5_8.md`.
- [x] **Viva Defense Slide Outline**: Comprehensive slide breakdown and speaker notes in `docs/SLIDES_MEMBER1.md`.

#### Member 2 (Person B) Deliverables
- [x] **Publication Plotting Suite (`plotter_cli.py`)**: Automated 300 DPI figure generator for execution latency (Fig 1), semi-log node expansion scale (Fig 2), $5 \times 5$ tournament win-rate heatmap (Fig 3), and MCTS simulation scaling (Fig 6).
- [x] **Tournament Benchmarking**: Multi-game round-robin tournament harness with alternating turns to eliminate first-player bias (`benchmark_cli.py`), persisting 200 games to `docs/results/tournament.csv`.
- [x] **Academic Report Sections**: Authored Sections 1, 6, 7, and cross-section synthesis in `docs/STAGE3_REPORT_SECTIONS_1_6_7.md`.
- [x] **Viva Defense Guide**: Complete defense guide, 3-minute opening pitch, live demonstration script, and honest experimental limitations in `docs/VIVA_TALKING_POINTS_PERSON_B.md`.
- [x] **Joint Defense Deck**: Unified presentation deck combining both members' contributions with balanced speaking roles.

---

## 🧠 Algorithmic Models

```
                                  ┌───────────────────────────┐
                                  │   CONNECT FOUR AGENTS     │
                                  └─────────────┬─────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
      [ Baseline Agents ]            [ Deterministic Search ]       [ Statistical Rollouts ]
      • Random Uniform Baseline      • Plain Minimax (No Pruning)   • MCTS (UCT Policy)
                                     • Alpha-Beta with Center Bias  • Dual-Budget (Sims & Time)
                                     • 69-Window Heuristic          • Tactical Guards
                                     • Iterative Deepening
```

### 1. Baseline Random Agent
Uniformly samples from valid, non-full columns. Establishes the lower-bound sanity baseline ($O(1)$ move selection).

### 2. Plain Minimax (No Pruning)
Exhaustive depth-bounded adversarial search evaluating all branches. Demonstrates the raw combinatorial state-space explosion before pruning optimizations. Evaluated up to depth 5.

### 3. Minimax with Alpha-Beta Pruning
Implements branch cutoff whenever $\alpha \ge \beta$ with center-out column ordering (`[3, 2, 4, 1, 5, 0, 6]`). Delivers a **97.1% node reduction** at depth 5 over plain minimax on an empty board.

### 4. 69-Window Heuristic Evaluator
Calculates utility across all **69 winning lines** on a $6 \times 7$ board:
- **24 horizontal** 4-tuples
- **21 vertical** 4-tuples
- **24 diagonal** 4-tuples (12 positive slope, 12 negative slope)

Weights open-3 threats ($-6$ opponent, $+5$ own), open-2 sequences ($\pm 2$), and center control ($+3$) dynamically.

### 5. Iterative Deepening with Time Budget
Searches depths $d = 1, 2, 3, \dots$ progressively. Employs per-node deadline checks with graceful rollback to the deepest fully completed iteration, guaranteeing move delivery within wall-clock constraints.

### 6. Monte Carlo Tree Search (MCTS) with UCT
Employs four-stage exploration:
1. **Selection**: Traverses tree using Upper Confidence Bound:
   $$\text{UCT}(i) = \frac{w_i}{n_i} + c \sqrt{\frac{2 \ln N}{n_i}} \quad (c = 1.414)$$
   *Note: With $c = 1.414$ multiplying $\sqrt{\frac{2 \ln N}{n_i}}$, the effective exploration weight is $c \sqrt{2} \approx 2.0$, which is approximately $1.4\times$ standard theoretical UCB1.*
2. **Expansion**: Adds new child state node for an unvisited legal action.
3. **Simulation (Rollout)**: Fast stochastic simulation to terminal state.
4. **Backpropagation**: Playout rewards propagated to parent lineage.
*Features dual-mode budgeting (fixed simulation count or sub-second wall-clock limit) and root-level 1-ply tactical checks.*

---

## 🎮 Quickstart & Gameplay Modes

### 📦 1. Installation
```bash
# Clone the repository
git clone https://github.com/sharancreates/connect-four.git
cd connect-four

# Install dependencies (Python 3.10+)
pip install -r requirements.txt
```

### 🧪 2. Run the Verification Suite
```bash
python -m pytest tests/ -v
```
> *Runs all 54 unit and integration tests across board mechanics, heuristics, search parity, MCTS, benchmarking, and plotter logic in ~10-15 seconds.*

---

### 🕹️ 3. Play via Pygame Interactive GUI

Launch a visual, hardware-rendered Connect Four board with mouse hover discs and real-time AI move indicators:

```bash
# Play Human vs. MCTS Agent
python gui_main.py --agent mcts --simulations 400

# Play Human vs. Alpha-Beta (with Heuristic)
python gui_main.py --agent alphabeta --depth 4

# Play Human vs. Iterative Deepening (1 second time budget)
python gui_main.py --agent iterative --depth 8 --time-limit 1.0
```

---

### 💻 4. Interactive Command-Line Interface (CLI)

```bash
# Human (Red 'X') vs. AI (Yellow 'O') in console
python main.py --mode human-vs-agent --agent2 mcts --simulations2 500

# Watch AI vs AI clash with turn telemetry
python main.py --mode agent-vs-agent --agent1 alphabeta --agent2 mcts --depth1 4 --simulations2 300 --delay 0.4
```

---

### 🏆 5. Automated Tournament & Benchmarking CLI

```bash
# Run a 20-game head-to-head match series with alternating turns
python benchmark_cli.py --agent1 alphabeta --agent2 mcts --games 20 --depth1 4 --simulations2 500

# Run full round-robin tournament (200 games across 5 agents)
python benchmark_cli.py --round-robin --games 20 --output docs/results/tournament.csv

# Generate 300 DPI publication figures from results CSVs
python plotter_cli.py --output-dir docs/figures
```

---

### 📈 6. Scaling & Failure-Mode Experiments (`experiments_cli.py`)

```bash
# 1. Depth-scaling complexity benchmark (Minimax up to d=5, Alpha-Beta up to d=9) with plot
python experiments_cli.py --experiment depth --plot

# 2. Iterative deepening deadline test across multiple time allocations
python experiments_cli.py --experiment iterative

# 3. Tactical block test verifying immediate threat response
python experiments_cli.py --experiment block

# 4. MCTS simulation budget sweep against Alpha-Beta (10 games per budget) with plot
python experiments_cli.py --experiment mcts --games 10 --budgets 50 200 500 1000 --plot
```

---

## 📊 Empirical Benchmarks & Results

All metrics below are drawn directly from persisted empirical datasets in `docs/results/`.

### 1. Depth Scaling & Pruning Efficiency (`docs/results/depth_scaling.csv`)
*Nodes count every recursive call. Minimax was run to depth 5 only; no depth-6 Minimax measurement exists. Timings are single runs and noisy; node counts are exact.*

- **Empty Board at Depth 5**:
  - Vanilla Minimax: **19,607 nodes** | **633.85 ms**
  - Alpha-Beta (Center Order): **563 nodes** | **28.25 ms**
  - **Pruning Gain**: **97.1% fewer nodes**, **~22× faster**
- **Mid-Game Position at Depth 5**:
  - Vanilla Minimax: **18,544 nodes** | **619.11 ms**
  - Alpha-Beta (Center Order): **1,624 nodes** | **63.17 ms**
  - **Pruning Gain**: **91.2% fewer nodes**, **~10× faster**
- **Alpha-Beta at Depth 6 (Empty Board)**: **1,248 nodes** | **49.42 ms**

### 2. Iterative Deepening Search Reach (`docs/results/iterative_depth.csv`)
- **Empty Board**: Reaches depth 5 (0.05 s), depth 6 (0.2 s), depth 7 (0.5 s), and depth 8 (1.0 s).
- **Mid-Game Position**: Reaches depth 3 (0.05 s), depth 5 (0.2 s), depth 5 (0.5 s), and depth 6 (1.0 s).

### 3. MCTS Simulation Scaling & Tactical Checks (`docs/results/mcts_vs_alphabeta.csv`, `block_test.csv`)
- **MCTS vs. Alpha-Beta ($d=4$, Heuristic)** across 10 games per budget:
  - 50 simulations: 0 wins, 10 losses (avg lost length: 17.9 plies)
  - 200 simulations: 0 wins, 10 losses (avg lost length: 30.9 plies)
  - 500 simulations: 3 wins, 7 losses (avg lost length: 29.9 plies)
  - 1000 simulations: 3 wins, 7 losses (avg lost length: 30.9 plies)
- **1-Ply Tactical Block Test**: MCTS successfully blocked immediate winning threats in **20/20** tests across all budgets (5, 20, 100, 500 simulations) via its root tactical check.

### 4. Round-Robin Tournament (`docs/results/tournament.csv`)
*200 games total, 20 games per pair, strictly alternating first mover. Scored 1 point for win, 0.5 for draw, 0 for loss (out of 80 points total across 4 opponent matchups).*

| Agent | Configuration | Points (/80) | Score % | Matchup Results (W-D-L) |
|---|---|:---:|:---:|---|
| **Alpha-Beta** | Depth $d = 6$ | **57.0** | 71.3% | vs Random: 20-0-0 \| vs Minimax: 10-10-0 \| vs AB(d=4): 0-20-0 \| vs MCTS: 12-0-8 |
| **Alpha-Beta** | Depth $d = 4$ | **55.5** | 69.4% | vs Random: 20-0-0 \| vs Minimax: 10-10-0 \| vs AB(d=6): 0-20-0 \| vs MCTS: 10-1-9 |
| **MCTS** | $N = 500$ sims | **52.5** | 65.6% | vs Random: 20-0-0 \| vs Minimax: 15-0-5 \| vs AB(d=4): 9-1-10 \| vs AB(d=6): 8-0-12 |
| **Minimax** | Depth $d = 3$ | **35.0** | 43.8% | vs Random: 20-0-0 \| vs AB(d=4): 0-10-10 \| vs AB(d=6): 0-10-10 \| vs MCTS: 5-0-15 |
| **Random** | Uniform | **0.0** | 0.0% | 0-0-20 vs each agent (0-0-80 overall) |

> **Tournament Evaluation Note:** The tournament uses deterministic agents, so some pairings repeat the same game (effectively 2 distinct games per pair, one for each starting player). The top three agents cannot be separated statistically with 20 games per pair.

---

## 📁 Repository Anatomy

```
connect-four/
├── connect4/                   # Core application package
│   ├── core/
│   │   └── board.py            # 6x7 NumPy int8 Board, gravity, undo, coordinate win-checks
│   ├── agents/                 # Adversarial & simulation intelligence
│   │   ├── base.py             # Polymorphic Agent interface & statistics
│   │   ├── random_agent.py     # Uniform random baseline
│   │   ├── minimax_agent.py    # Exhaustive depth-limited Minimax (depth 1–5 baseline)
│   │   ├── alphabeta_agent.py  # Minimax with Alpha-Beta pruning & heuristic toggle
│   │   ├── heuristic.py        # Precomputed 69-window evaluation matrix
│   │   ├── iterative_agent.py  # Iterative deepening Alpha-Beta with time budget
│   │   └── mcts_agent.py       # Monte Carlo Tree Search with UCT & tactical guards
│   ├── benchmark/              # Telemetry & Tournament Evaluation
│   │   ├── instrumentation.py  # Sub-ms perf_counter timer & NodeCounter wrapper
│   │   ├── runner.py           # Multi-game tournament runner with alternating turns
│   │   └── plotter.py          # Publication-grade Matplotlib plotting engine
│   ├── cli/
│   │   └── game_loop.py        # Terminal loop with live telemetry & board formatting
│   └── gui/
│       └── pygame_app.py       # 700x700px graphical Pygame board with hover & drops
├── docs/                       # Academic & Engineering documentation
│   ├── CODING_CONVENTIONS.md   # PEP 8, type hints & collaboration standards
│   ├── PEAS_AND_PROBLEM_STATEMENT.md # Academic PEAS & formal state-space draft
│   ├── ALGORITHMS.md           # Mathematical formulations, heuristic windows & UCT
│   ├── STAGE3_REPORT_SECTIONS_1_6_7.md # Academic report sections (Member 2)
│   ├── STAGE3_REPORT_SECTIONS_2_3_4_5_8.md # Academic report sections (Member 1)
│   ├── SLIDES_MEMBER1.md       # Presentation slide outline (Member 1)
│   ├── VIVA_TALKING_POINTS_PERSON_B.md # Viva preparation guide & limitations (Member 2)
│   ├── results/                # Measured CSV benchmark datasets (depth, MCTS, tournament)
│   └── figures/                # Publication-quality benchmark visualization charts (Figs 1, 2, 3, 6)
├── tests/                      # Automated Test Suite (54 Tests, 100% Pass)
│   ├── test_board.py           # Board mechanics, gravity, edge cases (9 tests)
│   ├── test_agents.py          # Random & Minimax baseline tests (4 tests)
│   ├── test_alphabeta.py       # Alpha-Beta parity & pruning verification (4 tests)
│   ├── test_heuristic.py       # 69-window score symmetry & threat checks (9 tests)
│   ├── test_iterative.py       # Iterative deepening time cutoffs & fallbacks (4 tests)
│   ├── test_mcts.py            # UCT selection, rollouts, deterministic seeding (6 tests)
│   ├── test_benchmark_runner.py# Tournament runner & turn alternation (2 tests)
│   ├── test_plotter.py         # Publication figures & CSV parsing (6 tests)
│   ├── test_gui.py             # Headless GUI event loop & coordinate mapping (2 tests)
│   ├── test_instrumentation.py # Timer & node counter checks (3 tests)
│   └── test_game_loop.py       # End-to-end simulated match test (1 test)
├── main.py                     # Unified CLI executable runner
├── gui_main.py                 # Pygame graphical application launcher
├── benchmark_cli.py            # Tournament evaluation runner
├── experiments_cli.py          # Scaling & failure-mode experimentation harness
├── plotter_cli.py              # Automated publication figures generator
└── requirements.txt            # Python dependencies (NumPy, Pygame, Pytest, Matplotlib)
```

---

## 🎨 Milestones Completed & Next Steps

```text
  [ Week 1: Foundation & Baselines ] ──────────► COMPLETE (17/17 tests)
  • Board Engine • Baselines (Random & Minimax) • CLI Loop • Instrumentation • PEAS Draft
                                     │
                                     ▼
  [ Week 2: Advanced Heuristics & MCTS ] ──────► COMPLETE (44/44 tests)
  • Alpha-Beta Pruning • 69-Window Heuristic • Iterative Deepening • MCTS (UCT) • Pygame GUI
                                     │
                                     ▼
  [ Week 3: Tournament, Scaling & Scientific Report ] ──► COMPLETE (54/54 tests)
  • Round-Robin Tournament (200 games) • Depth & Budget Scaling • Final Report & Slides
```

---

<div align="center">
  <sub>Developed for ECSCT24301 Foundation of AI • Adani University (FEST)</sub><br>
  <sub>Built with ❤️ using Python, NumPy & Pygame</sub>
</div>
