import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from dotenv import load_dotenv
load_dotenv()

from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow

def run_demo():
    query = """You are helping a PhD student prepare a research briefing on the topic:

"Do multi-agent LLM systems actually outperform single-agent systems on complex tasks?"

Your task is not just to summarize the topic. You must produce a structured research briefing that:
1. Defines the main claim precisely
2. Breaks the literature into major positions or schools of thought
3. Identifies arguments supporting the claim
4. Identifies arguments challenging the claim
5. Explains where empirical evidence is weak, incomplete, or confounded
6. Distinguishes between true multi-agent gains and gains caused by other factors such as more tokens, more prompt engineering, or repeated self-reflection
7. Proposes 3 concrete experiments that could better resolve the debate
8. Ends with a balanced final judgment

Constraints:
- Do not write a generic overview
- Explicitly discuss what kinds of evidence would count as convincing
- The final judgment must include uncertainty and unresolved issues
- Organize the answer so it could be used as speaking notes for a research group meeting

Output format:
- Core question
- Main positions
- Evidence for
- Evidence against
- Methodological concerns
- Proposed experiments
- Final judgment"""

    print("Running Multi-Agent Workflow on Demo Prompt 2...")
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    workflow = MultiAgentWorkflow()
    
    result = workflow.run(state)
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/demo_result.md", "w", encoding="utf-8") as f:
        f.write("# Demo: Research Briefing on Multi-Agent LLMs\n\n")
        f.write("## 1. Prompt\n")
        f.write("```text\n" + query + "\n```\n\n")
        f.write("## 2. Lộ trình thực thi (Route History)\n")
        f.write(str(result.route_history) + "\n\n")
        f.write("## 3. Nguồn tài liệu (Sources)\n")
        for s in result.sources:
            f.write(f"- [{s.title}]({s.url})\n")
        f.write("\n## 4. Final Answer\n\n")
        f.write(str(result.final_answer) + "\n\n")
        f.write("## 5. Trace Events\n")
        for event in result.trace:
            f.write(f"- {event['name']}: {event['payload']}\n")
        f.write("\n## 6. Errors\n")
        for err in result.errors:
            f.write(f"- {err}\n")
            
    print("Demo complete! Result saved to reports/demo_result.md")

if __name__ == "__main__":
    try:
        run_demo()
    except Exception as e:
        import traceback
        print(f"Failed with exception: {e}")
        traceback.print_exc()
