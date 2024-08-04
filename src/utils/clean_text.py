import re


def clean_text(text):
    # Remove emojis and special characters
    cleaned_text = re.sub(r"[^\w\sㄱ-ㅎ가-힣]", "", text)
    # Reduce multiple spaces to a single space
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    # Strip leading and trailing spaces
    cleaned_text = cleaned_text.strip()
    return cleaned_text
