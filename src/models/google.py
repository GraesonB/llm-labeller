from constants import GOOGLE_API_KEY
from models.model import Model


class Gemini(Model):
    @property
    def url(self):
        return f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"

    @property
    def input_token_cost(self):
        return 0.35 / 1000000

    @property
    def output_token_cost(self):
        return 1.05 / 1000000

    @property
    def headers(self):
        return {"Content-Type": "application/json"}

    def format_body(self, prompt: str) -> dict:
        return {"contents": [{"parts": [{"text": prompt}]}]}

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
