"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass

from multi_agent_research_lab.core.errors import StudentTodoError


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client skeleton."""

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion."""
        import os
        from langchain_groq import ChatGroq
        from langchain_core.messages import SystemMessage, HumanMessage

        model_name = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        
        try:
            llm = ChatGroq(model=model_name, temperature=0.1)
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = llm.invoke(messages)
            
            usage = response.response_metadata.get("token_usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)
            
            return LLMResponse(
                content=str(response.content),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=0.0
            )
        except Exception as e:
            raise RuntimeError(f"LLM API Error: {e}")
