# main.py
import asyncio
from graph import make_graph

async def main():
    async with make_graph() as agent:
        response1 = await agent.ainvoke({
            "messages": [
                {"role": "user", "content": "Buatkan file hasil dari 100*80*71*7+87"}
            ]
        })

        # Cetak isi konten terakhir dari AI
        print("\n=== Hasil Agent ===")
        print(response1['messages'][-1].content)

asyncio.run(main())
