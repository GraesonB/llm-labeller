import asyncio
from models.anthropic import ClaudeHaiku
from models.deepseek import DeepSeek
from models.google import Gemini
from models.openai import GPT4oMini
from prompts.korean_lemma_labeller import prompt
from rich import print
from utils.parse_response_tags import parse_tags

if __name__ == "__main__":

    async def main():
        gemini = Gemini()
        deepseek = DeepSeek()
        gpt4o = GPT4oMini()
        claude = ClaudeHaiku()
        # sentence = "하교에 가고 있어"
        sentence = "9점 이상을 쏘면 승리가 확정되는 상황, 김우진은 깨끗한 10점으로 금메달을 명중시켰습니다."

        for model in [gemini, deepseek, gpt4o, claude]:
            print(f"Model: {model}")
            output, usage, seconds = await model.label(prompt, {"sentence": sentence})
            print("Output:")
            print(parse_tags(output))
            print("Usage metrics:")
            print(usage)
            print(f"Seconds Taken: {seconds}")
            print("")

    asyncio.run(main())
