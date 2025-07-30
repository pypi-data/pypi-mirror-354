from typing import Any, Dict, List, Union

from groq import Groq

from repenseai.utils.logs import logger

from repenseai.genai.providers import VISION_MODELS


class ChatAPI:
    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.1-8b-instant",
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

        self.response = None
        self.tokens = None

        self.tool_flag = False

        self.client = Groq(api_key=self.api_key)

    def __process_prompt_list(self, prompt: List[Dict[str, str]]) -> list:
        if self.model not in VISION_MODELS:
            for message in prompt:
                message["content"] = message.get("content", [{}])[0].get("text", "")

            return prompt
        else:
            for message in prompt:
                if message.get("role") == "assistant":
                    message["content"] = message.get("content", [{}])[0].get("text", "")

            return prompt

    def call_api(self, prompt: Union[List[Dict[str, str]], str]) -> None:
        json_data = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": self.stream,
        }

        if isinstance(prompt, list):
            json_data["messages"] = self.__process_prompt_list(prompt)
        else:
            json_data["messages"] = [{"role": "user", "content": prompt}]

        try:
            self.response = self.client.chat.completions.create(**json_data)

            if not self.stream:
                self.tokens = self.get_tokens()
                return self.get_output()

            return self.response

        except Exception as e:
            logger(f"Erro na chamada da API - modelo {json_data['model']}: {e}")

    def get_response(self) -> Any:
        return self.response

    def get_output(self) -> Union[None, str]:
        if self.response is not None:
            return self.response.model_dump()["choices"][0]["message"]["content"]
        else:
            return None

    def get_tokens(self) -> Union[None, str]:
        if self.response is not None:
            return self.response.model_dump()["usage"]
        else:
            return None

    def process_stream_chunk(self, chunk: Any) -> Union[str, None]:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                return content
            else:
                if chunk.model_dump().get("x_groq", {}).get("usage"):
                    self.tokens = chunk.model_dump()["x_groq"]["usage"]


class VisionAPI:
    def __init__(
        self,
        api_key: str,
        model: str = "",
        temperature: float = 0.0,
        max_tokens: int = 3500,
        stream: bool = False,
    ):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stream = stream

        self.response = None
        self.tokens = None

    def call_api(self, prompt: str, image: Any):
        _ = prompt
        _ = image

        return "Not Implemented"

    def get_output(self) -> Union[None, str]:
        if self.response is not None:
            return self.response.model_dump()["choices"][0]["message"]["content"]
        else:
            return None

    def get_tokens(self):
        return {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

    def process_stream_chunk(self, chunk: Any) -> Union[str, None]:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                return content
            else:
                if chunk.model_dump().get("x_groq", {}).get("usage"):
                    self.tokens = chunk.model_dump()["x_groq"]["usage"]


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
        self.api_key = api_key
        self.model = model

    def call_api(self, audio: Any):
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
