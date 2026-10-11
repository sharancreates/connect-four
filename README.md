# Connect Four AI: Adversarial Search vs. Monte Carlo Tree Search

[![Tests](https://img.shields.io/badge/tests-34%20passed-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)]()
[![Course](https://img.shields.io/badge/Course-ECSCT24301%20Foundation%20of%20AI-orange.svg)]()
[![Institution](https://img.shields.io/badge/Institution-Adani%20University-red.svg)]()

> **Applied AI System Development Track (Track A)** — Game Playing & Adversarial Search  
> **Course:** ECSCT24301 – Foundation of AI, Academic Year 2026–27  
> **Faculty of Engineering Sciences and Technology (FEST), Adani University**

---

## 📌 Project Overview

This project designs, implements, and benchmarks autonomous decision-making agents for **Connect Four** (standard 6×7 grid). We evaluate the empirical trade-offs between:
1. **Deterministic Depth-Limited Search**: Minimax with Alpha-Beta pruning, iterative deepening, and heuristic board evaluation.
2. **Statistical Simulation Search**: Monte Carlo Tree Search (MCTS) utilizing the Upper Confidence Bound applied to Trees (UCT) selection policy.
3. **Baselines**: Uniform Random agent and Plain Minimax (no pruning) measuring raw state-space explosion.

---

## 👥 Team Work Distribution (3-Week Sprint)

| Role | Member | Responsibilities |
| :--- | :--- | :--- |
| **Member 1** | *Algorithms & Core Logic* | Minimax with Alpha-Beta pruning, depth-limited heuristic functions, iterative deepening, state-space write-up, and error analysis. |
| **Member 2** | *Engineering, GUI & Evaluation* | Repository architecture, coding conventions, CLI game loop, node/time/memory instrumentation wrapper, MCTS implementation, Pygame GUI demo, comparative benchmark harness, and PEAS / problem statement write-up. |

---

## 🚀 Week 1 Milestone Status (Member 2 Deliverables)

- [x] **Repository Scaffolding & Conventions**: Structured modular Python package with [Coding Conventions](docs/CODING_CONVENTIONS.md).
- [x] **Academic Documentation**: Formal [PEAS Characterization & Problem Statement](docs/PEAS_AND_PROBLEM_STATEMENT.md).
- [x] **Performance Instrumentation**: Wrapper tracking wall-clock time (`time.perf_counter`), memory consumption (`tracemalloc`), and node expansions.
- [x] **Interactive & Automated CLI**: Full-featured command-line game loop supporting Human-vs-Agent and Agent-vs-Agent play.
- [x] **Playable Baseline Agents**: Random baseline and Plain Minimax (depth-limited, no pruning) with empirical node-expansion logging.
- [x] **Automated Test Suite**: 17 unit and integration tests passing.

---

## ⚡ Week 2 Milestone Status (Member 1 Deliverables)

- [x] **Alpha-Beta Pruning**: Depth-limited adversarial search with alpha-beta cutoff and center-out move ordering ([connect4/agents/alphabeta_agent.py](connect4/agents/alphabeta_agent.py)).
- [x] **Heuristic Evaluation Function**: 69 sliding 4-window evaluation weighting 2-discs, 3-discs, and center control ([connect4/agents/heuristic.py](connect4/agents/heuristic.py)).
- [x] **Iterative Deepening with Time Budget**: Time-bounded search with per-node deadline checks and depth tracking ([connect4/agents/iterative_agent.py](connect4/agents/iterative_agent.py)).
- [x] **Heuristic Unit Tests**: Comprehensive test suite covering heuristic windows, sign symmetries, pruning parity, and time limits (34/34 tests passing).
- [x] **Algorithm Analysis & Viva Prep**: Theoretical and empirical evaluation documented in [docs/ALGORITHMS.md](docs/ALGORITHMS.md).

---

## 📁 Repository Structure

```
connect-four/
├── connect4/
│   ├── core/
│   │   └── board.py            # 6x7 grid, gravity drop, win/draw detection, undo
│   ├── agents/
│   │   ├── base.py             # Abstract base agent class
│   │   ├── random_agent.py     # Uniform random baseline
│   │   ├── minimax_agent.py    # Plain Minimax (measures state-space explosion)
│   │   ├── alphabeta_agent.py  # Minimax with Alpha-Beta pruning & heuristic switch
│   │   ├── heuristic.py        # 69-window evaluation function for non-terminal states
│   │   └── iterative_agent.py  # Iterative deepening Alpha-Beta with time budget
│   ├── benchmark/
│   │   └── instrumentation.py  # Wall-clock time, tracemalloc, node counter wrapper
│   └── cli/
│       └── game_loop.py        # Interactive CLI game loop with telemetry
├── docs/
│   ├── CODING_CONVENTIONS.md   # PEP 8, typing, git commit guidelines
│   ├── PEAS_AND_PROBLEM_STATEMENT.md # Academic PEAS & state-space formulation
│   └── ALGORITHMS.md           # Algorithm theory, heuristic design & benchmark results
├── tests/
│   ├── test_board.py           # Board rules & win-condition unit tests
│   ├── test_agents.py          # Random & Minimax behavior verification
│   ├── test_alphabeta.py       # Alpha-Beta move parity & pruning tests
│   ├── test_heuristic.py       # Heuristic sliding window evaluation tests
│   ├── test_iterative.py       # Iterative deepening & time limit tests
│   ├── test_instrumentation.py # Timer, memory profiler & node counter tests
│   └── test_game_loop.py       # Full automated game simulation tests
├── .gsd/                       # Get Shit Done (GSD) spec, roadmap, and state
├── main.py                     # Primary executable entrypoint
└── requirements.txt            # Project dependencies
```

---

## 💻 Installation & Quickstart

### 1. Requirements
Ensure Python 3.10 or 3.11 is installed, then install requirements:
```bash
pip install -r requirements.txt
```

### 2. Run the Test Suite
```bash
python -m pytest tests/ -v
```

### 3. Play Human vs. AI (Minimax)
```bash
python main.py --mode human-vs-agent --agent2 minimax --depth2 4
```

### 4. Run Agent vs. Agent (Random vs. Plain Minimax)
```bash
python main.py --mode agent-vs-agent --agent1 random --agent2 minimax --depth2 3 --delay 0.3
```

### 5. Run Alpha-Beta with Heuristic Evaluation
```bash
python main.py --mode agent-vs-agent --agent1 alphabeta --agent2 alphabeta --depth1 4 --depth2 4 --heuristic2
```

### 6. Run Iterative Deepening with Time Budget
```bash
python main.py --mode agent-vs-agent --agent1 alphabeta --agent2 iterative --depth1 4 --depth2 10 --time2 1.0
```

---

## 📊 Week 1 Baseline Telemetry (Empirical Output)

Sample telemetry captured during a Random vs. Plain Minimax match:

```
 AGENT TELEMETRY:
 [Player 1 (X)] Agent 1 (Random):
   * Total Moves:     4
   * Total Time:      0.10 ms
   * Avg Time / Move: 0.02 ms
   * Total Nodes:     4
   * Avg Nodes / Move: 1.0
   * Peak Memory:     20.54 KB
 [Player 2 (O)] Agent 2 (Minimax):
   * Total Moves:     4
   * Total Time:      111.06 ms
   * Avg Time / Move: 27.77 ms
   * Total Nodes:     1,540
   * Avg Nodes / Move: 385.0
   * Peak Memory:     23.22 KB
```

---

## 📅 Roadmap & Next Phases

- **Week 2**: Alpha-Beta pruning, iterative deepening, heuristic evaluation function (Member 1) + Monte Carlo Tree Search (UCT) and Pygame GUI skeleton (Member 2).
- **Week 3**: Comparative benchmarking suite (execution time vs. depth, nodes expanded vs. simulations), plots, GUI integration, and final report compilation.