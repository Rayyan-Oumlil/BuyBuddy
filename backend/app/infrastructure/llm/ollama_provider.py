"""
Ollama LLM Provider
"""

import json
import requests
from typing import Optional, Dict, Any
from app.infrastructure.llm.base import LLMProvider
from app.core.config import settings


class OllamaProvider(LLMProvider):
    """Ollama LLM provider."""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.api_url = f"{self.base_url}/api/generate"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate text using Ollama."""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Generate JSON response using Ollama."""
        json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON, no other text."
        
        response_text = self.generate(json_prompt, system_prompt, **kwargs)
        
        # Clean response (remove markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}\nResponse: {response_text}")

