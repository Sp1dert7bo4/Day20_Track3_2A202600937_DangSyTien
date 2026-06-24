"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentResult

class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""
        try:
            system_prompt = "You are an analyst. Extract key claims from the research notes, compare viewpoints, and flag any weak evidence."
            user_prompt = f"Query: {state.request.query}\nResearch Notes:\n{state.research_notes}"
            
            response = self.llm_client.complete(system_prompt, user_prompt)
            state.analysis_notes = response.content
            
            state.agent_results.append(AgentResult(agent=self.name, content="Analysis complete"))
            state.add_trace_event(self.name, {"analysis_length": len(response.content)})
        except Exception as e:
            state.errors.append(f"Analyst Error: {e}")
            
        return state
