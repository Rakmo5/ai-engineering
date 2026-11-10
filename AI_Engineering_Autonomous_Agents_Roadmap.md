# AI Engineering & Autonomous Agents --- Self-Learning Roadmap

**Starting point:** You know basic LLM concepts and have built or
studied simple RAG. You also have Python/FastAPI exposure.\
**Goal:** Learn to design, build, evaluate, secure, and deploy reliable
LLM applications and autonomous agents.\
**Pace:** 12--16 weeks, approximately 8--12 hours per week. Adjust
around college and internship commitments.

## How to study

This is a self-learning plan. Prioritize understanding over finishing
quickly.

For each topic: 1. Write down what you already know and what you don't.
2. Read official documentation before relying on a tutorial. 3. Watch
the selected video to clarify concepts; don't binge passively. 4.
Implement a small version yourself without copying line by line. 5. Test
edge cases and failure paths. 6. Explain the architecture and trade-offs
in your own words. 7. Record what failed, why, and how you fixed it.

**Rule:** Understand the underlying engineering pattern before adopting
a framework.

------------------------------------------------------------------------

# Phase 0 --- Refresh foundations (3--5 days)

Revise Python functions/classes, typing, exceptions, virtual
environments, async/await, HTTP, JSON, Pydantic, REST, Git, SQL joins,
indexes, and transactions.

**Documentation** - [Python
Tutorial](https://docs.python.org/3/tutorial/) - [FastAPI
Tutorial](https://fastapi.tiangolo.com/tutorial/) - [Pydantic
Docs](https://docs.pydantic.dev/latest/) - [PostgreSQL
Tutorial](https://www.postgresql.org/docs/current/tutorial.html) - [Pro
Git Book](https://git-scm.com/book/en/v2)

**Checkpoint:** Build a small FastAPI service with GET and POST
endpoints, Pydantic validation, useful errors, a simple database
operation, and tests. Explain the full request-response lifecycle.

# Phase 1 --- LLM application engineering (Week 1)

## Learn

-   Messages, roles, context windows, tokens
-   Temperature and output limits
-   Structured outputs and JSON schemas
-   Pydantic validation
-   Prompt templates and prompt versioning
-   Streaming, provider abstraction, timeouts, retries, rate limits, and
    cost tracking

**Docs** - [OpenAI API Docs](https://developers.openai.com/api/docs/) -
[Structured
Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) -
[Pydantic](https://docs.pydantic.dev/latest/)

**Video reference** - [Krish Naik --- Complete Agentic AI
Course](https://www.youtube.com/watch?v=rV3HJ4LEZ7k) --- use the
introductory LLM/application sections selectively.

## Build: Structured extraction API

Accept text, extract defined fields with an LLM, validate using
Pydantic, handle missing/invalid fields, store results, and record
latency and token usage where available.

**Checkpoint questions** - Why is valid JSON not necessarily correct
data? - What happens if a required field is missing? - When should a
request be retried? - Why should retries be bounded?

# Phase 2 --- Advanced RAG (Weeks 2--3)

You already know simple RAG. Focus on improving retrieval and diagnosing
retrieval failures.

## Learn in this order

1.  Document ingestion and parsing
2.  Fixed, recursive, semantic, and parent-child chunking
3.  Metadata and access-control filtering
4.  Embeddings and vector similarity
5.  Sparse retrieval / BM25
6.  Hybrid search (sparse + dense)
7.  Reranking
8.  Query rewriting and multi-query retrieval
9.  Context compression and deduplication
10. Citations and source-grounded answers

**Docs and reading** - [LlamaIndex
Documentation](https://docs.llamaindex.ai/) - [LlamaIndex ---
Understanding /
RAG](https://docs.llamaindex.ai/en/stable/understanding/) - [Pinecone
Learning Center](https://www.pinecone.io/learn/) - [Elasticsearch Hybrid
Search](https://www.elastic.co/what-is/hybrid-search) - [Cohere
Rerank](https://docs.cohere.com/docs/rerank)

**Videos** - [James Briggs --- Rerankers for
RAG](https://www.youtube.com/watch?v=Uh9bYiVrW_s) - [Krish Naik ---
Complete Agentic AI Course](https://www.youtube.com/watch?v=rV3HJ4LEZ7k)
--- use the RAG sections selectively.

## Build: Advanced document assistant

Ingest PDFs/text, chunk with metadata, retrieve with dense and sparse
methods, combine results, rerank, and answer with citations. It must say
when evidence is insufficient.

**Experiment:** Prepare at least 20 questions with expected source
passages. Compare dense retrieval, hybrid retrieval, and hybrid plus
reranking. Record which approach retrieves the evidence most reliably.
Don't assume complexity improves quality; measure it.

**Checkpoint:** Explain chunk-size trade-offs, sparse vs dense
retrieval, reranking, metadata filters, and why retrieved context does
not guarantee a faithful answer.

# Phase 3 --- RAG and LLM evaluation (Week 4)

## Learn

-   Evaluation datasets and expected evidence
-   Precision@k, Recall@k, Mean Reciprocal Rank (MRR)
-   Answer correctness, relevance, groundedness, faithfulness
-   LLM-as-a-judge and its limitations
-   Regression tests for prompt/model changes
-   Latency, cost, and failure-rate measurement
-   Human review and error categorization

**Resources** - [Ragas Docs](https://docs.ragas.io/) - [Ragas Available
Metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) -
[DeepLearning.AI Short
Courses](https://www.deeplearning.ai/short-courses/) - [LangSmith
Evaluation](https://docs.smith.langchain.com/evaluation)

**Build:** Create an evaluation script for your RAG system. Store 20--50
test questions, compare retrieval configurations, calculate retrieval
metrics, score answer quality with a rubric/evaluator, track
latency/cost, and save results.

**Checkpoint:** Show evidence that one approach is better on your test
set and explain where it still fails.

# Phase 4 --- Tool calling and the agent loop (Weeks 5--6)

## Understand the loop

1.  User provides a goal.
2.  Model decides whether a tool is needed.
3.  Model returns a structured tool call.
4.  Application validates arguments and permissions.
5.  Application executes the tool.
6.  Tool result is returned to the model.
7.  Model decides whether to continue or finish.

The model proposes actions; **your application controls and executes
them**.

## Learn

-   Function/tool schemas and selection
-   Argument validation
-   Tool results and multiple calls
-   Tool errors, retries, and timeouts
-   Authentication and authorization
-   Idempotency and duplicate side effects
-   Tool allowlists and execution limits

**Docs** - [OpenAI Function
Calling](https://developers.openai.com/api/docs/guides/function-calling) -
[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) -
[Agents SDK
Quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart) -
[Hugging Face --- Agent
Fundamentals](https://huggingface.co/learn/agents-course/unit1/introduction)

**Videos** - [freeCodeCamp --- LangGraph Complete
Course](https://www.youtube.com/watch?v=jGg_1h0qzaM) - [Krish Naik ---
Complete Agentic AI Course](https://www.youtube.com/watch?v=rV3HJ4LEZ7k)

**Build:** A tool-using assistant with three safe tools: search a local
knowledge base, query a read-only database, and create a draft
task/ticket. Require confirmation before sending messages, changing
records, spending money, or affecting real users.

**Checkpoint:** Explain function calling vs text generation, why
arguments need validation, why unrestricted database access is unsafe,
and how to handle tool timeouts and duplicate actions.

# Phase 5 --- Agent fundamentals and LangGraph (Weeks 7--8)

## Learn

-   Agent = model + instructions + tools + state/runtime
-   Think → Act → Observe loop
-   Planning and task decomposition
-   State and memory
-   Conditional routing
-   Sequential and parallel execution
-   Iteration and termination
-   Human-in-the-loop approval

LangGraph models applications as stateful graphs with state, nodes,
transitions, and conditions. It is useful when workflows need controlled
multi-step execution, persistence, interruption, and recovery.

**Primary course** - [LangChain Academy --- Introduction to
LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) ---
free, 55 lessons, approximately six hours.

**Docs** - [LangGraph
Documentation](https://docs.langchain.com/oss/python/langgraph/overview) -
[LangChain Learn /
Tutorials](https://docs.langchain.com/oss/python/learn) - [LangGraph
Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) -
[LangGraph Interrupts /
Human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/interrupts)

**Videos** - [freeCodeCamp --- LangGraph Complete
Course](https://www.youtube.com/watch?v=jGg_1h0qzaM) - [DeepLearning.AI
--- AI Agents in
LangGraph](https://www.deeplearning.ai/courses/ai-agents-in-langgraph/)

**Build:** A stateful research assistant that plans a task, searches
approved sources, stores findings, checks evidence, revises searches
when needed, and creates a cited report. Pause for approval before
external side effects.

**Checkpoint:** Draw the graph and explain every node, state field,
edge, termination condition, and failure path without looking at code.

# Phase 6 --- Autonomous and multi-agent systems (Weeks 9--10)

Autonomy is not an unlimited LLM loop. It is goal-directed execution
through controlled decisions and actions, with limits and safety
boundaries.

## Learn

-   Goal decomposition, planning, and replanning
-   Short-term state vs persistent memory
-   Reflection and critique loops
-   Tool selection and delegation
-   Supervisor/worker, router, handoff, and parallel-specialist patterns
-   Shared vs isolated state
-   Termination conditions
-   Budgets: maximum steps, time, tokens, and tool calls
-   Human approval and escalation

**Resources** - [Hugging Face Agents
Course](https://huggingface.co/learn/agents-course/en/unit0/introduction)
--- free structured course covering agent theory, practice, smolagents,
LangGraph, and LlamaIndex. - [Hugging Face --- Agent
Fundamentals](https://huggingface.co/learn/agents-course/unit1/introduction) -
[LangChain Academy ---
LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) -
[LangChain Learn --- Multi-agent
tutorials](https://docs.langchain.com/oss/python/learn) - [OpenAI Agents
SDK](https://openai.github.io/openai-agents-python/)

**Build:** A bounded research workflow with a planner, researcher,
reviewer, and writer. Track sources, detect repeated/unproductive tool
calls, enforce a maximum step count, and stop when complete or out of
budget.

**Important:** Start with one agent and a few tools. Add delegation only
when you can show that it improves results.

**Checkpoint** - When is a deterministic workflow better than an
agent? - When does multi-agent delegation help? - How can agents amplify
each other's errors? - How do you prevent loops? - How do you measure
whether autonomy improves task success?

# Phase 7 --- MCP and external tool ecosystems (Week 11)

MCP (Model Context Protocol) is a protocol for connecting AI
applications to external tools and context providers through a
standardized interface.

## Learn

-   Hosts, clients, and servers
-   Tools, resources, and prompts
-   Local vs remote MCP servers
-   Authentication and authorization
-   Tool discovery and schema handling
-   Trust boundaries and permissions

**Resources** - [MCP Official
Documentation](https://modelcontextprotocol.io/introduction) - [MCP
Specification](https://modelcontextprotocol.io/specification/latest) -
[MCP Tutorials](https://modelcontextprotocol.io/docs/tutorials)

**Build:** Create a small MCP server exposing two harmless tools, such
as searching local notes and retrieving a record from a sample database.
Test invalid inputs, unauthorized access, and unavailable tools.

**Checkpoint:** Explain how MCP differs from a normal function call and
why exposing a tool through MCP does not automatically make it safe.

# Phase 8 --- Production engineering (Weeks 12--13)

This is what turns an AI demo into a maintainable application.

## Backend and data

-   FastAPI structure and async I/O
-   PostgreSQL schema design and transactions
-   Redis and caching
-   Background workers and queues
-   Authentication, authorization, and tenant isolation
-   Database migrations

## Reliability

-   Timeouts and bounded retries
-   Exponential backoff and jitter
-   Idempotency
-   Rate limiting and circuit breakers
-   Failure states and recovery
-   Graceful degradation

## Deployment and observability

-   Docker and Docker Compose
-   Environment configuration and secrets
-   CI/CD basics
-   Structured logging, metrics, and traces
-   Request IDs and correlation
-   Latency, cost, token, and error monitoring

**Resources** - [FastAPI
Tutorial](https://fastapi.tiangolo.com/tutorial/) - [PostgreSQL
Docs](https://www.postgresql.org/docs/current/) - [Redis
Docs](https://redis.io/docs/latest/) - [Docker Get
Started](https://docs.docker.com/get-started/) - [OpenAI Agents SDK
Tracing](https://openai.github.io/openai-agents-python/tracing/) -
[OpenAI Agents SDK
Guardrails](https://openai.github.io/openai-agents-python/guardrails/)

**Build:** Turn your research agent into a backend service with FastAPI
endpoints, PostgreSQL persistence, background execution, job statuses,
bounded budgets, logs/traces, tests, and Docker-based local deployment.

# Phase 9 --- Security and responsible autonomy (Week 14)

## Learn

-   Prompt injection and indirect prompt injection
-   Untrusted retrieved content
-   Secrets and personal-data handling
-   Least-privilege tool permissions
-   Human approval for high-impact actions
-   Audit logs
-   Agent goal-success evaluation
-   Tool-call accuracy
-   Regression tests and cost/latency budgets

**Resources** - [OWASP Top 10 for LLM
Applications](https://genai.owasp.org/llm-top-10/) - [OWASP GenAI
Security Project](https://genai.owasp.org/) - [Ragas
Metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) -
[Agents SDK
Guardrails](https://openai.github.io/openai-agents-python/guardrails/) -
[Agents SDK
Tracing](https://openai.github.io/openai-agents-python/tracing/)

**Build:** Test malicious instructions in retrieved documents,
cross-user data access, invalid tool arguments, tool timeouts, repeated
failures, loops, actions without approval, and unsupported claims.
Record expected vs actual behavior.

# Phase 10 --- Capstone: Production-grade autonomous research agent (Weeks 15--16+)

## Product

Build an assistant that accepts a research goal, gathers evidence from
approved sources, evaluates evidence, and produces a cited report.

## Suggested architecture

``` text
User
  |
  v
FastAPI Backend
  |
  v
Job Manager ---- PostgreSQL
  |
  v
Agent Orchestrator
  |
  +---- Planner
  +---- Search / Retrieval Tools
  +---- Evidence Store
  +---- Reviewer / Evaluator
  +---- Report Generator
  |
  v
Human Approval (when required)
  |
  v
Final Report
```

## Minimum features

-   User authentication
-   Research-job creation and persistent status
-   Bounded agent loop
-   At least two useful tools
-   Evidence and source tracking
-   Final report with citations
-   Human approval before external side effects
-   Evaluation dataset
-   Logging and tracing
-   Docker-based local setup
-   Automated tests

## Stretch features

-   Multi-agent delegation
-   Multiple retrieval sources
-   Background execution
-   Streaming progress updates
-   Cost and latency dashboard
-   Retry and recovery from interrupted runs

## Definition of done

The project must handle missing evidence, stop when its budget is
exhausted, recover safely from transient failures, avoid duplicate side
effects, isolate user data, show sources for claims, and pass a
repeatable evaluation suite.

------------------------------------------------------------------------

# Suggested weekly routine

  Activity                       Hours per week
  ---------------------------- ----------------
  Official documentation                      2
  Videos / course lessons                     2
  Hands-on implementation                  3--5
  Debugging and experiments                   1
  Notes and self-explanation                  1

Keep DSA practice separate. This roadmap develops AI application and
backend skills; it does not replace DSA, operating systems, networking,
databases, or system-design preparation.

# Learning log template

Use this for every topic:

``` markdown
## Topic:

### What I think I know

### Questions I need to answer

### Official documentation read

### Video/course watched

### What I implemented myself

### What failed and why

### What I changed

### Trade-offs and limitations

### Explain it without notes

### Next experiment
```

# Rules for this journey

1.  Don't copy a complete GitHub project and call it your own.
2.  Don't move to multi-agent systems before understanding a
    single-agent loop.
3.  Don't trust an LLM output just because it is valid JSON.
4.  Don't assume RAG works without retrieval and answer evaluation.
5.  Don't give an agent unlimited steps, tools, or permissions.
6.  Read official documentation alongside tutorials.
7.  Record bugs you solved and engineering decisions you made.
8.  Be able to draw and explain every project's architecture.

------------------------------------------------------------------------

# Your first assignment

Before starting LangGraph, answer these questions in your own words:

1.  What is the difference between an LLM call, a tool call, a workflow,
    and an agent?
2.  In a basic RAG system, which components are deterministic and which
    involve model-generated decisions?
3.  Why should tool execution happen in application code rather than
    trusting the model to perform arbitrary actions?
4.  What would happen if an agent calls the same tool repeatedly without
    making progress?
5.  What evidence would convince you that your RAG system is better
    after adding a reranker?

Then implement a small Python function-calling assistant with **two
tools**, without using LangGraph. Once you can explain the tool-call
loop, move to LangGraph.

**Guiding principle:** Understand the mechanism first. Learn the
framework second. Build the system third. Evaluate it fourth.
