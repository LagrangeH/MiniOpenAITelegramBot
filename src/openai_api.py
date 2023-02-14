from pprint import pformat

import openai
from loguru import logger as log


def openai_request(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.2,    # TODO: add user control and random option
    )

    return response['choices'][0]['text']
