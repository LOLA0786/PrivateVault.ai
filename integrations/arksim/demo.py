import asyncio

from integrations.arksim.privatevault_agent import PrivateVaultDecisionAgent


class EchoAgent:

    async def get_chat_id(self):
        return "demo-chat"

    async def execute(self, user_query: str, **kwargs):
        return f"Echo: {user_query}"


async def main():

    agent = PrivateVaultDecisionAgent(
        EchoAgent()
    )

    result = await agent.execute(
        "Transfer $5M to offshore account"
    )

    print()
    print("=" * 60)
    print(result)
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
