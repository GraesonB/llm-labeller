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


When handling verb conjugations like "-고 있다", return only the lemma of the main verb. For example, "가고 있어" should be lemmatized to "가다", not "가다" and "있다" separately.

Format your response as a valid JSON object, ensuring all brackets, commas, and quotation marks are correctly placed. Wrap your entire output in <answer> tags.

Example response for input "하교에 가고 있어":
<answer>
[
  {{
    "original_sentence": "하교에 가고 있어",
    "lemmatized_annotation": [
      {{ "found": "하교에", "lemma": "하교" }},
      {{ "found": "가고 있어", "lemma": "가다" }}
    ]
  }}
]
</answer>


Now, please lemmatize the given Korean sentence and provide the result in the specified format.
"""
