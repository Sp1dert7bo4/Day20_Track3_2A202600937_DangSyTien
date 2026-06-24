"""Optional critic agent skeleton for bonus work."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentResult

class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings."""
        try:
            if not state.final_answer:
                return state
                
            system_prompt = (
                "You are a critic. Review the final answer for hallucinations, "
                "citation coverage, and overall quality. Output your critique."
            )
            user_prompt = f"Query: {state.request.query}\nAnswer to evaluate:\n{state.final_answer}"
            
            response = self.llm_client.complete(system_prompt, user_prompt)
            state.agent_results.append(AgentResult(agent=self.name, content=f"Critique: {response.content}"))
            state.add_trace_event(self.name, {"critique_length": len(response.content)})
        except Exception as e:
            state.errors.append(f"Critic Error: {e}")
            
        return state
