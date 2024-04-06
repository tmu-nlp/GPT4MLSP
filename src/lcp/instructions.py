instruction_for_lcp_with_role_lang = """
You are an individual without specialized knowledge or expertise in a specific area.

You will be given a sentence and a word included in the sentence.

Your task is to rate the word on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.


Evaluation Criteria:

Complexity (0.0, 0.25, 0.5, 0.75, 1.0): the complexity of a word in terms of how difficult the word is to understand.

Evaluation steps:
1. Read the sentence and word carefully to understand the context.
2. Determine the complexity of the word based on the following criteria:
   - 0.0: The word is simple and easily understandable to most people.
   - 0.25: The word may have some complexity or be specific to a certain field, but can still be understood with some effort.
   - 0.5: The word is moderately complex and may require some background knowledge or explanation to understand fully.
   - 0.75: The word is quite complex and may be difficult to understand without significant knowledge or explanation.
   - 1.0: The word is extremely complex and likely only understood by experts or individuals with specialized knowledge.
3. Assign a complexity rating to the word.

Note: Your own familiarity with a word should not impact your rating. This should be based on an average person's understanding of the word.

Please assign a complexity rating to the '{{lang}}' word.

Sentence: '{{sentence}}'

Word: '{{token}}'

Complexity:
"""

instruction_for_lcp_with_lang = """
You will be given a sentence and a word included in the sentence.

Your task is to rate the word on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.


Evaluation Criteria:

Complexity (0.0, 0.25, 0.5, 0.75, 1.0): the complexity of a word in terms of how difficult the word is to understand.

Evaluation steps:
1. Read the sentence and word carefully to understand the context.
2. Determine the complexity of the word based on the following criteria:
   - 0.0: The word is simple and easily understandable to most people.
   - 0.25: The word may have some complexity or be specific to a certain field, but can still be understood with some effort.
   - 0.5: The word is moderately complex and may require some background knowledge or explanation to understand fully.
   - 0.75: The word is quite complex and may be difficult to understand without significant knowledge or explanation.
   - 1.0: The word is extremely complex and likely only understood by experts or individuals with specialized knowledge.
3. Assign a complexity rating to the word.

Please assign a complexity rating to the '{{lang}}' word

Sentence: '{{sentence}}'

Word: '{{token}}'

Complexity:
"""

instruction_for_lcp_with_role = """
You are an individual without specialized knowledge or expertise in a specific area.

You will be given a sentence and a word included in the sentence.

Your task is to rate the word on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.


Evaluation Criteria:

Complexity (0.0, 0.25, 0.5, 0.75, 1.0): the complexity of a word in terms of how difficult the word is to understand.

Evaluation steps:
1. Read the sentence and word carefully to understand the context.
2. Determine the complexity of the word based on the following criteria:
   - 0.0: The word is simple and easily understandable to most people.
   - 0.25: The word may have some complexity or be specific to a certain field, but can still be understood with some effort.
   - 0.5: The word is moderately complex and may require some background knowledge or explanation to understand fully.
   - 0.75: The word is quite complex and may be difficult to understand without significant knowledge or explanation.
   - 1.0: The word is extremely complex and likely only understood by experts or individuals with specialized knowledge.
3. Assign a complexity rating to the word.

Note: Your own familiarity with a word should not impact your rating. This should be based on an average person's understanding of the word.

Sentence: '{{sentence}}'

Word: '{{token}}'

Complexity:
"""


instruction_for_lcp = """
You will be given a sentence and a word included in the sentence.

Your task is to rate the word on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.


Evaluation Criteria:

Complexity (0.0, 0.25, 0.5, 0.75, 1.0): the complexity of a word in terms of how difficult the word is to understand.

Evaluation steps:
1. Read the sentence and word carefully to understand the context.
2. Determine the complexity of the word based on the following criteria:
   - 0.0: The word is simple and easily understandable to most people.
   - 0.25: The word may have some complexity or be specific to a certain field, but can still be understood with some effort.
   - 0.5: The word is moderately complex and may require some background knowledge or explanation to understand fully.
   - 0.75: The word is quite complex and may be difficult to understand without significant knowledge or explanation.
   - 1.0: The word is extremely complex and likely only understood by experts or individuals with specialized knowledge.
3. Assign a complexity rating to the word.

Sentence: '{{sentence}}'

Word: '{{token}}'

Complexity:
"""
