"""
Model-specific dataset formatting templates for fine-tuning different LLMs
"""
from typing import Dict, List, Any, Optional, Callable
import json

class ModelFormatTemplate:
    """Base class for model-specific formatting templates"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def format_dataset(self, prompts: List[str], completions: Optional[List[str]] = None) -> Dict[str, Any]:
        """Format the dataset according to this template's requirements"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_sample_format(self) -> str:
        """Return a sample of the expected format for this model"""
        raise NotImplementedError("Subclasses must implement this method")

class OpenAIFormat(ModelFormatTemplate):
    """
    Format for OpenAI fine-tuning API
    
    Format: JSONL files with messages array containing role/content pairs
    Example:
    {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
    """
    
    def __init__(self):
        super().__init__(
            name="OpenAI ChatGPT",
            description="Format compatible with OpenAI's fine-tuning API (JSONL with messages array)"
        )
    
    def format_dataset(self, prompts: List[str], completions: Optional[List[str]] = None) -> Dict[str, Any]:
        data = []
        
        for i, prompt in enumerate(prompts):
            completion = completions[i] if completions and i < len(completions) else ""
            
            # OpenAI format with system, user, and assistant messages
            entry = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": completion}
                ]
            }
            data.append(entry)
        
        return {
            "format": "openai",
            "data": data
        }
    
    def get_sample_format(self) -> str:
        return """
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."}
  ]
}
"""

class LlamaAlpacaFormat(ModelFormatTemplate):
    """
    Format for LLaMA/Alpaca-style instruction tuning
    
    Format: JSON with instruction/input/output fields
    Example:
    {"instruction": "...", "input": "...", "output": "..."}
    """
    
    def __init__(self):
        super().__init__(
            name="LLaMA/Alpaca",
            description="Instruction-tuning format used by LLaMA, Alpaca (JSON with instruction/input/output)"
        )
    
    def format_dataset(self, prompts: List[str], completions: Optional[List[str]] = None) -> Dict[str, Any]:
        data = []
        
        for i, prompt in enumerate(prompts):
            completion = completions[i] if completions and i < len(completions) else ""
            
            # Try to extract instruction vs. input if possible
            instruction = prompt
            input_text = ""
            
            # If prompt contains special separator, try to split it
            if "\n\nInput:" in prompt:
                parts = prompt.split("\n\nInput:", 1)
                instruction = parts[0].strip()
                if instruction.startswith("Instruction:"):
                    instruction = instruction[12:].strip()
                input_text = parts[1].strip()
            
            entry = {
                "instruction": instruction,
                "input": input_text,
                "output": completion
            }
            data.append(entry)
        
        return {
            "format": "llama_alpaca",
            "data": data
        }
    
    def get_sample_format(self) -> str:
        return """
{
  "instruction": "Write a poem about the moon",
  "input": "",
  "output": "Silvery moon in night's embrace..."
}
"""

class MistralFormat(ModelFormatTemplate):
    """
    Format for Mistral models
    
    Format: JSONL with text field containing full conversation
    """
    
    def __init__(self):
        super().__init__(
            name="Mistral",
            description="Format for Mistral models (JSONL with conversation text)"
        )
    
    def format_dataset(self, prompts: List[str], completions: Optional[List[str]] = None) -> Dict[str, Any]:
        data = []
        
        for i, prompt in enumerate(prompts):
            completion = completions[i] if completions and i < len(completions) else ""
            
            # Format as a conversation
            entry = {
                "text": f"<s>[INST] {prompt} [/INST] {completion}</s>"
            }
            data.append(entry)
        
        return {
            "format": "mistral",
            "data": data
        }
    
    def get_sample_format(self) -> str:
        return """
{
  "text": "<s>[INST] What is the meaning of life? [/INST] The meaning of life is...</s>"
}
"""

class SimpleTextFormat(ModelFormatTemplate):
    """
    Simple text format for general use
    
    Format: JSONL with prompt and completion fields
    """
    
    def __init__(self):
        super().__init__(
            name="Simple Text",
            description="General-purpose format with prompt and completion fields (JSONL)"
        )
    
    def format_dataset(self, prompts: List[str], completions: Optional[List[str]] = None) -> Dict[str, Any]:
        data = []
        
        for i, prompt in enumerate(prompts):
            completion = completions[i] if completions and i < len(completions) else ""
            
            entry = {
                "prompt": prompt,
                "completion": completion
            }
            data.append(entry)
        
        return {
            "format": "simple_text",
            "data": data
        }
    
    def get_sample_format(self) -> str:
        return """
{
  "prompt": "What is machine learning?",
  "completion": "Machine learning is a branch of artificial intelligence..."
}
"""

class CustomFormat(ModelFormatTemplate):
    """
    Custom format defined by the user
    """
    
    def __init__(self, 
                format_func: Callable[[List[str], Optional[List[str]]], Dict[str, Any]],
                sample_format: str):
        super().__init__(
            name="Custom Format",
            description="User-defined custom format"
        )
        self.format_func = format_func
        self._sample_format = sample_format
    
    def format_dataset(self, prompts: List[str], completions: Optional[List[str]] = None) -> Dict[str, Any]:
        return self.format_func(prompts, completions)
    
    def get_sample_format(self) -> str:
        return self._sample_format

# Dictionary of available formatters
AVAILABLE_FORMATS = {
    "openai": OpenAIFormat(),
    "llama_alpaca": LlamaAlpacaFormat(),
    "mistral": MistralFormat(),
    "simple_text": SimpleTextFormat(),
}

def get_available_format_choices():
    """Get list of available format choices for UI"""
    choices = []
    for key, formatter in AVAILABLE_FORMATS.items():
        choices.append((f"{formatter.name} - {formatter.description}", key))
    choices.append(("Custom format", "custom"))
    return choices
