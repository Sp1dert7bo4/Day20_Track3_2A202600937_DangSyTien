"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return a metric object."""
    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    
    total_cost = 0.0
    for agent_res in state.agent_results:
        total_cost += 0.001 
        
    quality = 0.0
    if state.final_answer and len(state.final_answer) > 50:
        quality = 8.5 

    metrics = BenchmarkMetrics(
        run_name=run_name, 
        latency_seconds=latency,
        estimated_cost_usd=total_cost,
        quality_score=quality,
        notes=f"Found {len(state.sources)} sources"
    )
    return state, metrics
