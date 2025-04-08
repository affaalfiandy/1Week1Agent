from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from spotify_utils import extract_playlist as extract_spotify
from ytmusic_utils import search_song as ytmusic_search, create_playlist as create_ytmusic

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def search_song_tool(input: str):
    # Expecting input format: "<title> by <artist>"
    if " by " in input:
        title, artist = input.split(" by ", 1)
    else:
        raise ValueError("Invalid input format, expected '<title> by <artist>'")

    results = ytmusic_search(title.strip(), artist.strip())

    formatted = []
    for r in results:
        formatted.append({
            "videoId": r.get("videoId"),
            "title": r.get("title"),
            "artist": r.get("artist")
        })

    prompt = f"""
You are migrating a song from Spotify to YouTube Music.

Original Song:
Title: {title}
Artist: {artist}

Candidate Matches on YouTube Music:
{formatted}

Return ONLY the best videoId from the list above, or 'None' if unsure.
"""
    choice = llm.predict(prompt)
    return choice.strip().replace('"', '')

tools = [
    Tool(
        name="SearchSongTarget",
        func=search_song_tool,
        description="Searches song on YouTube Music using '<title> by <artist>' format string."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

if __name__ == "__main__":
    source_link = "https://open.spotify.com/playlist/0uDEzhu1q2g7znF65A9oe1"  # Replace with your link
    playlist_name = "Migrated Playlist by AI Agent"

    print("⏬ Extracting songs from Spotify...")
    songs = extract_spotify(source_link)

    matched_video_ids = []
    for song in songs:
        query = f"{song['title']} by {song['artist']}"
        print(f"🔍 Searching for: {query}")
        result = agent.invoke({"input": query})
        output = result["output"] if isinstance(result, dict) else result

        # Ekstrak videoId dari link YouTube
        import re
        match = re.search(r"v=([a-zA-Z0-9_-]{11})", output)
        if match:
            video_id = match.group(1)
            matched_video_ids.append(video_id)
        else:
            print(f"❌ No valid videoId found in: {output}")



    if matched_video_ids:
        print("📤 Creating playlist on YouTube Music...")
        print(matched_video_ids)
        playlist_url = create_ytmusic(playlist_name, matched_video_ids)
        print(f"✅ Playlist created: {playlist_url}")
    else:
        print("⚠️ No songs matched for migration.")
