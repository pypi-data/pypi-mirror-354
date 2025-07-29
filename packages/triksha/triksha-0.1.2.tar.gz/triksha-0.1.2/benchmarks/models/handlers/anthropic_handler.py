import os
import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
import time

from ..base_handler import ModelHandler


class AnthropicHandler(ModelHandler):
    """Model handler for Anthropic Claude models."""
    
    def __init__(self, api_key: str = None, verbose: bool = False):
        """Initialize the Anthropic handler.
        
        Args:
            api_key: Anthropic API key. If not provided, uses ANTHROPIC_API_KEY environment variable
            verbose: Whether to output verbose logging information.
        """
        super().__init__(verbose=verbose)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1"
        self.session = None
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
    
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            self.session = aiohttp.ClientSession(headers=headers)
            
    async def _close_session(self):
        """Close the aiohttp session if it exists"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def list_models(self) -> List[Dict[str, str]]:
        """List available models from Anthropic.
        
        Returns:
            List of dictionaries containing model information.
        """
        # Anthropic doesn't have a models endpoint, so return known models
        models = [
            {
                "id": "claude-3-opus-20240229",
                "name": "Claude 3 Opus",
                "provider": "anthropic"
            },
            {
                "id": "claude-3-sonnet-20240229", 
                "name": "Claude 3 Sonnet",
                "provider": "anthropic"
            },
            {
                "id": "claude-3-haiku-20240307",
                "name": "Claude 3 Haiku", 
                "provider": "anthropic"
            },
            {
                "id": "claude-2.1",
                "name": "Claude 2.1",
                "provider": "anthropic"
            },
            {
                "id": "claude-2.0",
                "name": "Claude 2.0",
                "provider": "anthropic"
            },
            {
                "id": "claude-instant-1.2",
                "name": "Claude Instant 1.2",
                "provider": "anthropic"
            }
        ]
        return models
    
    async def generate(self, model_id: str, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """Generate a response from the given prompt using the specified model.
        
        Args:
            model_id: Name of the model to use
            prompt: The prompt to generate a response for
            max_tokens: Maximum number of tokens to generate (optional, default 1000)
            temperature: Temperature for generation (optional, default 1.0)
            
        Returns:
            Generated text response
        """
        try:
            await self._ensure_session()
            
            if self.verbose:
                print(f"Generating with Anthropic model {model_id}")
            
            # Set defaults
            if max_tokens is None:
                max_tokens = 1000
            if temperature is None:
                temperature = 1.0
            
            # Prepare the request payload
            payload = {
                "model": model_id,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
                
            if self.verbose:
                print(f"Sending request to {self.base_url}/messages with model {model_id}")
                
            async with self.session.post(f"{self.base_url}/messages", json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    if self.verbose:
                        print(f"Error response: {error_text}")
                    raise Exception(f"Anthropic API error: {error_text}")
                
                response_data = await response.json()
                
                if self.verbose:
                    print(f"Received response from Anthropic")
                
                # Extract the response text
                if "content" in response_data and len(response_data["content"]) > 0:
                    return response_data["content"][0]["text"]
                else:
                    raise Exception("Invalid response format from Anthropic API")
                    
        except Exception as e:
            if self.verbose:
                print(f"Error during generation: {str(e)}")
            raise e
    
    async def test_prompt(self, model_id: str, prompt: str) -> Dict[str, Any]:
        """Test a prompt with the given model and return detailed results.
        
        Args:
            model_id: Name of the model to test
            prompt: The prompt to test
            
        Returns:
            Dictionary containing test results including response, timing, etc.
        """
        start_time = time.time()
        
        try:
            response = await self.generate(model_id, prompt)
            end_time = time.time()
            
            return {
                "success": True,
                "response": response,
                "model_id": model_id,
                "prompt": prompt,
                "response_time": end_time - start_time,
                "tokens_used": len(response.split()) if response else 0,
                "error": None
            }
            
        except Exception as e:
            end_time = time.time()
            
            return {
                "success": False,
                "response": None,
                "model_id": model_id,
                "prompt": prompt,
                "response_time": end_time - start_time,
                "tokens_used": 0,
                "error": str(e)
            }
    
    async def batch_generate(self, model_id: str, prompts: List[str], max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> List[str]:
        """Generate responses for multiple prompts.
        
        Args:
            model_id: Name of the model to use
            prompts: List of prompts to generate responses for
            max_tokens: Maximum number of tokens to generate per prompt
            temperature: Temperature for generation
            
        Returns:
            List of generated text responses
        """
        tasks = []
        for prompt in prompts:
            task = self.generate(model_id, prompt, max_tokens, temperature)
            tasks.append(task)
        
        # Execute all prompts concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error strings
        results = []
        for response in responses:
            if isinstance(response, Exception):
                results.append(f"Error: {str(response)}")
            else:
                results.append(response)
        
        return results
    
    async def close(self):
        """Close the handler and clean up resources."""
        await self._close_session()
        if self.verbose:
            print("Anthropic handler closed")
    
    def __del__(self):
        """Destructor to ensure session is closed."""
        if self.session and not self.session.closed:
            # Schedule cleanup if event loop is running
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self._close_session())
            except RuntimeError:
                # No event loop, can't clean up asyncio session
                pass 