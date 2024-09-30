import re


def extract_tags(text):
    pattern = re.compile(r"<(\w+)>\s*(.*?)\s*</\1>", re.DOTALL)
    matches = pattern.findall(text)
    result = {tag: content.strip() for tag, content in matches}
    return result
