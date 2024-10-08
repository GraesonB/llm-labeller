from abc import ABC, abstractmethod
import json
import time
from typing import Dict, List, Union
from aiohttp import ClientSession
from rich import print
from llm_labeller.utils.tag_extraction import extract_tags
from llm_labeller.prompt import Prompt


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

    async def invoke(
        self, prompt: Prompt, input_parameters: Dict[str, str]
    ) -> Union[Dict, List, str]:
        body = self.format_body(prompt.render(input_parameters))

        async with ClientSession(headers=self.headers) as session:
            start = time.time()
            res = await session.post(self.url, json=body)
            if res.status == 429:
                raise Exception(f"({self}): Rate limited")
            elif res.status == 401:
                if hasattr(self, "update_api_key"):
                    print(f"({self}): Unauthorized, updating API key...")
                    self.update_api_key()
                    return await self.invoke(prompt)
                else:
                    raise Exception(f"({self}): Unauthorized")
            res_json = await res.json()
            end = time.time()

        text = self.parse_output_text(res_json)
        token_usage = self.get_token_cost(res_json)
        seconds = end - start

        if prompt.output_type == "json":
            try:
                output = json.loads(extract_tags(text)[prompt.output_field])
            except json.JSONDecodeError:
                print(f"({self}): Failed to parse JSON output: {text}")
        else:
            output = extract_tags(text)[prompt.output_field]

        return {
            "output": output,
            "token_usage": token_usage,
            "seconds": seconds,
        }
