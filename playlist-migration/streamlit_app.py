# streamlit_app.py

import streamlit as st
from playlist_agent import extract_spotify, agent, create_ytmusic
import re

st.set_page_config(page_title="Playlist Migrator", page_icon="🎵")
st.title("🎧 Spotify ➡️ YouTube Music Migrator")

st.markdown("""
Masukkan link playlist Spotify kamu, lalu sistem akan memigrasikan lagu-lagunya ke YouTube Music.🎶
""")

# Input dari user
playlist_link = st.text_input("Masukkan Link Playlist Spotify")

if playlist_link:
    with st.spinner("🔍 Mengambil lagu dari Spotify..."):
        try:
            songs = extract_spotify(playlist_link)
        except Exception as e:
            st.error(f"Gagal mengambil playlist: {e}")
            st.stop()

    st.success(f"Berhasil mengambil {len(songs)} lagu dari Spotify!")
    st.markdown("---")

    matched_video_ids = []
    for song in songs:
        query = f"{song['title']} by {song['artist']}"
        st.write(f"🔍 Mencari: `{query}`")
        try:
            result = agent.invoke({"input": query})
            output = result["output"] if isinstance(result, dict) else result
            match = re.search(r"v=([a-zA-Z0-9_-]{11})", output)
            if match:
                matched_video_ids.append(match.group(1))
        except Exception as e:
            st.warning(f"Gagal mencari '{query}': {e}")

    if matched_video_ids:
        with st.spinner("📤 Membuat playlist di YouTube Music..."):
            try:
                playlist_url = create_ytmusic("Migrated from Spotify", matched_video_ids)
                st.success("✅ Playlist berhasil dibuat!")
                st.markdown(f"🔗 [Lihat di YouTube Music]({playlist_url})")
            except Exception as e:
                st.error(f"Gagal membuat playlist: {e}")
    else:
        st.error("Tidak ada lagu yang berhasil dimigrasikan.")
