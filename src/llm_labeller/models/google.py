import asyncio
import json
import time
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from .model import Model

model_costs = {
    "gemini-1.5-flash": {
        "input": 0.075 / 1000000,
        "output": 0.3 / 1000000,
    }
}


class Gemini(Model):
    def __init__(
        self,
        api_key: str = None,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0,
    ):
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
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
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
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
            "generationConfig": {"temperature": self.temperature},
        }

    def parse_output_text(self, model_output: dict) -> str:
        try:
            text = model_output["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError as e:
            print(f"Error parsing output: {e}")
            print(f"Output: {model_output}")
            raise e

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


class GeminiGCP(Gemini):
    def __init__(
        self,
        project_id: str,
        location: str,
        service_account_key_path: str,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0,
    ):
        self.project_id = project_id
        self.location = location
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.token_expiry = None
        self.api_key = self._get_bearer_token()

        super().__init__(
            model_name=model_name, temperature=temperature, api_key=self.api_key
        )

    @property
    def url(self):
        return f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}:generateContent"

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _get_bearer_token(self):
        if not self.token_expiry or time.time() > self.token_expiry:
            self.credentials.refresh(Request())
            self.token_expiry = self.credentials.expiry.timestamp()
        return self.credentials.token

    def update_api_key(self):
        self.api_key = self._get_bearer_token()
