from typing import Union, List
import json

from litellm.types.utils import ModelResponse

from litellm import completion, RateLimitError
from pydantic import BaseModel
from traceback_with_variables import format_exc

from sweetagent.core import RotatingList, LLMChatMessage
from sweetagent.io.base import BaseStaIO


class LLMClient:
    def __init__(
        self,
        provider: str,
        model: str,
        api_keys_rotator: Union[list, RotatingList],
        stdio: BaseStaIO,
        base_url: str = None,
    ):
        self.provider = provider
        self.model = model
        self.api_keys_rotator: RotatingList = (
            api_keys_rotator
            if isinstance(api_keys_rotator, RotatingList)
            else RotatingList(api_keys_rotator)
        )
        self.sta_stdio: BaseStaIO = stdio
        self.base_url: str = base_url

    def complete(
        self, messages: List[dict], tools: List[dict], **completion_kwargs
    ) -> LLMChatMessage:
        self.sta_stdio.log_debug(
            f"Using {self.base_url = } Sending {json.dumps(messages, indent=4)}"
        )

        last_error = None
        try:
            for i in range(self.api_keys_rotator.max_iter):
                try:
                    resp: ModelResponse = completion(
                        model=f"{self.provider}/{self.model}",
                        api_key=self.api_keys_rotator.current,
                        base_url=self.base_url,
                        temperature=completion_kwargs.pop("temperature", 0),
                        messages=messages,
                        tools=tools,
                        response_format=completion_kwargs.pop(
                            "response_format",
                            self.find_user_last_message_format(messages),
                        ),
                        **completion_kwargs,
                    )
                    break
                except RateLimitError as e:
                    last_error = e
                    self.api_keys_rotator.next()
            else:
                raise last_error

            llm_message = LLMChatMessage.from_model_response(resp)
            self.sta_stdio.log_debug(str(llm_message))

            if llm_message.content:
                parts = llm_message.content.split("</think>", maxsplit=1)
                if len(parts) == 1:
                    content = parts[0]
                else:
                    content = parts[1]

                llm_message.content = content

            return llm_message
        except Exception as e:
            self.sta_stdio.log_error(format_exc(e))

    def find_user_last_message_format(
        self, messages: List[dict]
    ) -> Union[dict, BaseModel, None]:
        for message in reversed(messages):
            if message["role"] == "user":
                return message.get("response_format")
