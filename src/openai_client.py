from openai import OpenAI


# Important Note: This following is openai implementation which can be used in real world scenarios.
async def ask_openai(prompt, model="gpt-3.5-turbo", max_tokens=150) -> str:
    client = OpenAI()

    completion = client.chat.completions.create(
        model=model,
        messages=[
                {"role": "system", "content": "can you help me with my queries?"},
                {"role": "user", "content": prompt}
            ]
    )

    # print(completion.choices[0].message)
    return str(completion.choices[0].message)