"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentResult

class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route."""
        
        if state.iteration >= 10:
            state.record_route("done")
            state.add_trace_event(self.name, {"decision": "done", "reason": "max iterations reached"})
            return state

        system_prompt = (
            "You are a supervisor managing a research task.\n"
            "Workers:\n"
            "- researcher: finds information and sources online.\n"
            "- analyst: analyzes findings and extracts key claims.\n"
            "- writer: writes the final answer based on the analysis.\n"
            "Rules:\n"
            "1. If no sources or research notes exist, call 'researcher'.\n"
            "2. If research notes exist but no analysis notes, call 'analyst'.\n"
            "3. If analysis notes exist but no final answer, call 'writer'.\n"
            "4. If a final answer exists, call 'done'.\n"
            "Return ONLY the exact worker name or 'done'."
        )

        user_prompt = f"Query: {state.request.query}\n"
        user_prompt += f"Sources count: {len(state.sources)}\n"
        user_prompt += f"Has research notes: {bool(state.research_notes)}\n"
        user_prompt += f"Has analysis notes: {bool(state.analysis_notes)}\n"
        user_prompt += f"Has final answer: {bool(state.final_answer)}\n"
        user_prompt += "Next worker:"

        try:
            response = self.llm_client.complete(system_prompt, user_prompt)
            decision = response.content.strip().lower()
            
            valid_routes = ["researcher", "analyst", "writer", "done"]
            next_route = "researcher" 
            for route in valid_routes:
                if route in decision:
                    next_route = route
                    break
                    
            state.record_route(next_route)
            state.agent_results.append(AgentResult(agent=self.name, content=f"Routing to {next_route}"))
            state.add_trace_event(self.name, {"decision": next_route, "raw_response": decision})
            
        except Exception as e:
            state.errors.append(f"Supervisor error: {e}")
            state.record_route("done")
            
        return state
