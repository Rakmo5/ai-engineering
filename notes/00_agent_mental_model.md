# The Agent Mental Model

## 1. What is an Agent?
An **Agent** is not an open-ended autonomous loop running wild. In production engineering, an agent is defined as:

$$\text{Agent} = \text{Model} + \text{System Instructions} + \text{Typed Tools} + \text{Stateful Runtime} + \text{Budget Constraints}$$

## 2. Deterministic vs Probabilistic Boundaries
- **Probabilistic (The Model)**: Language synthesis, query decomposition, semantic summarization, tool selection proposal.
- **Deterministic (Your Code)**: Tool argument validation (Pydantic), tool execution permissions, database transactions, loop termination, rate limits, audit logging.

**Golden Rule:** The model *proposes* actions. The application *validates, restricts, and executes* them.
