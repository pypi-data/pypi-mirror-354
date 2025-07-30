"""
LiteLLM integration for easy LLM calls in BubbleTea bots
"""

from typing import List, Dict, Optional, AsyncGenerator
import litellm
from litellm import acompletion, completion


class LLM:
    """
    Simple wrapper around LiteLLM for easy LLM calls
    
    Example:
        llm = LLM(model="gpt-3.5-turbo")
        response = llm.complete("Hello, how are you?")
        
        # Streaming
        async for chunk in llm.stream("Tell me a story"):
            yield Text(chunk)
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo", **kwargs):
        self.model = model
        self.default_params = kwargs
    
    def complete(self, prompt: str, **kwargs) -> str:
        """
        Get a completion from the LLM
        
        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters to pass to litellm
            
        Returns:
            The LLM's response as a string
        """
        params = {**self.default_params, **kwargs}
        messages = [{"role": "user", "content": prompt}]
        
        response = completion(
            model=self.model,
            messages=messages,
            **params
        )
        
        return response.choices[0].message.content
    
    async def acomplete(self, prompt: str, **kwargs) -> str:
        """
        Async version of complete()
        """
        params = {**self.default_params, **kwargs}
        messages = [{"role": "user", "content": prompt}]
        
        response = await acompletion(
            model=self.model,
            messages=messages,
            **params
        )
        
        return response.choices[0].message.content
    
    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream a completion from the LLM
        
        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters to pass to litellm
            
        Yields:
            Chunks of the LLM's response
        """
        params = {**self.default_params, **kwargs}
        messages = [{"role": "user", "content": prompt}]
        
        response = await acompletion(
            model=self.model,
            messages=messages,
            stream=True,
            **params
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Get a completion with full message history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters to pass to litellm
            
        Returns:
            The LLM's response as a string
        """
        params = {**self.default_params, **kwargs}
        
        response = completion(
            model=self.model,
            messages=messages,
            **params
        )
        
        return response.choices[0].message.content
    
    async def astream_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream a completion with full message history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters to pass to litellm
            
        Yields:
            Chunks of the LLM's response
        """
        params = {**self.default_params, **kwargs}
        
        response = await acompletion(
            model=self.model,
            messages=messages,
            stream=True,
            **params
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content