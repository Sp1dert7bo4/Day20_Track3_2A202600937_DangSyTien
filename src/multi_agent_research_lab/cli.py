"""Command-line entrypoint for the lab starter."""

from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    from dotenv import load_dotenv
    load_dotenv()
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a real single-agent baseline."""

    _init()
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    
    from multi_agent_research_lab.services.llm_client import LLMClient
    import time
    
    llm = LLMClient()
    system_prompt = "You are a helpful research assistant. Find information and answer the user's query comprehensively."
    
    start_time = time.time()
    try:
        response = llm.complete(system_prompt, query)
        state.final_answer = response.content
        latency = time.time() - start_time
        console.print(f"[bold green]Baseline latency:[/bold green] {latency:.2f}s")
    except Exception as e:
        state.final_answer = f"Error: {e}"
        
    console.print(Panel.fit(str(state.final_answer), title="Single-Agent Baseline"))


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow skeleton."""

    _init()
    state = ResearchState(request=ResearchQuery(query=query))
    workflow = MultiAgentWorkflow()
    import time
    
    start_time = time.time()
    try:
        result = workflow.run(state)
        latency = time.time() - start_time
        console.print(f"[bold green]Multi-Agent latency:[/bold green] {latency:.2f}s")
        console.print(f"[bold blue]Route taken:[/bold blue] {result.route_history}")
    except StudentTodoError as exc:
        console.print(Panel.fit(str(exc), title="Expected TODO", style="yellow"))
        raise typer.Exit(code=2) from exc
    
    if result.final_answer:
        console.print(Panel.fit(str(result.final_answer), title="Multi-Agent Result"))
    else:
        console.print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
