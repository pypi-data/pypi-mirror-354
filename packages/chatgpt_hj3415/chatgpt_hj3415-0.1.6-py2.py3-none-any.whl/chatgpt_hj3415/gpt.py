from openai import OpenAI
from typing import Iterator

def call_stream(messages: list[dict], temperature=0.7, response_format="text") -> Iterator[str]:
    """
    chunk 하나를 GPT에 보내고 생성되는 토큰을 delta 단위로 yield.
    마지막 yield 후 StopIteration.value 로 full_answer 반환.
    """
    client = OpenAI()

    full = ""
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=temperature,
        stream=True,
        # response_format={"type": "json_object"},
        response_format={"type": response_format},
    )

    for piece in stream:
        delta = piece.choices[0].delta.content
        if delta:
            full += delta
            yield delta  # <─ 여기서 즉시 전달

        if piece.choices[0].finish_reason and piece.choices[0].finish_reason != "length":
            break

    return full  # StopIteration.value

