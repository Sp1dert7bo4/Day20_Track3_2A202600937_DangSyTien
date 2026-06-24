"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient
from multi_agent_research_lab.core.schemas import AgentResult

class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"
    
    def __init__(self, llm_client: LLMClient, search_client: SearchClient):
        self.llm_client = llm_client
        self.search_client = search_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`."""
        try:
            search_query = state.request.query
            if len(search_query) > 350:
                search_query = search_query[:350] + "..."
                
            docs = self.search_client.search(query=search_query, max_results=state.request.max_sources)
            state.sources.extend(docs)
            
            system_prompt = "You are a researcher. Summarize the provided sources into concise research notes."
            user_prompt = f"Query: {state.request.query}\nSources:\n"
            for d in docs:
                user_prompt += f"- {d.title} ({d.url}): {d.snippet}\n"
                
            response = self.llm_client.complete(system_prompt, user_prompt)
            state.research_notes = response.content
            
            state.agent_results.append(AgentResult(agent=self.name, content="Gathered sources and notes"))
            state.add_trace_event(self.name, {"docs_found": len(docs), "notes_length": len(response.content)})
        except Exception as e:
            state.errors.append(f"Researcher Error: {e}")
            
        return state
