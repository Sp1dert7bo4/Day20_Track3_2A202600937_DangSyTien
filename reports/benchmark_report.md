# Benchmark Report

## Phân tích (Analysis)
1. Hệ thống Multi-Agent thường cho thấy ưu điểm trong việc chia nhỏ tác vụ (research, analyze, write) giúp cải thiện chất lượng (Quality).
2. Ngược lại, Single-Agent Baseline tuy nhanh hơn (Latency thấp) nhưng dễ bị thiếu sót thông tin do ngữ cảnh quá rộng hoặc thiếu công cụ (Tools).


| Run | Latency (s) | Cost (USD) | Quality | Notes |
|---|---:|---:|---:|---|
| baseline | 8.85 | 0.0000 | 8.5 | Found 0 sources |
| multi-agent | 16.39 | 0.0070 | 8.5 | Found 1 sources |


## Failure Mode và Cách Fix
**Failure Mode**: Khi chạy multi-agent ban đầu, quá trình kết thúc ngay lập tức (1.12s) với Quality = 0 và không có route nào được gọi ngoài 'done'.
**Nguyên nhân**: Code gọi LLM API (Groq) và Search API (Tavily) nằm trong khối `try...except`. Do thiếu thư viện `langchain-groq` và `tavily-python`, code bắt lỗi và đẩy thẳng state sang `done` thay vì break.
**Cách Fix**: Cài đặt các thư viện phụ thuộc bằng lệnh `pip install langchain-groq tavily-python langchain-community` và chạy lại.

## Trace Report
**LangSmith Public Trace**: [Multi-Agent Execution Trace](https://smith.langchain.com/public/10c3e90f-4f1e-4de2-9416-4fd489216d7c/r)
*(Bấm vào link trên để xem luồng chi tiết chuyển giao giữa các Agent: Supervisor ➔ Researcher ➔ Analyst ➔ Writer)*
