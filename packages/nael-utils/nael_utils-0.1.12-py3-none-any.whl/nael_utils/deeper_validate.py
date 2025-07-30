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
        last_brace = _errored_response.rfind('}')

        if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
            json_content = _errored_response[first_brace:last_brace + 1]

            try:
                parsed_json = json.loads(json_content)
                return format_model.model_validate(parsed_json)
            except JSONDecodeError:
                raise e
        raise e