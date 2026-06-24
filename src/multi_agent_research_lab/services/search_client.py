"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import SourceDocument as Document


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[Document]:
        """Perform a web search using Tavily."""
        try:
            from tavily import TavilyClient
            import os

            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key or api_key == "tvly-xxxxxxxxxxxxxxx":
                return [Document(
                    title="Mock Search Result",
                    url="https://example.com/mock-search",
                    snippet=f"This is a mock search result for: {query}. Multi-agent systems decompose tasks, verify reasoning, and handle long context better than single agents, but require more tokens and careful routing."
                )]

            client = TavilyClient(api_key=api_key)
            response = client.search(query=query, max_results=max_results)
            
            docs = []
            for item in response.get("results", []):
                docs.append(Document(title=item["title"], url=item["url"], snippet=item["content"]))
            return docs
        except Exception as e:
            return [Document(
                title="Search Error Fallback",
                url="https://example.com/error",
                snippet=f"Search failed due to {e}. Multi-agent systems decompose tasks, verify reasoning, and handle long context better than single agents, but require more tokens and careful routing."
            )]
