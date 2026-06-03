## Overview

PokeBot & MemeBot are Discord bots designed for entertainment and discovery.

- **PokeBot** recommends movies either randomly or based on selected genres and actors, and provides actor filmography and discography information.
- **MemeBot** generates and sends random memes on command.
- 
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

## Tech Stack
- **Python** – Core programming language  
- **discord.py** – Discord API wrapper for bot  
- **TMDb API** – Provides movie, actor, and filmography data
- **- **Meme API:** meme-api.com (`/gimme` endpoint)** – Source for randomly generated memes

