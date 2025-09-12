import discord, requests, random, asyncio, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MOVIE_API_KEY")
DISCORD_TOKEN = os.getenv("POKE_DISCORD_TOKEN")

GENRES = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "horror": 27,
    "romance": 10749,
    "sci-fi": 878,
    "thriller": 53,
    "western": 37,
    "war": 10752,
    "mystery": 9648,
    "history": 36,
    "music": 10402
}

class MyClient(discord.Client):
    async def getRandomMovie(self, genreID):
        url = "https://api.themoviedb.org/3/discover/movie?api_key=" + API_KEY + "&with_genres=" + str(genreID) + "&language=en-US"
        response =  requests.get(url).json()
        randomMovie = random.choice(response["results"])
    
    async def getMovieSearch(self,movieSearch, message):
        url = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query=" + movieSearch
        response = requests.get(url).json()
        if not response["results"]:
            await message.channel.send("Sorry, I don't recognize this movie")
        movie = response["results"][0]
        return movie

    async def userInput(self, prompt, message):
        await message.channel.send(prompt)
        try:
            msg = await self.wait_for("message", timeout = 30)
            return msg.content.lower()
        except asyncio.TimeoutError:
            await message.channel.send('Sorry Took To Long To Respond')

    async def getMovieDetails(self, movie, message):
         ageRating = await self.getAgeRating(movie)  
         poster = movie["poster_path"]
         await self.getPoster(poster, message)
         await message.channel.send("🎬 **" + movie["title"] + "**\nRelease Date: " + movie["release_date"] + "\nAge Rating: " + ageRating + "\nOverview: " + movie["overview"])
        
    async def getActor(self, actorName, message):
        url = "https://api.themoviedb.org/3/search/person?api_key=" + API_KEY + "&query=" + actorName
        response = requests.get(url).json()
        if not response["results"]:
            await message.channel.send("Sorry, I don't recognize this actor")
        knownFor = []
        for n in response["results"]:
            for m in n["known_for"]:
                knownFor.append(m)

        return knownFor
    
    async def getPoster(self, poster, message):
        if poster:
            img = "https://image.tmdb.org/t/p/w500" + poster
            await message.channel.send(img)
        else:
            message.channel.send("Sorry no poster found")

    async def getAgeRating(self, movie):
        certification_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/release_dates?api_key={API_KEY}"
        certResponse = requests.get(certification_url).json()
        ageRating = "NR"  
        for c in certResponse["results"]:
            if c["iso_3166_1"] == "US":
                for r in c["release_dates"]:
                    if r.get("certification"):
                        ageRating = r["certification"]
                        break
                break
        
        return ageRating

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$poke'):
            await message.channel.send('Hi, I am called PokeBot, I give movie recommendations based on what genre you like! Please Enter "$movie" To Start')
        if message.content.startswith('$movie'):
            genreName = await self.userInput("What Genre Of Movie Do You Want To Watch", message)
            genreID = GENRES.get(genreName)
            if not genreID:
                await message.channel.send('I dont recognize this genre, my apolgies')
                return
            randomMovie = await self.getRandomMovie(genreID)
            await self.getMovieDetails(randomMovie, message)
           
        if message.content.startswith("$actorRandom"):
            actorName = await self.userInput("What Is The Name Of The Actor You Want To Watch?", message)
            knownFor = await self.getActor(actorName, message)
            randomMovie =  random.choice(knownFor)
            await self.getMovieDetails(randomMovie, message)
           
        if message.content.startswith("$actorKnownfor"):
            actorName = await self.userInput("What Is The Name Of The Actor You Want To Watch?", message)
            knownFor = await self.getActor(actorName, message)
            for i in knownFor:
                await self.getMovieDetails(i, message)

        if message.content.startswith("$search"):
             movieSearch = await self.userInput("What Movie Do You Want To Search For?", message)
             movie = await self.getMovieSearch (movieSearch, message)
             await self.getMovieDetails(movie, message)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
