"""
DeepSeek LLM Provider
"""

import json
import requests
from typing import Optional, Dict, Any
from app.infrastructure.llm.base import LLMProvider
from app.core.config import settings


class DeepSeekProvider(LLMProvider):
    """DeepSeek LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or settings.deepseek_api_key
        self.base_url = base_url or settings.deepseek_base_url
        self.api_url = f"{self.base_url}/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("DeepSeek API key is required. Set DEEPSEEK_API_KEY in .env")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate text using DeepSeek."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            **kwargs
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
            raise Exception(f"DeepSeek API error: {str(e)}")
    
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Generate JSON response using DeepSeek."""
        json_system_prompt = (system_prompt or "") + "\n\nRespond ONLY with valid JSON, no other text."
        
        response_text = self.generate(prompt, json_system_prompt, **kwargs)
        
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

