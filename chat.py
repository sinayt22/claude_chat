import anthropic

def basic_message():
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ]
    )
    print(f"Response: '{response.content[0].text}'")
    print(f"Input token used: {response.usage.input_tokens}")
    print(f"Output tokens used: {response.usage.output_tokens}")
    print(f"Stop reason: '{response.stop_reason}'")