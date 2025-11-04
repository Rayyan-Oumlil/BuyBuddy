"""
LLM Provider Factory
Creates the appropriate LLM provider based on configuration.
"""

from app.core.config import settings
from app.infrastructure.llm.base import LLMProvider
from app.infrastructure.llm.ollama_provider import OllamaProvider
from app.infrastructure.llm.deepseek_provider import DeepSeekProvider
from app.infrastructure.llm.openai_provider import OpenAIProvider


def get_llm_provider() -> LLMProvider:
    """
    Factory function to get the configured LLM provider.
    
    Returns:
        LLMProvider instance based on LLM_PROVIDER setting
    """
    provider_name = settings.llm_provider.lower()
    
    if provider_name == "ollama":
        return OllamaProvider()
    elif provider_name == "deepseek":
        return DeepSeekProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    else:
        raise ValueError(
            f"Unknown LLM provider: {provider_name}. "
            f"Supported: ollama, deepseek, openai"
        )

