"""
BossAgent — LLM Client

Provider-agnostic wrapper for NVIDIA NIM and Nebius Token Factory.
Both expose an OpenAI-compatible API, so we use one client and switch
the base_url based on environment variable BOSSAGENT_PROVIDER.

Usage:
    from backend.llm.client import chat
    reply = chat("Say hello in one sentence.")
"""

import os
from openai import OpenAI


PROVIDERS = {
    "nvidia": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "api_key_env": "NVIDIA_API_KEY",
        "models": {
            "ultra": "nvidia/nemotron-3-ultra-550b-a55b",
            "super": "nvidia/nemotron-3-super-120b-a12b",
            "nano":  "nvidia/nemotron-3.5-lightning-30b-a3b",
            "lightning": "nvidia/nemotron-3.5-lightning-30b-a3b",
        },
    },
    "nebius": {
        "base_url": "https://api.tokenfactory.nebius.com/v1/",
        "api_key_env": "NEBIUS_API_KEY",
        "models": {
            "ultra": "Nemotron-3-Ultra-550b-a55b",
            "super": "Nemotron-3-Super-120b-a12b",
            "nano":  "Nemotron-3-Nano-30B-A3B",
            "lightning": "Nemotron-3.5-Lightning",
        },
    },
}


def _get_provider():
    name = os.environ.get("BOSSAGENT_PROVIDER", "nvidia").lower()
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider '{name}'.")
    return name, PROVIDERS[name]


def _get_client():
    _, provider = _get_provider()
    api_key = os.environ.get(provider["api_key_env"])
    if not api_key:
        raise RuntimeError(f"Missing {provider['api_key_env']}.")
    return OpenAI(base_url=provider["base_url"], api_key=api_key)


def get_model(tier: str) -> str:
    _, provider = _get_provider()
    if tier not in provider["models"]:
        raise ValueError(f"Unknown tier '{tier}'.")
    return provider["models"][tier]


def chat(message, tier="nano", system=None, max_tokens=200,
         temperature=0.7, json_mode=False) -> str:
    client = _get_client()
    model = get_model(tier)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})

    kwargs = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "extra_body": {"chat_template_kwargs": {"enable_thinking": False}},
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


if __name__ == "__main__":
    print("BossAgent LLM Client — test")
    print(f"Provider: {os.environ.get('BOSSAGENT_PROVIDER', 'nvidia')}")
    print(f"Model: {get_model('lightning')}")
    print("-" * 40)
    reply = chat("Say hello to the BossAgent project in one short sentence.")
    print(reply)
