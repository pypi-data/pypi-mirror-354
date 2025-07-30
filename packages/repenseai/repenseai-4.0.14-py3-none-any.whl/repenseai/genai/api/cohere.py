from io import BufferedReader
from typing import Any, Union

from cohere import ClientV2
from repenseai.utils.logs import logger

from repenseai.genai.providers import VISION_MODELS


class ChatAPI:
    def __init__(
        self,
        api_key: str,
        model: str = "command-r-08-2024",
        temperature: float = 0.0,
        max_tokens: int = 3500,
        stream: bool = False,
        **kwargs,
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.max_tokens = max_tokens

        self.tool_flag = False

        self.response = None
        self.tokens = None

        self.client = ClientV2(api_key=self.api_key)

    def __process_prompt_list(self, prompt: list) -> list:

        if self.model not in VISION_MODELS:
            for history in prompt:
                content = history.get("content", [])

                if content[0].get("type") == "image_url":
                    prompt.remove(history)

        return prompt

    def call_api(self, prompt: list | str) -> None:
        json_data = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if isinstance(prompt, list):
            json_data["messages"] = self.__process_prompt_list(prompt)
        else:
            json_data["messages"] = [{"role": "user", "content": prompt}]

        try:
            if not self.stream:

                self.response = self.client.chat(**json_data)
                self.tokens = self.get_tokens()

                return self.get_output()

            self.response = self.client.chat_stream(**json_data)

            return self.response

        except Exception as e:
            logger(f"Erro na chamada da API - modelo {json_data['model']}: {e}")

    def get_response(self) -> Any:
        return self.response

    def get_output(self) -> Union[None, str]:
        if self.response is not None:
            return self.response.model_dump()["message"]["content"][0]["text"]
        else:
            return None

    def get_tokens(self) -> Union[None, str]:
        if self.response is not None:

            usage = self.response.model_dump()["usage"]

            prompt_tokens = usage["billed_units"]["input_tokens"]
            completion_tokens = usage["billed_units"]["output_tokens"]

            total_tokens = prompt_tokens + completion_tokens

            return {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            }
        else:
            return None

    def process_stream_chunk(self, chunk: Any) -> Union[str, None]:
        if chunk.type == "content-delta":
            return chunk.delta.message.content.text
        elif chunk.type == "message-end":
            usage = chunk.model_dump()["delta"]["usage"]["tokens"]

            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)

            self.tokens = {
                "completion_tokens": output_tokens,
                "prompt_tokens": input_tokens,
                "total_tokens": output_tokens + input_tokens,
            }


class VisionAPI:
    def __init__(
        self,
        api_key: str,
        model: str = "",
        temperature: float = 0.0,
        max_tokens: int = 3500,
        stream: bool = False,
    ):
        self.client = ClientV2(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.max_tokens = max_tokens

        self.response = None
        self.tokens = None

    def call_api(self, prompt: str, image: Any):
        _ = prompt
        _ = image

        return "Not Implemented"

    def get_output(self) -> Union[None, str]:
        if self.response is not None:
            return self.response.model_dump()["message"]["content"][0]["text"]
        else:
            return None

    def get_tokens(self):
        return {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

    def process_stream_chunk(self, chunk: Any) -> Union[str, None]:
        if chunk.type == "content-delta":
            return chunk.delta.message.content.text
        elif chunk.type == "message-end":
            usage = chunk.model_dump()["delta"]["usage"]["tokens"]

            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)

            self.tokens = {
                "completion_tokens": output_tokens,
                "prompt_tokens": input_tokens,
                "total_tokens": output_tokens + input_tokens,
            }


class ImageAPI:
    def __init__(self, api_key: str, model: str = "", **kwargs):
        self.api_key = api_key
        self.model = model

    def call_api(self, prompt: Any, image: Any):
        _ = image
        _ = prompt

        return self.get_output()

    def get_output(self):
        return "Not Implemented"

    def get_tokens(self):
        return {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}


class AudioAPI:
    def __init__(self, api_key: str, model: str, **kwargs):
        self.client = ClientV2(api_key=api_key)
        self.model = model

    def call_api(self, audio: BufferedReader):
        _ = audio

        return self.get_output()

    def get_output(self):
        return "Not Implemented"

    def get_tokens(self):
        return {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}


class SpeechAPI:
    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model

    def call_api(self, text: str) -> bytes:
        _ = text

        return self.get_output()

    def get_output(self):
        return "Not Implemented"

    def get_tokens(self):
        return 0
