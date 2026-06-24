"""LangGraph workflow skeleton."""

from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


from langgraph.graph import StateGraph, END
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.writer import WriterAgent
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient

class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph."""

    def __init__(self):
        self.llm_client = LLMClient()
        self.search_client = SearchClient()
        self.supervisor = SupervisorAgent(self.llm_client)
        self.researcher = ResearcherAgent(self.llm_client, self.search_client)
        self.analyst = AnalystAgent(self.llm_client)
        self.writer = WriterAgent(self.llm_client)
        self.graph = self.build()

    def build(self) -> object:
        """Create a LangGraph graph."""
        workflow = StateGraph(ResearchState)
        
        workflow.add_node("supervisor", self.supervisor.run)
        workflow.add_node("researcher", self.researcher.run)
        workflow.add_node("analyst", self.analyst.run)
        workflow.add_node("writer", self.writer.run)
        
        workflow.set_entry_point("supervisor")
        
        def route(state: ResearchState):
            if not state.route_history:
                return "done"
            return state.route_history[-1]

        workflow.add_conditional_edges(
            "supervisor",
            route,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "done": END
            }
        )
        
        workflow.add_edge("researcher", "supervisor")
        workflow.add_edge("analyst", "supervisor")
        workflow.add_edge("writer", "supervisor")
        
        return workflow.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        result = self.graph.invoke(state)
        # LangGraph typically returns a dict
        if isinstance(result, dict):
            return ResearchState(**result)
        return result
