"""
A collection of utilities for Python.
"""

# Import all public functions and classes
from .decorators import retry, forever
from .anthropic_ext import call_claude
from .langchain_ext import (
    call_gpt_with_prompt_model,
    call_gpt,
)

# Define what gets exported when using "from nael_utils import *"
__all__ = [
    "retry",
    "forever", 
    "call_claude",
    "call_gpt_with_prompt_model",
    "call_gpt",
]

__version__ = "0.1.8"
