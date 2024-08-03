prompt = """
You are tasked with lemmatizing a Korean sentence. Your goal is to identify the lemmas (base forms) of the words in the sentence and provide their spans in the original text.

Here is the Korean sentence you need to process:
<korean_sentence>
{sentence}
</korean_sentence>

Your output should be a JSON object with the following structure:
- An array containing a single object with two keys:
  1. "original_sentence": The full original Korean sentence
  2. "lemmatized_annotation": An array of objects, each representing a lemma found in the sentence

Each object in the "lemmatized_annotation" array should have:
- "span": A two-element array indicating the start and end indices of the word in the original sentence
- "lemma": The base form (lemma) of the word

Follow these steps to process the sentence:
1. Identify each meaningful word or particle in the sentence.
2. For each identified word:
   a. Determine its lemma (base form).
   b. Find its start and end indices in the original sentence.
   c. Create an object with the "span" and "lemma" information.
3. Add all created objects to the "lemmatized_annotation" array.

Special cases to consider:
- Include only content words (nouns, verbs, adjectives, adverbs) and significant particles.
- Exclude spaces and punctuation marks from the lemmatization process.
- Exclude grammar particles from the lemmatization process.
- For compound words or phrases that function as a single unit, treat them as one lemma. *THIS ONE IS REALLY IMPORTANT

Format your response as a valid JSON object, ensuring all brackets, commas, and quotation marks are correctly placed. Wrap your entire output in <answer> tags.

<answer>
[
  {{
    "original_sentence": "{sentence}",
    "lemmatized_annotation": [
      {{ "span": [start_index, end_index], "lemma": "lemma_1" }},
      {{ "span": [start_index, end_index], "lemma": "lemma_2" }},
      ...
    ]
  }}
]
</answer>
"""
