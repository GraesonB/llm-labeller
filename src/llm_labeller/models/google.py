from .model import Model

model_costs = {
    "gemini-1.5-flash": {
        "input": 0.075 / 1000000,
        "output": 0.3 / 1000000,
    }
}


class Gemini(Model):
    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        self.api_key = api_key
        super().__init__()

    @property
    def url(self):
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

    @property
    def input_token_cost(self):
        return model_costs[self.model_name]["input"]

    @property
    def output_token_cost(self):
        return model_costs[self.model_name]["output"]

    @property
    def headers(self):
        return {"Content-Type": "application/json"}

    def __str__(self):
        return f"Gemini ({self.model_name})"

    def format_body(self, prompt: str) -> dict:
        return {
            "contents": [{"parts": [{"text": prompt}]}],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ],
        }

    def parse_output_text(self, model_output: dict) -> str:
        text = model_output["candidates"][0]["content"]["parts"][0]["text"]
        return text

    def get_token_cost(self, model_output: dict) -> dict:
        token_usage = model_output["usageMetadata"]
        input_cost = token_usage["promptTokenCount"] * self.input_token_cost
        output_cost = token_usage["candidatesTokenCount"] * self.output_token_cost
        return {
            "cost": input_cost + output_cost,
            "input_tokens": token_usage["promptTokenCount"],
            "output_tokens": token_usage["candidatesTokenCount"],
            "total_tokens": token_usage["totalTokenCount"],
        }
