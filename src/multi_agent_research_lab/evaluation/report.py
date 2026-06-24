"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown."""
    
    analysis = "## Phân tích (Analysis)\n"
    analysis += "1. Hệ thống Multi-Agent thường cho thấy ưu điểm trong việc chia nhỏ tác vụ (research, analyze, write) giúp cải thiện chất lượng (Quality).\n"
    analysis += "2. Ngược lại, Single-Agent Baseline tuy nhanh hơn (Latency thấp) nhưng dễ bị thiếu sót thông tin do ngữ cảnh quá rộng hoặc thiếu công cụ (Tools).\n\n"

    lines = ["# Benchmark Report\n", analysis, "| Run | Latency (s) | Cost (USD) | Quality | Notes |", "|---|---:|---:|---:|---|"]
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"{item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {item.notes} |")
        
    failure_mode = "\n\n## Failure Mode và Cách Fix\n"
    failure_mode += "**Failure Mode**: Khi chạy multi-agent ban đầu, quá trình kết thúc ngay lập tức (1.12s) với Quality = 0 và không có route nào được gọi ngoài 'done'.\n"
    failure_mode += "**Nguyên nhân**: Code gọi LLM API (Groq) và Search API (Tavily) nằm trong khối `try...except`. Do thiếu thư viện `langchain-groq` và `tavily-python`, code bắt lỗi và đẩy thẳng state sang `done` thay vì break.\n"
    failure_mode += "**Cách Fix**: Cài đặt các thư viện phụ thuộc bằng lệnh `pip install langchain-groq tavily-python langchain-community` và chạy lại."
    
    lines.append(failure_mode)
    
    return "\n".join(lines) + "\n"
