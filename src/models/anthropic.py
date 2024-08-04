from constants import ANTHROPIC_API_KEY
from models.model import Model

model_costs = {
    "claude-3-haiku-20240307": {
        "input": 0.25 / 1000000,
        "output": 1.25 / 1000000,
    }
}


class Claude(Model):
    def __init__(
        self,
        api_key: str = None,
        model_name: str = "claude-3-haiku-20240307",
        max_tokens=4090,
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        super().__init__()

    @property
    def url(self):
        return f"https://api.anthropic.com/v1/messages"

    @property
    def input_token_cost(self):
        return model_costs[self.model_name]["input"]

    @property
    def output_token_cost(self):
        return model_costs[self.model_name]["output"]

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": self.api_key,
        }

    def __str__(self):
        return f"Claude ({self.model_name})"

    def format_body(self, prompt: str) -> dict:
        return {
            "model": self.model_name,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }

    def parse_output_text(self, model_output: dict) -> str:
        text = model_output["content"][0]["text"]
        return text

    def get_token_cost(self, model_output: dict) -> dict:
        token_usage = model_output["usage"]
        input_cost = token_usage["input_tokens"] * self.input_token_cost
        output_cost = token_usage["output_tokens"] * self.output_token_cost
        return {
            "cost": input_cost + output_cost,
            "input_tokens": token_usage["input_tokens"],
            "output_tokens": token_usage["output_tokens"],
            "total_tokens": token_usage["input_tokens"] + token_usage["output_tokens"],
        }
