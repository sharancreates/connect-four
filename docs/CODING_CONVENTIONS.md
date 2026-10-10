# Connect Four AI — Coding Conventions & Engineering Guidelines

> **Project:** Intelligent Game-Playing Agent for Connect Four  
> **Course:** ECSCT24301 – Foundation of AI, Adani University  
> **Authors:** Team of 2 (Member 1: Algorithms & Search | Member 2: Engineering & Evaluation)

---

## 1. Project Architecture & Directory Layout

```
connect-four/
├── connect4/                   # Main Python application package
│   ├── __init__.py
│   ├── core/                   # Game engine & representation
│   │   ├── __init__.py
│   │   └── board.py            # 6x7 Board class, rules, move validation, win checks
│   ├── agents/                 # Adversarial & simulation agents
│   │   ├── __init__.py
│   │   ├── base.py             # Abstract base agent class & statistics interface
│   │   ├── random_agent.py     # Uniform random baseline
│   │   ├── minimax_agent.py    # Plain Minimax agent (no pruning, raw node count)
│   │   ├── alphabeta_agent.py  # (Week 2) Alpha-Beta pruning + heuristic
│   │   └── mcts_agent.py       # (Week 2) Monte Carlo Tree Search
│   ├── benchmark/              # Instrumentation and evaluation suite
│   │   ├── __init__.py
│   │   └── instrumentation.py  # Time, memory (tracemalloc), and node counter wrapper
│   └── cli/                    # User interface & gameplay loops
│       ├── __init__.py
│       └── game_loop.py        # Terminal game runner (Human-vs-Agent, Agent-vs-Agent)
├── docs/                       # Project documentation & academic drafts
│   ├── CODING_CONVENTIONS.md
│   └── PEAS_AND_PROBLEM_STATEMENT.md
├── tests/                      # Automated test suite (pytest / unittest)
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_agents.py
│   ├── test_instrumentation.py
│   └── test_game_loop.py
├── main.py                     # Primary executable entrypoint
├── requirements.txt            # Dependency definitions
└── README.md                   # Repository overview & instructions
```

---

## 2. Python Coding Standards

1. **Python Version**: Python 3.10+ / 3.11.
2. **PEP 8 Compliance**:
   - Follow standard PEP 8 naming:
     - `snake_case` for functions, methods, modules, and variable names.
     - `PascalCase` for classes (e.g., `Board`, `MinimaxAgent`, `MetricsTracker`).
     - `UPPER_CASE_SNAKE` for module-level constants (e.g., `ROWS = 6`, `COLS = 7`).
   - Indentation: 4 spaces (no tabs).
   - Maximum line length: 100 characters.
3. **Type Annotations**:
   - All public function signatures and class methods MUST include standard type hints (`typing.List`, `typing.Tuple`, `typing.Optional`, or built-in generics in 3.10+).
   - Example:
     ```python
     def get_legal_moves(self) -> list[int]:
         ...
     ```
4. **Documentation**:
   - Google-style or standard Sphinx docstrings for all classes and non-trivial methods.
   - Explain inputs, outputs, exceptions, and algorithmic details.

---

## 3. Git & Collaboration Protocols

1. **Branching Strategy**:
   - `main`: Production-ready, verified code.
   - Feature branches: `feat/member1-algorithm-name` or `feat/member2-feature-name`.
2. **Commit Message Format**:
   - Use Conventional Commits: `<type>(<scope>): <short description>`
   - Types:
     - `feat`: New feature or agent
     - `fix`: Bug fix
     - `test`: Unit or integration tests
     - `docs`: Documentation, proposals, write-ups
     - `refactor`: Code change that neither fixes a bug nor adds a feature
     - `chore`: Project setup, configuration, formatting
3. **Peer Review**:
   - Per course requirements, both team members review all code merged into `main`. Both members must be prepared to defend all algorithms and architectures during viva evaluation.

---

## 4. Testing & Verification Standards

1. **Test Coverage**:
   - Every component must have automated tests.
   - Core board transitions and win-checks must be 100% verified against edge cases (horizontal, vertical, positive diagonal, negative diagonal, full board draw).
2. **Empirical Evidence**:
   - No feature is declared complete without automated test runner output and empirical performance figures.
