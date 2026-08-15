import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llama_index.core.workflow import Context
from src.agent import build_agent

async def main() -> None:
    print("=" * 60)
    print(" Ask My Company - Internal Policy Assistant")
    print("=" * 60)
    print("Loading model and Index ...\n")

    agent = build_agent()
    ctx = Context(agent)

    print("Ready! Ask about vacation, expenses, remote work, sick leave,")
    print("onboarding, purchasing, or IT support. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            response = await agent.run(question, ctx=ctx)
            print(f"\nAgent: {response}\n")
        except Exception as exc:
            print(f"\n[Error] {exc}\n")

if __name__ == "__main__":
    asyncio.run(main())