"""
Main Jarvis assistant loop.
"""

from core.router import Router


class Assistant:

    def __init__(self):
        self.running = True
        self.router = Router()

    def start(self):

        print("🤖 Jarvis is online.\n")

        while self.running:

            try:
                command = input("Jarvis > ").strip()

            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                break

            if not command:
                continue

            if command.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                self.running = False
                break

            print("\n🤖 Thinking...\n")

            response = self.router.route(command)

            if response:
                print(response)

            print()