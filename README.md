## Overview

PokeBot & MemeBot are Discord bots designed for entertainment purposes.

- **PokeBot** recommends movies either randomly or based on selected genres and actors, provides actor filmography and discography information, and provides detailed movie information
- **MemeBot** generates and sends random memes on command for the selected channel.

---
## Features
### PokeBot Commands

- **`$movieRandom <genre>`**  
  Recommends a random movie based on the genre you want to watch.

- **`$actorRandom <actor>`**  
  Recommends a movie featuring the actor you want to watch.

- **`$actorKnown <actor>`**  
  Shows the most well-known movies of a given actor.

- **`$actorFilms <actor>`**  
  Displays the complete filmography of a given actor.

- **`$search <movie>`**  
  Retrieves detailed information about a specific movie.

- **`$stop`**  
  Stops the bot and resets all current actions.

### MemeBot Commands

- **`$meme`**  
  Generates a random meme in the current channel
  
---
## Tech Stack
- **Python** – Core programming language  
- **discord.py** – Discord API wrapper for bot  
- **TMDb API** – Provides movie, actor, and filmography data
- ****Meme API:** meme-api.com (`/gimme` endpoint)** – Source for randomly generated memes
- **HTTP Requests:** requests  
- **Environment Variables:** python-dotenv  

---

## 📂 Project Structure

```
project-root/
│── bot.py
│── .env
│── requirements.txt
│── README.md
```
---


1. Clone the repository:
```bash
git clone https://github.com/your-username/pokebot-memebot.git
cd pokebot-memebot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:

```env
DISCORD_TOKEN=your_discord_bot_token
TMDB_API_KEY=your_tmdb_api_key
```

4. Run the bot:
```bash
python bot.py
```

---

## Usage Examples

```
$movieRandom action
$actorRandom Tom Hanks
$actorKnown Leonardo DiCaprio
$actorFilms Scarlett Johansson
$search Inception
$meme
```
---

## ✅ Requirements

- Python 3.9 or higher  
- Discord Bot Token  
- TMDb API Key  
- Internet connection  

### 🔐 Bot Permissions
- Send Messages  
- Read Messages  
- Embed Links (recommended)  

---

## Environment Variables

| Variable        | Description                  |
|----------------|------------------------------|
| DISCORD_TOKEN  | Your Discord bot token       |
| TMDB_API_KEY   | Your TMDb API key            |

---

## Future Improvements
- Watchlist feature  


## 👤 Author

**Derek Goodman**  
GitHub: https://github.com/DerekGoodman721


