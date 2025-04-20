# main.py
import asyncio
from graph import make_graph

async def main():
    async with make_graph() as agent:
        response1 = await agent.ainvoke({
            "messages": [
                {"role": "user", "content": "Create file for me to save result print This code works"}
            ]
        })

        # Cetak isi konten terakhir dari AI
        print("\n=== Hasil Agent ===")
        print(response1['messages'][-1].content)

asyncio.run(main())
