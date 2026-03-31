import chat
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Hello from claude-chat!")
    chat.basic_message()


if __name__ == "__main__":
    main()
