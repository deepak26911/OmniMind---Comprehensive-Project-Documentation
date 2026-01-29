# -*- coding: utf-8 -*-
"""
LLM Client

Claude API client wrapper for agent services.
Uses the Anthropic SDK for all LLM interactions.
"""
import anthropic
from typing import Optional, List, Dict

from .config import (
    DEFAULT_LLM_BASE_URL,
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_API_KEY,
)


# Global client instance (will be initialized on first use or via configure)
_client: Optional[anthropic.Anthropic] = None
_current_config = {
    "api_key": DEFAULT_LLM_API_KEY,
}


def configure(base_url: str = None, api_key: str = None) -> anthropic.Anthropic:
    """
    Configure the LLM client with custom API key.

    Args:
        base_url: Ignored for Claude (kept for compatibility)
        api_key: Anthropic API key

    Returns:
        Configured Anthropic client instance
    """
    global _client, _current_config

    if api_key:
        _current_config["api_key"] = api_key

    _client = anthropic.Anthropic(
        api_key=_current_config["api_key"],
    )
    return _client


def get_client() -> anthropic.Anthropic:
    """Get or create the Anthropic client."""
    global _client
    if _client is None:
        _client = anthropic.Anthropic(
            api_key=_current_config["api_key"],
        )
    return _client


def chat(
    message: str,
    model: str = DEFAULT_LLM_MODEL,
    max_tokens: int = 1024,
) -> str:
    """
    Send a single message and get response.

    Args:
        message: User message content
        model: Model identifier (e.g., claude-sonnet-4-20250514)
        max_tokens: Maximum tokens in response

    Returns:
        Model's response text
    """
    # Force use of Claude model if "default" or empty is passed
    if model == "default" or not model:
        model = DEFAULT_LLM_MODEL
    
    client = get_client()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": message}],
    )
    return response.content[0].text


def chat_with_history(
    messages: list,
    model: str = DEFAULT_LLM_MODEL,
    max_tokens: int = 1024,
    temperature: float = 0.6,
) -> str:
    """
    Chat with message history.

    Args:
        messages: List of message dicts with role and content
        model: Model identifier (e.g., claude-sonnet-4-20250514)
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature (0.0 - 1.0)

    Returns:
        Model's response text

    Raises:
        ValueError: If the API returns an invalid or empty response
    """
    # Force use of Claude model if "default" or empty is passed
    if model == "default" or not model:
        model = DEFAULT_LLM_MODEL
    
    client = get_client()
    
    # Extract system message if present (Claude handles system separately)
    system_content = None
    filtered_messages = []
    
    for msg in messages:
        if msg.get("role") == "system":
            system_content = msg.get("content", "")
        else:
            filtered_messages.append(msg)
    
    # Build the API call kwargs
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": filtered_messages,
    }
    
    if system_content:
        kwargs["system"] = system_content
    
    response = client.messages.create(**kwargs)

    # Validate response structure
    if response is None:
        raise ValueError("Claude API returned None response")

    if not hasattr(response, 'content') or response.content is None:
        raise ValueError(f"Claude API returned response without content: {response}")

    if len(response.content) == 0:
        raise ValueError("Claude API returned empty content list")

    content_block = response.content[0]
    
    # Handle text response
    if hasattr(content_block, 'text'):
        return content_block.text
    
    # Handle tool use response
    if hasattr(content_block, 'type') and content_block.type == 'tool_use':
        import json
        tool_name = content_block.name
        tool_input = json.dumps(content_block.input) if isinstance(content_block.input, dict) else str(content_block.input)
        return f"<|channel|>commentary to=functions.{tool_name}<|message|>{tool_input}<|call|>"
    
    raise ValueError(f"Claude API returned unexpected content type: {content_block}")


if __name__ == "__main__":
    result = chat("1+1=?")
    print(result)