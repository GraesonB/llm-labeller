from constants import OPENAI_API_KEY
from models.model import Model


class GPT4oMini(Model):
    @property
    def url(self):
        return f"https://api.openai.com/v1/chat/completions"

    @property
    def input_token_cost(self):
        return 0.15 / 1000000

    @property
    def output_token_cost(self):
        return 0.6 / 1000000

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }

    def __str__(self):
        return "GPT 4o Mini"

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
