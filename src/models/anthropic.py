from constants import ANTHROPIC_API_KEY
from models.model import Model


class ClaudeHaiku(Model):
    @property
    def url(self):
        return f"https://api.anthropic.com/v1/messages"

    @property
    def input_token_cost(self):
        return 0.25 / 1000000

    @property
    def output_token_cost(self):
        return 1.25 / 1000000

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": ANTHROPIC_API_KEY,
        }

    def __str__(self):
        return "Claude 3 Haiku"

    def format_body(self, prompt: str) -> dict:
        return {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 4096,
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
