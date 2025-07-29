# pr_agent/core/summarizer.py

import os
import requests
from tiktoken import encoding_for_model

# from pr_agent.settings import (
#     OLLAMA_BASE_URL,
#     OLLAMA_MODEL_SHORT as MODEL,
#     EMBED_TOKEN_MODEL,
#     TOKEN_LIMIT,
# )

from pr_agent.settings import settings

ollama_base = settings.OLLAMA_BASE_URL
model = settings.OLLAMA_MODEL_SHORT
embed_token = settings.EMBED_TOKEN_MODEL
tok_limit = settings.TOKEN_LIMIT


def call_llama(model: str, messages=None, prompt: str = None, max_tokens: int = 256) -> str:
    """
    Send a chat or completion request to Ollama’s /v1 API.
    """
    endpoint = (
        f"{ollama_base}/chat/completions"
        if messages
        else f"{ollama_base}/completions"
    )
    payload = {
        "model": model,
        **({"messages": messages} if messages else {"prompt": prompt}),
        "max_tokens": max_tokens,
        "temperature": 0,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer nokey"
    }
    resp = requests.post(endpoint, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if messages:
        return data["choices"][0]["message"]["content"].strip()
    return data["choices"][0]["text"].strip()


def extract_summary(text: str) -> str:
    """
    Create a 250–350 word summary of `text` using:
      • <800 words → extract 5 sentences, optional truncate
      • 800–2 000 → extract 8 sentences, optional compress
      • >2 000 → chunk by ~500 words, extract 2 sentences/chunk, combine, compress
    Finally ensure under TOKEN_LIMIT tokens.
    """
    words = text.split()
    n = len(words)

    # Branch 1: short document
    if n < 800:
        summary = call_llama(
            model,
            prompt=f"Extract the 5 most important sentences from the following text:\n\n{text}",
            max_tokens=512
        )
        if len(summary.split()) > 300:
            summary = call_llama(
                model,
                prompt=f"Compress the following text into a concise 200–250 word summary:\n\n{summary}",
                max_tokens=300
            )

    # Branch 2: mid-length document
    elif n <= 2000:
        summary = call_llama(
            model,
            prompt=f"Extract the 8 most important sentences from the following text:\n\n{text}",
            max_tokens=512
        )
        if len(summary.split()) > 250:
            summary = call_llama(
                model,
                prompt=f"Rewrite the following into a concise 200–250 word summary:\n\n{summary}",
                max_tokens=300
            )

    # Branch 3: long document
    else:
        chunks = [" ".join(words[i : i + 500]) for i in range(0, n, 500)]
        extracted = []
        for chunk in chunks:
            extracted.append(
                call_llama(
                    model,
                    prompt=f"Extract the 2 most important sentences from the following text:\n\n{chunk}",
                    max_tokens=128
                )
            )
        summary = " ".join(extracted)
        if len(summary.split()) > 300:
            summary = call_llama(
                model,
                prompt=f"Rewrite the following into a concise 200–250 word summary:\n\n{summary}",
                max_tokens=300
            )

    # Final token-count check
    enc = encoding_for_model(embed_token)
    tokens = len(enc.encode(summary))
    if tokens > tok_limit:
        summary = call_llama(
            model,
            prompt=(
                f"Reduce the following summary to under {tok_limit} tokens. "
                "Keep it coherent and informative:\n\n"
                f"{summary}"
            ),
            max_tokens=tok_limit
        )

    return summary
