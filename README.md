<div align="center">

# 🔴🟡 CONNECT FOUR AI
### *Adversarial Search meets Monte Carlo Tree Search*

[![Tests](https://img.shields.io/badge/Test%20Suite-53%2F53%20Passing-10B981?style=for-the-badge&logo=pytest&logoColor=white)]()
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
[📊 Benchmark Results](#-empirical-benchmarks) •
[✨ Pygame GUI](#-graphical-interface) •
[👥 Team Distribution](#-team-work-distribution)

---

</div>

## 🌌 The Mission

In a discrete $6 \times 7$ grid with $\approx 4.53 \times 10^{12}$ reachable positions and over $10^{21}$ possible game tree paths, Connect Four provides an ideal proving ground for AI reasoning. Exhaustive brute-force search is computationally intractable in real time, exposing a fundamental question in Artificial Intelligence:

> **When under strict thinking-time and compute constraints, does depth-bounded heuristic pruning (Alpha-Beta) outperform statistical simulation-based approximation (MCTS with UCT)?**

This project investigates, implements, and benchmarks both paradigms head-to-head under identical memory, move-latency, and CPU budgets.

---

## 👥 Team Work Distribution (3-Week Sprint)

> **Course:** ECSCT24301 – Foundation of AI (Track A: Applied AI System Development)  
> **Team of 2:** Responsibilities partitioned across algorithmic core and systems evaluation.

| Role | Member | Responsibilities | Status |
| :--- | :--- | :--- | :---: |
| **Member 1** | *Algorithms & Core Logic* | Alpha-Beta pruning, 69-window heuristic evaluation, iterative deepening with time budgeting, theoretical formulation (`docs/ALGORITHMS.md`), empirical depth scaling and failure-mode analysis, Stage 3 report sections (2, 3, 4, 5, 8), slide outline. | ✅ **Week 1, 2 & 3 Complete** |
| **Member 2** | *Engineering, GUI & Evaluation* | Modular repository scaffolding, PEAS formulation, performance instrumentation (`tracemalloc`, `perf_counter`), CLI & Pygame GUI, MCTS with UCT, automated tournament benchmark harness, Stage 3 report sections (1, 6, 7), viva guide. | ✅ **Week 1, 2 & 3 Complete** |

### 📋 Week 3 Milestone Status (Member 1 Deliverables)
- [x] **Scaling Experiments (`experiments_cli.py`)**: Depth-scaling complexity benchmarks for Minimax and Alpha-Beta up to depth 9 across empty and mid-game positions.
- [x] **Empirical Metrics & Plotting**: Persisted experimental data in `docs/results/` (`depth_scaling.csv`, `iterative_scaling.csv`, `mcts_budget_scaling.csv`, `ordering_comparison.csv`) and generated publication charts (`fig5_depth_scaling.png`, `fig6_mcts_strength.png`).
- [x] **Error & Failure-Mode Analysis**: Evaluated tactical horizon effects, one-move tactical guards, and MCTS simulation budget curves (50, 200, 500, 1000 rollouts).
- [x] **Academic Report Sections**: Authored Sections 2, 3, 4, 5, and 8 in `docs/STAGE3_REPORT_SECTIONS_2_3_4_5_8.md`.
- [x] **Viva Defense Slide Outline**: Comprehensive slide breakdown and speaker notes in `docs/SLIDES_MEMBER1.md`.

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
Exhaustive depth-bounded adversarial search evaluating all branches. Demonstrates the raw combinatorial state-space explosion before pruning optimizations.

### 3. Minimax with Alpha-Beta Pruning
Implements branch cutoff whenever $\alpha \ge \beta$ with center-out column ordering ($\text{col } 3 \to 2, 4 \to 1, 5 \to 0, 6$). Delivers up to **$9.9\times$ node reduction** over plain minimax.

### 4. 69-Window Heuristic Evaluator
Calculates utility across all **69 winning lines** on a $6 \times 7$ board:
- **24 horizontal** 4-tuples
- **21 vertical** 4-tuples
- **24 diagonal** 4-tuples (12 positive slope, 12 negative slope)

Weights open-3 threats, open-2 sequences, and center control dynamically.

### 5. Iterative Deepening with Time Budget
Searches depths $d = 1, 2, 3, \dots$ progressively. Employs per-node deadline checks with graceful rollback to the deepest fully completed iteration, guaranteeing move delivery within wall-clock constraints.

### 6. Monte Carlo Tree Search (MCTS) with UCT
Employs four-stage exploration:
1. **Selection**: Traverses tree using Upper Confidence Bound:
   $$\text{UCT}(i) = \frac{w_i}{n_i} + C_p \sqrt{\frac{2 \ln N}{n_i}} \quad (C_p = \sqrt{2} \approx 1.414)$$
2. **Expansion**: Adds new state node from legal action space.
3. **Simulation (Rollout)**: Fast simulation to terminal state.
4. **Backpropagation**: Rewards propagated to parent lineage.
*Features dual-mode budgeting (fixed simulation count or sub-second wall-clock limit) and 1-ply tactical guards.*

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
> *Runs all 53 unit and integration tests across board mechanics, heuristics, search parity, MCTS, and GUI logic in ~25-30 seconds.*

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

### 🏆 5. Automated Tournament Benchmark Runner

Auto-run an $N$-game tournament between any two agents with alternating starting turns to eliminate first-player bias:

```bash
python benchmark_cli.py --agent1 alphabeta --agent2 mcts --games 10 --depth1 4 --simulations2 300 --verbose
```

---

### 📈 6. Scaling & Failure-Mode Experimentation Runner (`experiments_cli.py`)

Run dedicated empirical complexity experiments, iterative deepening tests, tactical block benchmarks, and MCTS budget sweeps:

```bash
# 1. Depth-scaling complexity benchmark (Minimax & Alpha-Beta to depth 9) with plot
python experiments_cli.py --experiment depth --plot

# 2. Iterative deepening deadline test across multiple time allocations
python experiments_cli.py --experiment iterative

# 3. Tactical block test verifying immediate threat response
python experiments_cli.py --experiment block

# 4. MCTS simulation budget sweep against Alpha-Beta (10 games per budget) with plot
python experiments_cli.py --experiment mcts --games 10 --budgets 50 200 500 1000 --plot
```

---

## 📊 Empirical Benchmarks

### Head-to-Head Tournament: Alpha-Beta vs. MCTS (4-Game Series)

```
=================================================================
            BENCHMARK MATCH EVALUATION REPORT
=================================================================
 Total Games Played: 4 (Alternating starting turns)
-----------------------------------------------------------------
Metric                    | Alpha-Beta (d=3)   | MCTS (150 sims) 
-----------------------------------------------------------------
Wins (Win Rate)           | 2 (50.0%)          | 2 (50.0%)
Draws (Draw Rate)         | 0 (0.0%)
Total Moves Played        | 54                 | 54              
Avg Decision Time         | 15.34 ms           | 276.85 ms
Avg Expansions / Move     | 60.4 nodes         | 125.2 rollouts
Peak Memory Allocated     | 1,464.7 KB         | 1,573.6 KB
=================================================================
```

### Search Pruning Efficiency (Minimax vs. Alpha-Beta at Depth 4)

| Metric | Plain Minimax | Alpha-Beta (Center Order) | Optimization Gain |
| :--- | :---: | :---: | :---: |
| **Nodes Expanded** | 17,134 | 1,726 | **9.9× fewer nodes** |
| **Total Thinking Time** | 1,907.86 ms | 245.33 ms | **7.8× faster** |
| **Avg Time / Move** | 90.85 ms | 11.68 ms | **Sub-12ms response** |

---

## 📁 Repository Anatomy

```
connect-four/
├── connect4/                   # Core application package
│   ├── core/
│   │   └── board.py            # 6x7 Board, gravity, undo, bitwise & coordinate win-checks
│   ├── agents/                 # Adversarial & simulation intelligence
│   │   ├── base.py             # Polymorphic Agent interface & statistics
│   │   ├── random_agent.py     # Uniform random baseline
│   │   ├── minimax_agent.py    # Exhaustive depth-limited Minimax (state-space baseline)
│   │   ├── alphabeta_agent.py  # Minimax with Alpha-Beta pruning & heuristic toggle
│   │   ├── heuristic.py        # Precomputed 69-window evaluation matrix
│   │   ├── iterative_agent.py  # Iterative deepening Alpha-Beta with time budget
│   │   └── mcts_agent.py       # Monte Carlo Tree Search with UCT & dual budgeting
│   ├── benchmark/              # Telemetry & Tournament Evaluation
│   │   ├── instrumentation.py  # Sub-ms perf_counter & tracemalloc memory profiler
│   │   └── runner.py           # Multi-game tournament runner with alternating turns
│   ├── cli/
│   │   └── game_loop.py        # Terminal loop with live telemetry & board formatting
│   └── gui/
│       └── pygame_app.py       # 700x700px graphical Pygame board with hover & drops
├── docs/                       # Academic & Engineering documentation
│   ├── CODING_CONVENTIONS.md   # PEP 8, type hints & collaboration standards
│   ├── PEAS_AND_PROBLEM_STATEMENT.md # Academic PEAS & formal state-space draft
│   ├── ALGORITHMS.md           # Mathematical formulations, heuristic windows & proofs
│   ├── STAGE3_REPORT_SECTIONS_1_6_7.md # Academic report sections (Member 2)
│   ├── STAGE3_REPORT_SECTIONS_2_3_4_5_8.md # Academic report sections (Member 1)
│   ├── SLIDES_MEMBER1.md       # Presentation slide outline (Member 1)
│   ├── VIVA_TALKING_POINTS_PERSON_B.md # Viva preparation guide (Member 2)
│   ├── results/                # CSV experimental outputs (depth scaling, MCTS, ordering)
│   └── figures/                # Publication-quality benchmark visualization charts
├── tests/                      # Automated Test Suite (53 Tests, 100% Pass)
│   ├── test_board.py           # Board mechanics, gravity, edge cases (9 tests)
│   ├── test_agents.py          # Random & Minimax baseline tests (4 tests)
│   ├── test_alphabeta.py       # Alpha-Beta parity & pruning verification (4 tests)
│   ├── test_heuristic.py       # 69-window score symmetry & threat checks (9 tests)
│   ├── test_iterative.py       # Iterative deepening time cutoffs & fallbacks (4 tests)
│   ├── test_mcts.py            # UCT selection, rollouts, deterministic seeding (6 tests)
│   ├── test_benchmark_runner.py# Tournament runner & turn alternation (2 tests)
│   ├── test_gui.py             # Headless GUI event loop & coordinate mapping (2 tests)
│   ├── test_instrumentation.py # Timer & tracemalloc profiler checks (3 tests)
│   └── test_game_loop.py       # End-to-end simulated match test (1 test)
├── main.py                     # Primary CLI executable runner
├── gui_main.py                 # Pygame graphical application launcher
├── benchmark_cli.py            # Tournament evaluation runner
├── experiments_cli.py          # Scaling & failure-mode experimentation harness
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
  [ Week 3: Tournament, Scaling & Scientific Report ] ──► COMPLETE (53/53 tests)
  • Large-scale Tournament Benchmarks • Scaling & Error Analysis • Final Report & Slides
```

---

<div align="center">
  <sub>Developed for ECSCT24301 Foundation of AI • Adani University (FEST)</sub><br>
  <sub>Built with ❤️ using Python, NumPy & Pygame</sub>
</div>