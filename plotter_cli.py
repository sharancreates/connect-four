"""CLI Entrypoint for Benchmark Visualizations.

Generates the 4 publication-quality benchmark figures comparing Minimax,
Alpha-Beta pruning, Iterative Deepening, and Monte Carlo Tree Search.
"""

from __future__ import annotations
import argparse
import os
import sys
from connect4.benchmark.plotter import generate_all_figures


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Connect Four AI Benchmark Plotter (Adani University)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--output-dir",
        default="docs/figures",
        help="Target directory to save generated PNG figures",
    )

    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f" Connect Four AI — Benchmark Figures Generation")
    print(f" Target Output: {os.path.abspath(args.output_dir)}")
    print(f"=======================================================\n")

    files = generate_all_figures(output_dir=args.output_dir)

    for i, f in enumerate(files, 1):
        size_kb = os.path.getsize(f) / 1024
        print(f"  [Fig {i}] Saved: {os.path.basename(f)} ({size_kb:.1f} KB)")

    print(f"\nSuccessfully generated {len(files)} publication figures at 300 DPI.\n")


if __name__ == "__main__":
    main()
