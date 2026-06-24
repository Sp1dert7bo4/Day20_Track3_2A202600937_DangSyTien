import os
import sys

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from dotenv import load_dotenv
load_dotenv()

from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_markdown_report

def baseline_runner(query: str) -> ResearchState:
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    llm = LLMClient()
    system_prompt = "You are a helpful research assistant. Find information and answer the user's query comprehensively."
    try:
        response = llm.complete(system_prompt, query)
        state.final_answer = response.content
    except Exception as e:
        state.final_answer = f"Error: {e}"
    return state

def multi_agent_runner(query: str) -> ResearchState:
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    workflow = MultiAgentWorkflow()
    return workflow.run(state)

if __name__ == "__main__":
    query = "Research GraphRAG state-of-the-art and write a 500-word summary"
    print(f"Running benchmark for query: {query}")
    
    # 1. Baseline
    print("Running baseline...")
    baseline_state, baseline_metrics = run_benchmark("baseline", query, baseline_runner)
    
    # 2. Multi-Agent
    print("Running multi-agent...")
    ma_state, ma_metrics = run_benchmark("multi-agent", query, multi_agent_runner)
    
    # 3. Report
    report_content = render_markdown_report([baseline_metrics, ma_metrics])
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/benchmark_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print("Benchmark complete. Report saved to reports/benchmark_report.md")
