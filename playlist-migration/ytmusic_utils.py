from ytmusicapi import YTMusic

ytmusic = YTMusic("browser.json")

def search_song(title: str, artist: str):
    query = f"{title} {artist}"
    search_results = ytmusic.search(query, filter="songs", limit=5)

    formatted = []
    for r in search_results:
        formatted.append({
            "videoId": r.get("videoId"),
            "title": r.get("title"),
            "artist": r.get("artists", [{}])[0].get("name")
        })
    return formatted

def create_playlist(name: str, video_ids: list):
    playlist_id = ytmusic.create_playlist(name, description="Migrated playlist")
    ytmusic.add_playlist_items(playlist_id, video_ids)
    return f"https://music.youtube.com/playlist?list={playlist_id}"
