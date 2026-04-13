import chat
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Hello from claude-chat!")
    chat.interactive_full()


if __name__ == "__main__":
    main()
