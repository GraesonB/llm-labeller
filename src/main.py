import asyncio
from models.deepseek import DeepSeek
from models.google import Gemini
from models.openai import GPT4oMini
from prompts.korean_lemma_labeler import prompt
from rich import print


if __name__ == "__main__":

    async def main():
        gemini = Gemini()
        deepseek = DeepSeek()
        gpt4o = GPT4oMini()
        sentence = "하교에 가고 있어"

        output, usage, seconds = await gemini.label(prompt, {"sentence": sentence})
        print("GEMINI:")
        print(output)
        print(usage)
        print(seconds)
        print("")
        output, usage, seconds = await deepseek.label(prompt, {"sentence": sentence})
        print("DeepSeek:")
        print(output)
        print(usage)
        print(seconds)
        print("")
        output, usage, seconds = await gpt4o.label(prompt, {"sentence": sentence})
        print("GPT 4o:")
        print(output)
        print(usage)
        print(seconds)
        print("")

    asyncio.run(main())
