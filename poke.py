import discord, random, os, subprocess
from dotenv import load_dotenv
from movieFunctions import (userInput, getActor, getRandomMovie, getMovieSearch, getMovieDetails, getFilmography, getActorID)
from genreData import GENRES


load_dotenv()
API_KEY = os.getenv("MOVIE_API_KEY")
DISCORD_TOKEN = os.getenv("CINEBOT_DISCORD_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def startMessage(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("Hi everyone! Enter $info To Get Started!")
                break
    
    async def on_message(self, message):

        if message.author == self.user:
            return
        
        if message.content.startswith('$info'):
            await message.channel.send("Hi, I am called PokeBot, I give information and recommendations for movies!" 
                                       + "__**\n Commands: **__" 
                                       + "\n $movieRandom: Recommends a movie based on the genre you want to watch" 
                                       + "\n $actorRandom: Recommends a movie based on an actor you want to watch"
                                       + "\n $actorKnown: Tells you what movies the actor is known for"
                                       + "\n $actorFilms: Tells you the entire filmography of an actor"
                                       + "\n $search: Gets details on movies you want to search for"
                                       + "\n $stop: Resets and stops all current actions of the bot")

        if message.content.startswith('$movieRandom'):
            genreName = await userInput(self, "What Genre Of Movie Do You Want To Watch", message)
            genreID = GENRES.get(genreName)
            if not genreID:
                await message.channel.send('I dont recognize this genre, my apolgies')
                return
            randomMovie = await getRandomMovie(genreID)
            await getMovieDetails(randomMovie, message)
           
        if message.content.startswith("$actorRandom"):
            actorName = await userInput(self, "What Is The Name Of The Actor You Want To Watch?", message)
            knownFor = await getActor(actorName, message)
            randomMovie =  random.choice(knownFor)
            await getMovieDetails(randomMovie, message)
           
        if message.content.startswith("$actorKnown"):
            actorName = await userInput(self, "What Is The Name Of The Actor You Want To Watch?", message)
            knownFor = await getActor(actorName, message)
            for i in knownFor:
                await getMovieDetails(i, message)
        if message.content.startswith("$actorFilms"):
            actorName = await userInput(self, "What Is The Name Of The Actor You Want To Watch?", message)
            actorID = await getActorID(actorName, message)
            await getFilmography(actorID, message)

        if message.content.startswith("$search"):
             movieSearch = await userInput(self, "What Movie Do You Want To Search For?", message)
             movie = await getMovieSearch (movieSearch, message)
             await getMovieDetails(movie, message)
        
        if message.content.startswith("$stop"):
            await self.close()
            subprocess.run(["python", "poke.py"])


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
