import openpyxl
import os
import re
import urllib.request
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(script_dir, "AI_Engineering_Roadmap.xlsx")
readme_path = os.path.join(script_dir, "README.md")
svg_path = os.path.join(script_dir, "progress.svg")

if not os.path.exists(excel_path):
    print("Excel file not found at:", excel_path)
    exit(1)

# Step 1: Fetch checked boxes from GitHub Issue #1 (1-tap mobile tracker)
checked_from_issue = set()
issue_url = "https://api.github.com/repos/Rakmo5/ai-engineering/issues/1"
github_token = os.environ.get("GITHUB_TOKEN")

try:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AIEngineeringTracker"
    }
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    req = urllib.request.Request(issue_url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        body = data.get('body', '')
        for line in body.splitlines():
            # Match lines like "- [x] [1. Modern Python Typing...]"
            m = re.search(r'-\s*\[[xX]\]\s*\[?(\d+)\.', line)
            if m:
                checked_from_issue.add(int(m.group(1)))
    if checked_from_issue:
        print(f"Fetched {len(checked_from_issue)} checked modules from GitHub Issue #1: {sorted(list(checked_from_issue))}")
except Exception as e:
    print("Note: Could not reach GitHub Issue API (running in offline mode):", e)

# Step 2: Sync checked boxes to Excel
if checked_from_issue:
    wb_sync = openpyxl.load_workbook(excel_path)
    sheet_sync = wb_sync["Master Roadmap"]
    updated_any = False
    for r in range(2, sheet_sync.max_row + 1):
        no_v = sheet_sync.cell(row=r, column=1).value
        try:
            if int(no_v) in checked_from_issue:
                if sheet_sync.cell(row=r, column=9).value != "Completed":
                    sheet_sync.cell(row=r, column=9, value="Completed")
                    updated_any = True
        except (TypeError, ValueError):
            continue
    if updated_any:
        wb_sync.save(excel_path)
        print("Updated Excel file with checked modules from GitHub Issue #1!")

# Step 3: Load Excel to generate updated README & progress.svg
wb = openpyxl.load_workbook(excel_path, data_only=True)
sheet = wb["Master Roadmap"]

modules = []
completed_count = 0

for r in range(2, sheet.max_row + 1):
    no_val = sheet.cell(row=r, column=1).value
    phase = sheet.cell(row=r, column=2).value
    category = sheet.cell(row=r, column=3).value
    name = sheet.cell(row=r, column=4).value
    skills = sheet.cell(row=r, column=5).value
    pri_video = sheet.cell(row=r, column=6).value
    sup_video = sheet.cell(row=r, column=7).value
    practice = sheet.cell(row=r, column=8).value
    status = sheet.cell(row=r, column=9).value
    
    if not name:
        continue
        
    try:
        no_val = int(no_val)
    except (TypeError, ValueError):
        continue
        
    is_completed = (status == "Completed" or status == "Solved")
    if is_completed:
        completed_count += 1
        
    modules.append({
        'no': no_val,
        'phase': phase,
        'category': category,
        'name': name,
        'skills': skills,
        'pri_video': pri_video,
        'sup_video': sup_video,
        'practice': practice,
        'status': "Completed" if is_completed else ("In Progress" if status == "In Progress" else "Not Started"),
        'completed': is_completed
    })

total_modules = len(modules)
pct = (completed_count / total_modules) * 100 if total_modules else 0
fill_width = 400 * (completed_count / total_modules) if total_modules else 0

# Count by phase
phase_order = [
    "Phase 0",
    "Phase 1",
    "Phase 2",
    "Phase 3",
    "Phase 4",
    "Phase 5",
    "Phase 6",
    "Phase 7",
    "Phase 8",
    "Phase 9",
    "Phase 10"
]

phase_stats = {}
for m in modules:
    p = m['phase']
    if p not in phase_stats:
        phase_stats[p] = {'total': 0, 'completed': 0}
    phase_stats[p]['total'] += 1
    if m['completed']:
        phase_stats[p]['completed'] += 1

# Find first unsolved module (Active Target)
active_module = None
for m in modules:
    if not m['completed']:
        active_module = m
        break

# Generate progress.svg
svg_content = f"""<svg width="400" height="60" viewBox="0 0 400 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .track {{
      fill: #e2e8f0;
    }}
    .fill {{
      fill: url(#grad);
      animation: load 2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
      width: 0px;
    }}
    .text {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 14px;
      font-weight: 600;
      fill: #0f172a;
      opacity: 0;
      animation: fadeIn 0.5s ease-out 1s forwards;
    }}
    @keyframes load {{
      to {{ width: {fill_width:.1f}px; }}
    }}
    @keyframes fadeIn {{
      to {{ opacity: 1; }}
    }}
    @media (prefers-color-scheme: dark) {{
      .track {{
        fill: #1e293b;
        stroke: #334155;
      }}
      .text {{
        fill: #f8fafc;
      }}
    }}
  </style>
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4F46E5" />
      <stop offset="50%" stop-color="#7C3AED" />
      <stop offset="100%" stop-color="#EC4899" />
    </linearGradient>
  </defs>
  
  <text x="0" y="18" class="text" style="animation: fadeIn 0.5s ease-out forwards; opacity: 1;">AI Engineering &amp; Agents Mastery</text>
  <text x="350" y="18" class="text">{pct:.1f}%</text>

  <rect x="0" y="30" width="400" height="16" rx="8" class="track" />
  <rect x="0" y="30" height="16" rx="8" class="fill" />
</svg>
"""

with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

# Target Module Card
active_card = ""
if active_module:
    a_no = active_module['no']
    a_phase = active_module['phase']
    a_cat = active_module['category']
    a_name = active_module['name']
    a_skills = active_module['skills']
    a_pri = active_module['pri_video']
    a_sup = active_module['sup_video']
    a_prac = active_module['practice']

    active_card = f"""---

## 🎯 Current Target Module (Study & Implement on the Go)

> **📱 Mobile Dashboard**: Watch your current video lesson, review the key interview concepts, and complete the hands-on engineering task straight from your phone or laptop!

### **Lesson #{a_no}: [{a_name}]({a_pri})**
* **Phase:** `{a_phase}` | **Category:** `{a_cat}`
* **Core Concepts & Interview Skills:** `{a_skills}`

#### 🎥 Video & Documentation Resources
* ▶️ **Primary Video Resource:** [Watch Lesson #{a_no} Video Tutorial]({a_pri})
* 📖 **Official Reference / Documentation:** [Read Documentation / Guide]({a_sup})

#### 🛠️ Hands-On Practice Task
> **Assignment:** {a_prac}

---
"""
else:
    active_card = """---

## 🏆 All 60 AI Engineering Modules Completed!
Congratulations on completing the entire **AI Engineering & Autonomous Agents Mastery Roadmap**! You are thoroughly equipped to architect, evaluate, secure, and deploy production-grade autonomous agent systems and enterprise RAG applications.

---
"""

phase_titles = {
    "Phase 0": "🛠️ Phase 0: Engineering Foundations & Modern Python Backend (Lessons 1–5)",
    "Phase 1": "⚡ Phase 1: LLM Application Engineering & Structured Outputs (Lessons 6–11)",
    "Phase 2": "🔍 Phase 2: Advanced Retrieval-Augmented Generation (RAG) (Lessons 12–19)",
    "Phase 3": "📊 Phase 3: RAG & LLM Evaluation Frameworks (Lessons 20–24)",
    "Phase 4": "🔄 Phase 4: Function Calling & The Agent Loop (Lessons 25–29)",
    "Phase 5": "🕸️ Phase 5: Stateful Workflows with LangGraph (Lessons 30–36)",
    "Phase 6": "🤖 Phase 6: Multi-Agent Architectures & Autonomous Swarms (Lessons 37–42)",
    "Phase 7": "🔌 Phase 7: Model Context Protocol (MCP) Ecosystem (Lessons 43–46)",
    "Phase 8": "🚀 Phase 8: Production Engineering & System Scalability (Lessons 47–52)",
    "Phase 9": "🛡️ Phase 9: AI Security, Red Teaming & Responsible Autonomy (Lessons 53–56)",
    "Phase 10": "🏆 Phase 10: Capstone: Production Autonomous Research & Synthesis Agent (Lessons 57–60)"
}

content = f"""# 🧠 AI Engineering & Autonomous Agents: 0 to Production Roadmap

Welcome to my personal **AI Engineering & Autonomous Agents** workspace and repository! This repo contains a comprehensive, **60-module production curriculum** covering the end-to-end lifecycle of modern Generative AI systems: from tokenomics, advanced hybrid RAG, and rigorous evaluations to LangGraph stateful loops, multi-agent swarms, Model Context Protocol (MCP), and enterprise security guardrails.

<p align="left">
  <img src="https://img.shields.io/badge/AI%20Engineering-{completed_count}%20%2F%20{total_modules}%20Completed-indigo?style=for-the-badge&logo=openai" alt="Modules Completed">
  <img src="https://img.shields.io/badge/Framework-LangGraph%20%7C%20FastMCP%20%7C%20FastAPI-blue?style=for-the-badge" alt="Framework">
  <img src="https://img.shields.io/badge/Focus-Production%20Agents%20%7C%20Advanced%20RAG-darkgreen?style=for-the-badge" alt="Focus">
  <img src="https://img.shields.io/badge/Track-0%20to%20Production%20Hero-purple?style=for-the-badge" alt="Track">
</p>

---

## 📊 Progress Dashboard

Track my interactive progress through the 11 phases of AI Engineering below:

<p align="left">
  <img src="./progress.svg" alt="AI Engineering Progress" width="400">
</p>

| Phase | Modules Completed | Progress Percentage | Status |
| :--- | :---: | :---: | :---: |
"""

for p_name in phase_order:
    stats = phase_stats.get(p_name, {'total': 0, 'completed': 0})
    p_pct = (stats['completed'] / stats['total']) * 100 if stats['total'] else 0
    indicator = "🟢 Active" if (stats['completed'] > 0 and stats['completed'] < stats['total']) else ("⚪ Not Started" if stats['completed'] == 0 else "🏆 Completed")
    short_title = phase_titles.get(p_name, p_name).split(":", 1)[1].strip() if ":" in phase_titles.get(p_name, p_name) else p_name
    content += f"| **{p_name}**: {short_title} | {stats['completed']} / {stats['total']} | {p_pct:.1f}% | {indicator} |\n"

content += f"""| **TOTAL** | **{completed_count} / {total_modules}** | **{pct:.1f}%** | **🧠 Engineering Grind** |

> 📱 **1-Tap Interactive Mobile Checklist**: You can directly check off completed lessons on your phone anytime:  
> 👉 [**Open Interactive Checkbox Issue #1**](https://github.com/Rakmo5/ai-engineering/issues/1)

{active_card}

## 📚 Repository Structure
```text
ai-engineering/
├── 00-foundations/             # Python typing, AsyncIO, Pydantic v2, REST & SQL
├── 01-llm-engineering/         # Tokenomics, Prompt versioning, Structured outputs & LiteLLM
├── 02-advanced-rag/            # Chunking, Embeddings, Hybrid search (BM25+Dense), Reranking & Citations
├── 03-evaluations/             # Golden test sets, Ragas, DeepEval, LLM-as-a-judge & Latency/Cost
├── 04-tool-calling/            # Function calling schemas, Safe execution, Idempotency & Confirmation gates
├── 05-langgraph-workflows/     # StateGraph, Nodes, Edges, MemorySaver, Human-in-the-loop & Time travel
├── 06-multi-agent-systems/     # Supervisor/Worker, Swarm handoffs, Reflection/Critique & Budget governors
├── 07-mcp-servers/             # FastMCP custom servers, stdio/SSE transports, Tools/Resources/Prompts
├── 08-production-fastapi/      # Async FastAPI, PostgreSQL persistence, Redis queue & Docker Compose
├── 09-security-guardrails/     # Prompt injection defenses, Sandboxing, OWASP LLM Top 10 & Audit logging
├── 10-capstone-agent/          # Full-stack Autonomous Research & Synthesis Agent with API & UI
├── notes/                      # Architectural cheat-sheets, pattern summaries & design diagrams
├── templates/                  # Learning log template, problem statement template & eval rubrics
├── AI_Engineering_Roadmap.xlsx # Master tracking spreadsheet with openpyxl formatting
├── generate_readme.py          # Auto-generates README.md, animated progress.svg & syncs with GitHub Issue #1
├── progress.svg                # Dynamic animated progress bar
├── sync.bat                    # 1-click Windows sync script (pull -> sync -> commit -> push)
└── requirements.txt            # All required Python packages
```

---

## 📂 Complete 60-Module Learning Path

"""

for p_name in phase_order:
    p_mods = [m for m in modules if m['phase'] == p_name]
    stats = phase_stats.get(p_name, {'total': 0, 'completed': 0})
    title = phase_titles.get(p_name, p_name)
    
    content += f"""
<details>
<summary><b>{title} ({stats['completed']}/{stats['total']} Completed)</b></summary>
<br>

| No. | Module Name | Key Concepts | Primary Video Link | Official Docs | Practice Task | Checkbox Status |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: |
"""
    for m in p_mods:
        status_box = "`[x]` ✅ Completed" if m['completed'] else ("`[~]` ⏳ In Progress" if m['status'] == "In Progress" else "`[ ]` ⚪ Not Started")
        content += f"| {m['no']} | {m['name']} | `{m['skills']}` | [Watch Video]({m['pri_video']}) | [Read Docs]({m['sup_video']}) | {m['practice']} | {status_box} |\n"
        
    content += "\n</details>\n"

content += """
---

## 🚀 Top 5% Engineering Masterclass: Open-Source Models, VRAM Math & Fine-Tuning

Beyond standard cloud APIs, top-tier AI Engineers master on-premise open-source inference, hardware memory budgets, fine-tuning, and high-performance data processing:

| Topic & Masterclass Guide | Core Engineering Skills | Runnable Code & Resources |
| :--- | :--- | :---: |
| 🧮 **GPU VRAM & Quantization Calculator** | VRAM formula $(P \\times B \\times 1.2)$, KV Cache sizing, PagedAttention, AWQ vs GGUF | [`notes/vram_quantization_math.md`](./notes/vram_quantization_math.md) |
| 🧭 **Architecture Decision Matrix** | When to use Prompting vs RAG vs Fine-Tuning vs Classical ML (XGBoost) | [`notes/rag_vs_finetuning_decision_matrix.md`](./notes/rag_vs_finetuning_decision_matrix.md) |
| ⚡ **Local Inference with vLLM & Ollama** | Self-hosting Llama 3.1 & Qwen 2.5, OpenAI-compatible vLLM server, continuous batching | [`01-llm-engineering/local_inference_vllm_ollama.py`](./01-llm-engineering/local_inference_vllm_ollama.py) |
| 🎯 **Fine-Tuning (PEFT / LoRA / QLoRA)** | Low-Rank Adaptation math $(\\Delta W = B \\cdot A)$, Unsloth acceleration, QLoRA NF4 | [`01-llm-engineering/finetuning_lora_unsloth.py`](./01-llm-engineering/finetuning_lora_unsloth.py) |
| 🏎️ **High-Speed Data Ingestion (DuckDB & Polars)** | 50x faster analytical filtering over Parquet/JSONL before vector embedding generation | [`02-advanced-rag/fast_data_duckdb_polars.py`](./02-advanced-rag/fast_data_duckdb_polars.py) |
| ☁️ **Amazon Bedrock & Enterprise Security** | Serverless foundation models (Claude 3.5 Sonnet), Knowledge Bases, Bedrock Guardrails | [`notes/amazon_bedrock_guide.md`](./notes/amazon_bedrock_guide.md) |

---

## ⏱️ Suggested Weekly Routine (8–12 Hours / Week)

| Activity | Hours per Week | Focus |
| :--- | :---: | :--- |
| **Official Documentation** | 2 hrs | Read docs before tutorials; understand specs and schemas |
| **Videos / Course Lessons** | 2 hrs | Watch selected video lessons actively; clarify architectural concepts |
| **Hands-On Implementation** | 3–5 hrs | Build minimal implementations from scratch; test edge cases |
| **Debugging & Experiments** | 1 hr | Measure retrieval accuracy, test failure paths and cost limits |
| **Notes & Self-Explanation** | 1 hr | Record what failed, why, and explain the architecture without notes |

---

## 📜 The 8 Core AI Engineering Rules

1. **Don't copy-paste a framework demo and call it production.** Understand the raw HTTP and JSON-RPC mechanics first.
2. **Never move to multi-agent swarms before mastering a single-agent loop.** Delegation multiplies failure rates if single nodes fail.
3. **Don't trust an LLM output just because it is valid JSON.** Validate data semantics, types, and constraints strictly with Pydantic.
4. **Don't assume RAG works without quantitative retrieval and answer evaluation.** Measure Hit Rate, Faithfulness, and MRR.
5. **Never grant an agent unlimited steps, unchecked tools, or infinite token budgets.** Always enforce step counters, timeouts, and human approval gates.
6. **Tool execution must happen in application code, never in prompt faith.** The model proposes actions; the application controls and executes them.
7. **Maintain audit trails.** Record every prompt, retrieved chunk ID, tool call argument, and latency metric.
8. **Be able to draw and explain the state graph of every project from memory without looking at code.**

---

## 🎯 Your First Assignment

Before adopting LangGraph or multi-agent frameworks, answer these 5 questions in your notes:
1. *What is the fundamental difference between an LLM call, a tool call, a workflow, and an autonomous agent?*
2. *In a basic RAG system, which components are purely deterministic and which involve probabilistic model decisions?*
3. *Why should tool execution strictly happen in application code rather than allowing the model arbitrary access?*
4. *What happens if an agent enters an infinite loop calling the same tool repeatedly, and how do you terminate it gracefully?*
5. *What quantitative evidence would convince you that adding a reranker genuinely improved your RAG pipeline?*

Then implement a raw Python function-calling loop with **two safe tools** (e.g., calculator and local notes lookup) without using any external agent framework.

---

## 🚀 How to Sync Progress

Whenever you check off an item on your phone via [Issue #1](https://github.com/Rakmo5/ai-engineering/issues/1) or edit the local Excel file:
1. Double-click **`sync.bat`** (or run `python generate_readme.py && git push`).
2. Your local Excel sheet, README, and animated progress SVG will automatically synchronize in seconds!

*“Understand the mechanism first. Learn the framework second. Build the system third. Evaluate it fourth.”* 💻🤖🚀
"""

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"SUCCESS: Generated README.md and progress.svg! (Completed: {completed_count}/{total_modules})")
