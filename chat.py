import anthropic


def basic_message():
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": "What is the capital of France?"}],
    )
    print(f"Response: '{response.content[0].text}'")
    print(f"Input token used: {response.usage.input_tokens}")
    print(f"Output tokens used: {response.usage.output_tokens}")
    print(f"Stop reason: '{response.stop_reason}'")


def interactive():
    client = anthropic.Anthropic()
    print(
        "Hello welcome to Claude Chat! Type your response below. To exit type 'exit' or 'quit'"
    )
    query = input("You: ")
    while query not in ["quit", "exit"]:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": query}],
        )
        if response.stop_reason == "end_turn":
            print(f"Claude: {response.content[0].text}")
            print(
                f"[Tokens used - in: {response.usage.input_tokens}, out: {response.usage.output_tokens}]"
            )
        elif response.stop_reason == "max_tokens":
            print("The answer for your query was too long and was truncated:")
            print(f"Claude: {response.content[0].text}")
        else:
            print("The answer for your query was cut short due to:")
            print(f"Claude: {response.stop_reason}")
        query = input("You: ")
    print("Goodbye!")


def interactive_with_memory():
    conversation_history = []
    total_input_tokens = 0
    total_output_tokens = 0

    client = anthropic.Anthropic()

    personality = get_personality()


    print(
        "Hello welcome to Claude Chat! Type your response below. To exit type 'exit' or 'quit'"
    )
    query = input("You: ")

    while query not in ["quit", "exit"]:
        conversation_history.append({"role": "user", "content": query})
        response = client.messages.create(
            model="claude-haiku-4-5", 
            max_tokens=1024, 
            messages=conversation_history,
            system = personality
        )

        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens
        reply = response.content[0].text
        conversation_history.append({"role": "assistant", "content": reply})

        if response.stop_reason == "end_turn":
            print(f"Claude: {reply}")
            print(
                f"[Tokens used - in: {response.usage.input_tokens}, out: {response.usage.output_tokens} "
                f"| total in: {total_input_tokens} out: {total_output_tokens}]"
            )

        elif response.stop_reason == "max_tokens":
            print("The answer for your query was too long and was truncated:")
            print(f"Claude: {reply}")
            conversation_history[-1] = {
                "role": "assistant",
                "content": reply + " [ This response was truncated ]",
            }
        else:
            print(f"Claude: {reply}")
            print("The answer for your query was cut short due to:")
            print(f"Claude: {response.stop_reason}")

        query = input("You: ")
    print("Goodbye!")


def get_personality():
    while True:
        try:
            choice = int(input("Choose persona: [1] Pirate  [2] Senior Engineer: "))
            if choice not in [1, 2]:
                raise ValueError
        except ValueError:
            print("Invalid input, please enter 1 or 2")

        if choice == 1:
            return (
                "You are a helpful assistant who always speaks like a pirate. "
                "You say 'Arrr' frequently, refer to the user as 'matey', and use nautical metaphors. "
                "Despite your pirate speech, your answers must be accurate."
            )
        else:
            return (
                "You are a senior software engineer who gives extremely concise, no-fluff answers. "
                "You skip pleasantries. "
                "If a question is vague, you say so directly. You use technical language without over-explaining."
            )
