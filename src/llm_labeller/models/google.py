import asyncio
import json
import time
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from llm_labeller.utils.parse_response_tags import parse_tags
from .model import Model

model_costs = {
    "gemini-1.5-flash": {
        "input": 0.075 / 1000000,
        "output": 0.3 / 1000000,
    },
    "gemini-1.5-pro": {
        "input": 3.5 / 1000000,
        "output": 7 / 1000000,
    },
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


class GeminiTuned(Gemini):
    def __init__(
        self,
        model_name: str,
        client_cred_path: str,
        temperature: float = 0,
    ):
        self.credentials = Credentials.from_authorized_user_file(
            client_cred_path,
            ["https://www.googleapis.com/auth/generative-language.retriever"],
        )
        self.token_expiry = None
        self.api_key = self._get_bearer_token()

        super().__init__(
            api_key=self.api_key,
            model_name=model_name,
            temperature=temperature,
        )

    @property
    def url(self):
        return f"https://generativelanguage.googleapis.com/v1beta/tunedModels/{self.model_name}:generateContent"

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    @property
    def input_token_cost(self):
        return model_costs["gemini-1.5-flash"]["input"]

    @property
    def output_token_cost(self):
        return model_costs["gemini-1.5-flash"]["output"]

    def _get_bearer_token(self):
        if not self.token_expiry or time.time() > self.token_expiry:
            self.credentials.refresh(Request())
            self.token_expiry = self.credentials.expiry.timestamp()
        return self.credentials.token

    def update_api_key(self):
        self.api_key = self._get_bearer_token()


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

    def format_body(self, prompt: str) -> dict:
        return {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
            ],
            "generationConfig": {"temperature": self.temperature},
        }


if __name__ == "__main__":
    from rich import print

    gemini = GeminiTuned(
        "testcsv-ifg27kjo4ctj",
        "/Users/graesonbergen/creds.json",
    )

    prompt = """
You are tasked with lemmatizing a Korean sentence. Your goal is to return the lemmas of each word while following specific rules for handling verb conjugations and grammar particles.

Here is the Korean sentence to lemmatize:
<korean_sentence>
{sentence}
</korean_sentence>

Follow these rules when lemmatizing:
1. For verb conjugations, only return the lemma of the main verb. Do not include auxiliary verbs or conjugation endings as separate lemmas.
2. Identify each word or phrase in the sentence and provide its corresponding lemma.
3. In the 'found' field, the word should be included as found in the text (including verb conjugations and particles), and the 'lemma' field should only include the lemma following the rules above.
4. Ignore special characters, punctation, and non-Korean text (this includes abreviations of organizations, names, etc.).

When handling verb conjugations like "-고 있다", return only the lemma of the main verb. For example, "가고 있어" should be lemmatized to "가다", not "가다" and "있다" separately.

Format your response as a valid JSON object, ensuring all brackets, commas, and quotation marks are correctly placed. Wrap your entire output in <answer> tags.

Example response for input "학교에 가고 있어":
<answer>
{{
    "original_sentence": "학교에 가고 있어",
    "lemmatized_annotation": [
      {{ "found": "학교에", "lemma": "학교" }},
      {{ "found": "가고 있어", "lemma": "가다" }}
    ]
}}
</answer>


Now, please lemmatize the given Korean sentence and provide the result in the specified format.
"""

    async def main():

        output, _, _ = await gemini.label(
            prompt,
            {
                "sentence": "이재명 대통령 당선을 저지했다는 것만으로도 윤석열 정부가 해야 할 일들을 다 했다고 자위하는 이들의 커밍아웃은 오늘도 계속되고 있다. 그런 사람들의 특징이 교조적으로 어떤 면에서는 단정적으로 그리고 상대를 하대하는 듯한 말투로 이야기하지"
            },
        )

        print(parse_tags(output, json_output=True)["answer"])

    asyncio.run(main())
