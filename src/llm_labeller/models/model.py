from abc import ABC, abstractmethod
import time
from aiohttp import ClientSession
from rich import print


class Model(ABC):
    def __init__(self):
        if not self.api_key:
            raise ValueError(f"({self}) API key must be set.")

    @property
    @abstractmethod
    def url(self):
        pass

    @property
    @abstractmethod
    def input_token_cost(self):
        pass

    @property
    @abstractmethod
    def output_token_cost(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def format_body(self, prompt: str) -> dict:
        pass

    @abstractmethod
    def get_token_cost(self, model_output: dict) -> dict:
        pass

    @abstractmethod
    def parse_output_text(self, model_output: dict) -> dict:
        pass

    async def label(self, prompt: str, prompt_params: dict) -> str:
        formatted_prompt = prompt.format(**prompt_params)
        body = self.format_body(formatted_prompt)

        async with ClientSession(headers=self.headers) as session:
            start = time.time()
            res = await session.post(self.url, json=body)
            if res.status == 429:
                raise Exception(f"({self}): Rate limited")
            elif res.status == 401:
                if hasattr(self, "update_api_key"):
                    print(f"({self}): Unauthorized, updating API key...")
                    self.update_api_key()
                    return await self.label(prompt, prompt_params)
                else:
                    raise Exception(f"({self}): Unauthorized")
            res_json = await res.json()
            end = time.time()

        text = self.parse_output_text(res_json)
        token_usage = self.get_token_cost(res_json)
        seconds = end - start

        return text, token_usage, seconds
