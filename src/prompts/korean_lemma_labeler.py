prompt = """
You are tasked with lemmatizing a Korean sentence. Your goal is to identify the lemmas (base forms) of the words or meaningful phrases in the sentence and provide the corresponding original text found in the sentence.

Here is the Korean sentence you need to process:
<korean_sentence>
{sentence}
</korean_sentence>

Your output should be a JSON object with the following structure:
- An array containing a single object with two keys:
  1. **"original_sentence"**: The full original Korean sentence
  2. **"lemmatized_annotation"**: An array of objects, each representing a lemma found in the sentence

Each object in the "lemmatized_annotation" array should have:
- **"found"**: The exact original text (word or phrase) as it appears in the sentence, including any grammar particles attached to the word.
- **"lemma"**: The base form (lemma) of the word or phrase, excluding grammar particles.

Follow these steps to process the sentence:
1. Identify each meaningful word, phrase, or particle in the sentence.
2. For each identified word or phrase:
   a. Determine its lemma (base form).
   b. Extract the exact text as it appears in the original sentence, including any attached grammar particles.
   c. Create an object with the "found" and "lemma" information.
3. Add all created objects to the "lemmatized_annotation" array.

### Special Instructions
- **Include Content Words with Grammar Particles**: Include the entire segment from the sentence in the "found" entry, including any grammar particles (e.g., 은, 는, 이, 가, 을, 를, etc.). However, ensure the lemma corresponds only to the base form (excluding particles).
- **Combine Compound Words or Phrases**: For compound words or phrases that function as a single unit, treat them as one lemma and combine the entire phrase in the "found" entry. For example, "가고 있어요" should be treated as one unit with the lemma "가다." This applies to all types of verb/adjective conjugations. Only the lemma of the main verb/adjective should be included.
- **Consistency**: Ensure that the "found" entry accurately reflects the exact text in the sentence, and that the lemmas are consistently applied.

Format your response as a valid JSON object, ensuring all brackets, commas, and quotation marks are correctly placed. Wrap your entire output in <answer> tags.

<answer>
[
  {{
    "original_sentence": "{sentence}",
    "lemmatized_annotation": [
      {{ "found": "original_text_1", "lemma": "lemma_1" }},
      {{ "found": "original_text_2", "lemma": "lemma_2" }},
      ...
    ]
  }}
]
</answer>
"""
