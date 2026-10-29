"""Unit tests for the benchmark plotting module."""

import os
import pytest
from connect4.benchmark.plotter import (
    plot_execution_time_vs_depth,
    plot_nodes_expanded_log_scale,
    plot_winrate_matrix_heatmap,
    plot_mcts_vs_alphabeta,
    plot_mcts_strength,
    generate_all_figures,
)


@pytest.fixture
def mock_results_dir(tmp_path):
    """Create a temporary directory with valid mock CSV files for tests."""
    results_dir = tmp_path / "mock_results"
    results_dir.mkdir()

    # depth_scaling.csv
    depth_file = results_dir / "depth_scaling.csv"
    depth_content = (
        "position,agent,depth,nodes,time_ms\n"
        "empty,minimax,1,7,0.5\n"
        "empty,minimax,2,56,1.2\n"
        "empty,minimax,5,19607,500.0\n"
        "empty,alphabeta,1,7,0.5\n"
        "empty,alphabeta,2,20,1.0\n"
        "empty,alphabeta,6,1248,45.0\n"
        "empty,alphabeta+heuristic,1,7,0.6\n"
        "empty,alphabeta+heuristic,2,20,1.1\n"
        "empty,alphabeta+heuristic,6,1282,90.0\n"
        "mid-game,minimax,1,7,0.4\n"
        "mid-game,minimax,2,56,1.0\n"
        "mid-game,minimax,5,18544,550.0\n"
        "mid-game,alphabeta,1,7,0.4\n"
        "mid-game,alphabeta,2,20,0.9\n"
        "mid-game,alphabeta,6,2967,100.0\n"
        "mid-game,alphabeta+heuristic,1,7,0.5\n"
        "mid-game,alphabeta+heuristic,2,28,1.2\n"
        "mid-game,alphabeta+heuristic,6,4747,180.0\n"
    )
    depth_file.write_text(depth_content, encoding="utf-8")

    # tournament.csv
    tourney_file = results_dir / "tournament.csv"
    tourney_content = (
        "agents,first_mover,winner,plies\n"
        "Random vs Minimax (d=3),Random,Minimax (d=3),8\n"
        "Random vs Minimax (d=3),Minimax (d=3),Minimax (d=3),7\n"
        "Random vs AlphaBeta (d=4),Random,AlphaBeta (d=4),12\n"
        "AlphaBeta (d=4) vs AlphaBeta (d=6),AlphaBeta (d=4),Draw,42\n"
        "AlphaBeta (d=4) vs MCTS (N=500),AlphaBeta (d=4),MCTS (N=500),28\n"
    )
    tourney_file.write_text(tourney_content, encoding="utf-8")

    # mcts_vs_alphabeta.csv
    mcts_file = results_dir / "mcts_vs_alphabeta.csv"
    mcts_content = (
        "simulations,games,mcts_wins,draws,mcts_losses,avg_plies_when_lost\n"
        "50,10,0,0,10,17.9\n"
        "200,10,0,0,10,30.9\n"
        "500,10,3,0,7,29.9\n"
        "1000,10,3,0,7,30.9\n"
    )
    mcts_file.write_text(mcts_content, encoding="utf-8")

    return results_dir


def test_missing_csv_raises_file_not_found(tmp_path):
    """Verify that all plotting functions raise FileNotFoundError when CSV is absent."""
    nonexistent = str(tmp_path / "nonexistent.csv")
    dummy_out = str(tmp_path / "dummy.png")

    with pytest.raises(FileNotFoundError):
        plot_execution_time_vs_depth(csv_path=nonexistent, output_path=dummy_out)

    with pytest.raises(FileNotFoundError):
        plot_nodes_expanded_log_scale(csv_path=nonexistent, output_path=dummy_out)

    with pytest.raises(FileNotFoundError):
        plot_winrate_matrix_heatmap(csv_path=nonexistent, output_path=dummy_out)

    with pytest.raises(FileNotFoundError):
        plot_mcts_vs_alphabeta(csv_path=nonexistent, output_path=dummy_out)


def test_plot_execution_time_vs_depth(mock_results_dir, tmp_path):
    """Verify latency vs depth figure creation and non-zero size."""
    csv_file = str(mock_results_dir / "depth_scaling.csv")
    out_file = str(tmp_path / "test_fig1.png")
    result = plot_execution_time_vs_depth(csv_path=csv_file, output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000


def test_plot_nodes_expanded_log_scale(mock_results_dir, tmp_path):
    """Verify log-scale node expansion figure creation."""
    csv_file = str(mock_results_dir / "depth_scaling.csv")
    out_file = str(tmp_path / "test_fig2.png")
    result = plot_nodes_expanded_log_scale(csv_path=csv_file, output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000


def test_plot_winrate_matrix_heatmap(mock_results_dir, tmp_path):
    """Verify tournament win-rate matrix heatmap creation."""
    csv_file = str(mock_results_dir / "tournament.csv")
    out_file = str(tmp_path / "test_fig3.png")
    result = plot_winrate_matrix_heatmap(csv_path=csv_file, output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000


def test_plot_mcts_vs_alphabeta(mock_results_dir, tmp_path):
    """Verify MCTS budget scaling figure creation."""
    csv_file = str(mock_results_dir / "mcts_vs_alphabeta.csv")
    out_file = str(tmp_path / "test_fig6.png")
    result = plot_mcts_vs_alphabeta(csv_path=csv_file, output_path=out_file)
    assert os.path.exists(result)
    assert os.path.getsize(result) > 10_000

    # Also check alias
    out_file_alias = str(tmp_path / "test_fig6_alias.png")
    res_alias = plot_mcts_strength(csv_path=csv_file, output_path=out_file_alias)
    assert os.path.exists(res_alias)
    assert os.path.getsize(res_alias) > 10_000


def test_generate_all_figures(mock_results_dir, tmp_path):
    """Verify bulk orchestrator produces all figures."""
    target_dir = str(tmp_path / "figures")
    files = generate_all_figures(output_dir=target_dir, results_dir=str(mock_results_dir))
    assert len(files) == 4
    for f in files:
        assert os.path.exists(f)
        assert os.path.getsize(f) > 10_000
