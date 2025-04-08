# 🎧 Playlist Migrator: Spotify ➡️ YouTube Music

A simple Python + Streamlit project to migrate a Spotify playlist into YouTube Music using LLM and LangChain agent.

---

## 🚀 Features
- Extracts playlist tracks from Spotify
- Searches best match on YouTube Music
- Uses LLM (GPT-4) to choose best match
- Creates a new YouTube Music playlist with the matched songs
- Simple web UI with Streamlit

---

## 🛠 Requirements
```bash
Python >= 3.8
```
Install dependencies:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Setup

### 1. Create `.env` file in the project root:
```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8080
```

> Make sure you register the redirect URI at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)

### 2. Get YouTube Music Auth Headers:
Open Chrome and go to [https://music.youtube.com](https://music.youtube.com), login, open DevTools, and copy:
- `Cookie`
- `User-Agent`

Create a file `headers_auth.json`:
```json
{
  "Cookie": "...",
  "User-Agent": "...",
  "Accept": "*/*",
  "Accept-Language": "en-US,en;q=0.9"
}
```

Save it in the project root.

---

## ▶️ Running the App
```bash
streamlit run streamlit_app.py
```

Open in browser: [http://localhost:8501](http://localhost:8501)

---

## 🧠 Powered by
- [LangChain](https://www.langchain.com/)
- [OpenAI GPT-4](https://platform.openai.com/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [ytmusicapi](https://github.com/sigma67/ytmusicapi)
- [Streamlit](https://streamlit.io)

---