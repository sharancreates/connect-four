"""Unit tests for the benchmark plotting module."""

import os
import pytest
from connect4.benchmark.plotter import (
    plot_execution_time_vs_depth,
    plot_nodes_expanded_log_scale,
    plot_winrate_matrix_heatmap,
    plot_memory_footprint,
    generate_all_figures,
)


def test_plot_execution_time_vs_depth(tmp_path):
    """Verify latency vs depth figure creation and non-zero size."""
    out_file = str(tmp_path / "test_fig1.png")
    result = plot_execution_time_vs_depth(output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000  # Non-trivial high-DPI image


def test_plot_nodes_expanded_log_scale(tmp_path):
    """Verify log-scale node expansion figure creation."""
    out_file = str(tmp_path / "test_fig2.png")
    result = plot_nodes_expanded_log_scale(output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000


def test_plot_winrate_matrix_heatmap(tmp_path):
    """Verify tournament win-rate matrix heatmap creation."""
    out_file = str(tmp_path / "test_fig3.png")
    result = plot_winrate_matrix_heatmap(output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000


def test_plot_memory_footprint(tmp_path):
    """Verify peak memory footprint bar chart creation."""
    out_file = str(tmp_path / "test_fig4.png")
    result = plot_memory_footprint(output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000


def test_generate_all_figures(tmp_path):
    """Verify bulk orchestrator produces all 4 figures."""
    target_dir = str(tmp_path / "figures")
    files = generate_all_figures(output_dir=target_dir)
    assert len(files) == 4
    for f in files:
        assert os.path.exists(f)
        assert os.path.getsize(f) > 10_000
