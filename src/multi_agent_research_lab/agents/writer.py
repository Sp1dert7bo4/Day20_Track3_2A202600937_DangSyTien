"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentResult

class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""
        try:
            system_prompt = (
                f"You are a professional writer. Write a final response to the query for the audience: {state.request.audience}. "
                "Synthesize the research and analysis notes into a clear answer with citations to the original sources."
            )
            user_prompt = (
                f"Query: {state.request.query}\n"
                f"Research Notes:\n{state.research_notes}\n"
                f"Analysis Notes:\n{state.analysis_notes}\n"
            )
            
            response = self.llm_client.complete(system_prompt, user_prompt)
            state.final_answer = response.content
            
            state.agent_results.append(AgentResult(agent=self.name, content="Final answer written"))
            state.add_trace_event(self.name, {"answer_length": len(response.content)})
        except Exception as e:
            state.errors.append(f"Writer Error: {e}")
            
        return state
