from .model import Model

model_costs = {
    "deepseek-chat": {
        "input": 0.14 / 1000000,
        "input_cache": 0.014 / 1000000,
        "output": 0.28 / 1000000,
    }
}


class DeepSeek(Model):

    def __init__(self, api_key: str = None, model_name: str = "deepseek-chat"):
        self.model_name = model_name
        self.api_key = api_key
        super().__init__()

    @property
    def url(self):
        return f"https://api.deepseek.com/chat/completions"

    @property
    def input_token_cost(self):
        return model_costs[self.model_name]["input"]

    @property
    def input_cache_hit_cost(self):
        return model_costs[self.model_name]["input_cache"]

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
        return f"DeepSeek ({self.model_name})"

    def format_body(self, prompt: str) -> dict:
        return {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }

    def parse_output_text(self, model_output: dict) -> str:
        text = model_output["choices"][0]["message"]["content"]
        return text

    def get_token_cost(self, model_output: dict) -> dict:
        token_usage = model_output["usage"]
        input_cost = token_usage["prompt_tokens"] * self.input_token_cost
        input_cache_hit_cost = (
            token_usage["completion_tokens"] * self.input_cache_hit_cost
        )
        output_cost = token_usage["completion_tokens"] * self.output_token_cost
        return {
            "cost": input_cost + output_cost + input_cache_hit_cost,
            "input_tokens": token_usage["prompt_tokens"],
            "output_tokens": token_usage["completion_tokens"],
            "total_tokens": token_usage["total_tokens"],
        }
