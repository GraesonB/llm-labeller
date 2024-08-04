import asyncio
from constants import (
    ANTHROPIC_API_KEY,
    DEEPSEEK_API_KEY,
    GOOGLE_API_KEY,
    OPENAI_API_KEY,
)
from models import Claude, DeepSeek, Gemini, OpenAI
from prompts.korean_lemma_labeller import prompt
from rich import print
from utils import clean_text_simple
from utils import parse_tags

if __name__ == "__main__":

    async def main():
        gemini = Gemini(api_key=GOOGLE_API_KEY)
        deepseek = DeepSeek(api_key=DEEPSEEK_API_KEY)
        gpt4o = OpenAI(api_key=OPENAI_API_KEY)
        claude = Claude(api_key=ANTHROPIC_API_KEY)
        # sentence = "하교에 가고 있어"
        sentence = "낮에는 선장님! ☀️                       밤에는 가수다! 🌜"
        # sentence = "9점 이상을 쏘면 승리가 확정되는 상황, 김우진은 깨끗한 10점으로 금메달을 명중시켰습니다."

        for model in [gemini, deepseek, gpt4o, claude]:
            print(f"Model: {model}")
            output, usage, seconds = await model.label(
                prompt, {"sentence": clean_text_simple(sentence)}
            )
            print("Output:")
            print(parse_tags(output))
            print("Usage metrics:")
            print(usage)
            print(f"Seconds Taken: {seconds}")
            print("")

    asyncio.run(main())
