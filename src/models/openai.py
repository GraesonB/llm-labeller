from constants import OPENAI_API_KEY
from models.model import Model

model_costs = {
    "gpt-4o-mini": {
        "input": 0.15 / 1000000,
        "output": 0.6 / 1000000,
    }
}


class OpenAI(Model):

    def __init__(self, api_key: str = None, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.api_key = api_key
        super().__init__()

    @property
    def url(self):
        return f"https://api.openai.com/v1/chat/completions"

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
            "Authorization": f"Bearer {self.api_key}",
        }

    def __str__(self):
        return f"OpenAI ({self.model_name})"

    def format_body(self, prompt: str) -> dict:
        return {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

    def parse_output_text(self, model_output: dict) -> str:
        text = model_output["choices"][0]["message"]["content"]
        return text

    def get_token_cost(self, model_output: dict) -> dict:
        token_usage = model_output["usage"]
        input_cost = token_usage["prompt_tokens"] * self.input_token_cost
        output_cost = token_usage["completion_tokens"] * self.output_token_cost
        return {
            "cost": input_cost + output_cost,
            "input_tokens": token_usage["prompt_tokens"],
            "output_tokens": token_usage["completion_tokens"],
            "total_tokens": token_usage["total_tokens"],
        }
