from json import JSONDecodeError
from typing import Type, TypeVar
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
import json

T = TypeVar('T', bound=BaseModel)

def deeper_validate(raw: BaseMessage, format_model: Type[T]) -> T:
    """
    Validate the raw message and return a pydantic model.
    """
    try:
        return format_model.model_validate(raw)
    except Exception as e:
        if 'Invalid json output' not in str(e):
            raise e
    
        _errored_response = str(e)
        first_brace = _errored_response.find('{')
        if first_brace == -1:
            raise e
        
        last_brace = _errored_response.rfind('}')
        if last_brace == -1 and _errored_response[-1] != '}':
            raise e
        
        if first_brace >= last_brace:
            raise e

        json_content = _errored_response[first_brace:last_brace + 1]

        parsed_json = json.loads(json_content)
        return format_model.model_validate(parsed_json)