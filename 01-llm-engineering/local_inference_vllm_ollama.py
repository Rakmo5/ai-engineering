"""
Advanced Elective 1: Local Open-Source LLM Inference with Ollama & vLLM
Demonstrates how to run and serve open-source models (Llama 3.1 8B, Qwen 2.5) locally
with zero cloud API cost and complete data privacy.
"""

import os
import json
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# 1. Ollama Local Inference (Development & Local Testing)
# Ollama runs models locally and exposes an OpenAI-compatible REST API at port 11434.
# Command to run locally: `ollama run llama3.1:8b`
# ---------------------------------------------------------------------------

def call_ollama_local(prompt: str, model: str = "llama3.1:8b"):
    """
    Sends a generation request to a local Ollama instance.
    Standard endpoint: http://localhost:11434/api/generate
    """
    url = "http://localhost:11434/api/generate"
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 150
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"--- Ollama ({model}) Response ---")
            print(data.get("response", "").strip())
            print(f"Tokens evaluated: {data.get('eval_count', 'N/A')}")
    except urllib.error.URLError:
        print("[Ollama Note] Local Ollama daemon not running at localhost:11434.")
        print("To test locally: install Ollama from https://ollama.ai and run: `ollama run llama3.1:8b`")


# ---------------------------------------------------------------------------
# 2. Production High-Throughput Serving with vLLM
# vLLM is the industry standard for production serving of open-source models.
# It uses PagedAttention to eliminate memory fragmentation in the KV cache.
#
# Production launch command:
# vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct --port 8000 --max-model-len 8192 --gpu-memory-utilization 0.90
#
# vLLM exposes an exact drop-in replacement for the OpenAI API!
# ---------------------------------------------------------------------------

def call_vllm_openai_compatible(prompt: str, base_url: str = "http://localhost:8000/v1"):
    """
    Calls a production vLLM instance using the standard OpenAI client schema.
    Because vLLM is 100% OpenAI API compatible, existing code requires ZERO rewrites.
    """
    try:
        from openai import OpenAI

        # Point OpenAI client to your self-hosted vLLM server
        client = OpenAI(
            base_url=base_url,
            api_key="EMPTY"  # vLLM doesn't require a key unless behind a reverse proxy
        )

        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            messages=[
                {"role": "system", "content": "You are a senior systems engineer. Explain concepts concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=150
        )
        print("\n--- vLLM Server Response ---")
        print(response.choices[0].message.content)
    except Exception as e:
        print("\n[vLLM Note] Local vLLM server not currently running at localhost:8000.")
        print("Production Pattern: vLLM replaces OpenAI calls with self-hosted private GPUs at 90% cost reduction.")


# ---------------------------------------------------------------------------
# 3. Unified LiteLLM Routing (Cloud vs Self-Hosted Fallback)
# ---------------------------------------------------------------------------

def unified_routing_example():
    """
    LiteLLM can route between local Ollama, self-hosted vLLM, and cloud Bedrock/OpenAI
    using the exact same syntax!
    """
    try:
        import litellm

        print("\n--- LiteLLM Multi-Backend Syntax Example ---")
        print("1. Local Ollama: litellm.completion(model='ollama/llama3.1:8b', messages=[...])")
        print("2. Self-Hosted vLLM: litellm.completion(model='openai/meta-llama/3.1-8b', api_base='http://localhost:8000/v1')")
        print("3. Cloud AWS Bedrock: litellm.completion(model='bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0')")
    except ImportError:
        pass


if __name__ == "__main__":
    print("Testing Local Open-Source LLM Inference Patterns...\n")
    call_ollama_local("Explain what PagedAttention is in two sentences.")
    call_vllm_openai_compatible("What are the advantages of self-hosting models over cloud APIs?")
    unified_routing_example()
