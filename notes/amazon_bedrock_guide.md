# ☁️ Amazon Bedrock: Production Enterprise AI & Free Learning Path

## 1. What is Amazon Bedrock & Why is it High in Demand?
**Amazon Bedrock** is AWS's flagship serverless service for Generative AI. Instead of managing your own GPU clusters (EC2/SageMaker), Bedrock provides unified API access to leading Foundation Models (FMs):
- **Anthropic Claude 3.5 Sonnet & Haiku** (Industry leader in coding and reasoning)
- **Meta Llama 3 / 3.1 / 3.2**
- **Amazon Titan** (Embeddings & Text)
- **Cohere Command R+ & Embed**
- **Mistral Large**

### Why Enterprise Recruiters Value It:
1. **Data Privacy & Compliance**: Prompts and data never leave your AWS Virtual Private Cloud (VPC), and models are never trained on customer data.
2. **Enterprise Security**: Native integration with AWS IAM, CloudWatch, and AWS KMS encryption.
3. **Bedrock Knowledge Bases**: Fully managed RAG with OpenSearch Serverless or Aurora pgvector.
4. **Bedrock Guardrails**: Automated PII masking, toxic content filtering, and prompt injection defense.

---

## 2. How Bedrock Maps Directly to Your 60-Module Course

You don't need a separate roadmap—Bedrock maps 1:1 onto the exact patterns you are already mastering:

| Course Pattern | Open-Source / Framework Approach | Amazon Bedrock Equivalent | Where to Use in Repo |
| :--- | :--- | :--- | :--- |
| **Model Ingestion & APIs** | OpenAI / LiteLLM Python Client | `boto3.client('bedrock-runtime')` or `LiteLLM(model="bedrock/...")` | `01-llm-engineering/` |
| **Advanced RAG** | Qdrant + BM25 + Hybrid RRF | **Bedrock Knowledge Bases** (OpenSearch / Aurora) | `02-advanced-rag/` |
| **Agent Loops** | LangGraph StateGraph | **Amazon Bedrock Agents** (Action Groups via AWS Lambda) | `05-langgraph-workflows/` |
| **Safety & Redaction** | Presidio + Guardrails AI | **Amazon Bedrock Guardrails** (Content filters & PII mask) | `09-security-guardrails/` |
| **Observability** | OpenTelemetry / LangSmith | **AWS CloudWatch & CloudTrail Logs** | `08-production-fastapi/` |

---

## 3. How to Learn Amazon Bedrock for 100% FREE

Just like you learned foundational AWS on **AWS Skill Builder**, Amazon offers completely free official training, free sandbox labs, and digital certification badges for Bedrock:

### 🎓 1. Official Free AWS Skill Builder Courses (with Badges)
1. **[Amazon Bedrock Getting Started](https://explore.skillbuilder.aws/learn/course/external/view/elearning/17539/amazon-bedrock-getting-started)**  
   * **Duration:** 1 hour | **Cost:** FREE  
   * Covers: Foundation models, playgrounds, API invocations, and pricing models.
2. **[Building Generative AI Applications using Amazon Bedrock](https://explore.skillbuilder.aws/learn/course/external/view/elearning/17590/building-generative-ai-applications-using-amazon-bedrock)**  
   * **Duration:** ~3.5 hours | **Cost:** FREE  
   * Covers: Prompt engineering, LangChain integration, Knowledge Bases, and Agents.
3. **[Generative AI Learning Plan for Developers](https://explore.skillbuilder.aws/learn/public/learning_plan/view/2034/generative-ai-learning-plan-for-developers)**  
   * Comprehensive official AWS digital learning plan with a verifiable badge for your LinkedIn profile.

### 💻 2. Free Hands-On Workshop Labs (No Cost)
* **[Official Amazon Bedrock Workshop (GitHub)](https://github.com/aws-samples/amazon-bedrock-workshop)**:  
  Contains dozens of ready-to-run Jupyter notebooks covering text generation, embeddings, RAG, and Agents.
* **AWS Workshop Studio & AWS Educate**:  
  Look out for free AWS-sponsored community immersion days on AWS Workshop Studio, which provide free temporary 4-hour AWS sandbox credentials with zero credit card required!

---

## 4. Hands-On Python Code: Calling Bedrock via `boto3` & `LiteLLM`

### Method A: Native AWS SDK (`boto3`)
```python
import boto3
import json

client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# New Converse API (unified schema for Claude, Llama 3, Titan)
response = client.converse(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages=[
        {"role": "user", "content": [{"text": "Explain hybrid search in 2 sentences."}]}
    ],
    inferenceConfig={"maxTokens": 100, "temperature": 0.2}
)

output_text = response["output"]["message"]["content"][0]["text"]
print(output_text)
```

### Method B: Unified LiteLLM Integration (Matches our Course!)
Since you already learn `LiteLLM` in **Phase 1 (Lesson 10)**, calling Bedrock requires zero new syntax:
```python
import litellm

# LiteLLM automatically uses your AWS credentials from ~/.aws/credentials or env vars
response = litellm.completion(
    model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages=[{"role": "user", "content": "Explain agent loops."}]
)
print(response.choices[0].message.content)
```

---

## 5. Adding Amazon Bedrock to Your Resume
When you complete this module, list it under your Skills and Projects:
* **Cloud & LLM Platforms:** Amazon Bedrock (Claude 3.5 Sonnet, Titan), AWS Lambda, IAM, boto3
* **Project Highlight:** *Integrated Amazon Bedrock via boto3 and LiteLLM, configuring model fallbacks and secure IAM least-privilege policies for enterprise compliance.*
