"""
Base class for LLM providers.
All LLM providers must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMProvider(ABC):
    """Base class for all LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate a JSON response from the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            **kwargs: Additional parameters
            
        Returns:
            Parsed JSON response as dictionary
        """
        pass

