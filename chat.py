import anthropic
import os


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


def full_chat():
    try:
        conversation_history = []
        total_input_tokens = 0
        total_output_tokens = 0

        client = anthropic.Anthropic()

        personality = get_personality()
        temperature = get_temperature()
        max_tokens = get_max_tokens()

        print(
            "Hello welcome to Claude Chat! Type your response below. To exit type '/exit' or '/quit'\n" \
            "type /clear to clear the chat history\n" \
            "type /tokens to view the tokens usage"
        )
        query = input("You: ")
        response = None
        
        while query not in ["/quit", "/exit"]:
            if query == '/clear':
                conversation_history = []
                os.system('clear' if os.name == 'posix' else 'cls')
                query = input("You: ")
                continue

            if query == '/tokens':
                print_token_usage(response, total_input_tokens, total_output_tokens)
                query = input("You: ")
                continue

            conversation_history.append({"role": "user", "content": query})
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=max_tokens,
                messages=conversation_history,
                system=personality,
                temperature=temperature,
            )

            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens
            reply = response.content[0].text
            conversation_history.append({"role": "assistant", "content": reply})

            if response.stop_reason == "end_turn":
                print(f"Claude: {reply}")
                print_token_usage(response, total_input_tokens, total_output_tokens)

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
    except KeyboardInterrupt:
        print("\n\nGoodbye! (interrupted)")




def print_token_usage(response, total_input_tokens, total_output_tokens):
    if response:
        print(f"[Tokens used last response - in: {response.usage.input_tokens}, out: {response.usage.output_tokens} ]")
    else:
        print(f"[No messages sent yet]")
    print(f"[total in: {total_input_tokens} out: {total_output_tokens}]")


def get_personality():
    while True:
        options = {
            1: "You are a helpful assistant who always speaks like a pirate. "
            "You say 'Arrr' frequently, refer to the user as 'matey', and use nautical metaphors. "
            "Despite your pirate speech, your answers must be accurate.",
            2: "You are a senior software engineer who gives extremely concise, no-fluff answers. "
            "You skip pleasantries. "
            "If a question is vague, you say so directly. You use technical language without over-explaining.",
            3: "You are an extremely enthusiastic life coach who treats every question as a profound opportunity "
            "for personal growth. You use excessive exclamation marks, relate everything back to 'the journey', "
            "and somehow connect even mundane technical questions to self-actualization. Despite the energy, your answers must be accurate.",
            4: "You are a corporate lawyer who answers every question with excessive legal hedging. "
            "You preface statements with 'allegedly', add disclaimers to everything, "
            "and occasionally warn the user that your response does not constitute legal advice. "
            "Despite this, your actual answers are technically correct and useful."
        }
        try:
            choice = int(input("Choose persona: [1] Pirate  [2] Senior Engineer [3] Coach [4] Cautious Laywer: "))
            return options[choice]
        except (ValueError, KeyError):
            print("Invalid input, please select a valid option")
            continue

def get_temperature():
    while True:
        try:
            choice = input("Temperature (Values between 0.0 - 1.0), default = 0.7: ")
            if not choice:
                choice = 0.7
            choice = float(choice)
            if choice < 0.0 or choice > 1.0:
                raise ValueError

        except ValueError:
            print(
                "Invalid input, please enter a valid number between 0.0 - 1.0 or press enter for default 0.7"
            )
            continue

        return choice


def get_max_tokens():
    while True:
        try:
            choice = input("Max Tokens, default = 1024: ")
            if not choice:
                choice = 1024
            choice = int(choice)
            if choice < 0 or choice > 8192:
                raise ValueError

        except ValueError:
            print(
                "Invalid input, please enter a valid number between 0 - 8192 or press enter for default 1024"
            )
            continue

        return choice
