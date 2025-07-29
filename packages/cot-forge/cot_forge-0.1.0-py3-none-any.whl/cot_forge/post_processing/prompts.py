

NATURAL_LANGUAGE_COT_PROMPT = """<Thought Process>
{Thought_Process}
</Thought Process>

<Question>
{Question}
</Question>

The <Thought Process> above reflects a large language model's reasoning based on the <Question>. Your task is to
rewrite the <Thought Process> to resemble a more human-like, intuitive natural thinking process. The new
version should:
1. Be presented as step-by-step reasoning, with each thought on a new line separated by a line break.
2. Avoid structured titles or formatting, focusing on natural transitions. Use casual and natural language for
transitions or validations, such as "hmm," "oh," "also," "actually," or "wait."
3. Expand the content, making the reasoning richer, more detailed, and logically clear while still being
conversational and intuitive."""

NATURAL_LANGUAGE_FORMAT_PROMPT = """### Output Format:
In your response, follow the JSON structure below with they key 'NaturalReasoning'.
Ensure that the value for 'NaturalReasoning' is a single, valid JSON string. 
Any newlines or special characters (like quotes) within this string must be properly escaped (e.g., use \\n for newlines, \\" for quotes).
```json
{"NaturalReasoning": "<INSERT_NATURAL_LANGUAGE_REASONING_HERE>"}
```"""


def build_natural_language_cot_prompt(
    question: str,
    cot: list[dict],
) -> str:
  """
  Build the natural language chain of thought prompt.

  Args:
      question (str): The question to be answered.
      cot (list[dict]): The chain of thought to be reformatted.

  Returns:
      str: The formatted prompt.
  """
  prompt = NATURAL_LANGUAGE_COT_PROMPT.format(
      Thought_Process=str(cot),
      Question=question
  ) + '\n\n' + NATURAL_LANGUAGE_FORMAT_PROMPT
  return prompt


FORMAL_RESPONSE_PROMPT = """<Thinking>
{natural_reasoning}
</Thinking>

<Question>
{question}
</Question>

The <Thinking> tags represents your internal thoughts about the <Question>. Based on this, generate
a rich and high-quality final response to the user. If there is a clear answer, provide it first. Ensure your
final response closely follows the <Question>. Output only your final response, without any additional content.
"""


def build_formal_answer_prompt(
    question: str,
    natural_reasoning: str,
) -> str:
  """
  Build the formal answer prompt.

  Args:
      question (str): The question to be answered.
      natural_reasoning (str): The natural reasoning process.

  Returns:
      str: The formatted prompt.
  """
  return FORMAL_RESPONSE_PROMPT.format(
      question=question,
      natural_reasoning=natural_reasoning,
  )
