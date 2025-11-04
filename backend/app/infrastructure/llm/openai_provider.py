"""
OpenAI LLM Provider
"""

import json
import requests
from typing import Optional, Dict, Any
from app.infrastructure.llm.base import LLMProvider
from app.core.config import settings


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate text using OpenAI."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": kwargs.get("model", "gpt-4o-mini"),
            "messages": messages,
            **{k: v for k, v in kwargs.items() if k != "model"}
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Generate JSON response using OpenAI."""
        json_system_prompt = (system_prompt or "") + "\n\nRespond ONLY with valid JSON, no other text."
        
        # Use response_format for JSON mode if available
        kwargs_with_json = {**kwargs, "response_format": {"type": "json_object"}}
        
        response_text = self.generate(prompt, json_system_prompt, **kwargs_with_json)
        
        # Clean response
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

