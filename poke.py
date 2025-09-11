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
            await message.channel.send('Enter The Genre Of Movie You Want To Watch: ')
            try:
                msg = await self.wait_for("message", timeout=30)
                genreName = msg.content.lower()
                genreID = GENRES.get(genreName)
                if not genreID:
                    await message.channel.send('I dont recognize this genre, my apolgies')
                    return
                url = "https://api.themoviedb.org/3/discover/movie?api_key=" + API_KEY + "&with_genres=" + str(genreID) + "&language=en-US"
                response =  requests.get(url).json()
                randomMovie = random.choice(response["results"])
                ageRating = await self.getAgeRating(randomMovie)  
                poster = randomMovie["poster_path"]
                await self.getPoster(poster, message)
                await message.channel.send("🎬 **" + randomMovie["title"] + "**\nRelease Date: " + randomMovie["release_date"] + "\nAge Rating: " + ageRating + "\nOverview: " + randomMovie["overview"])
            except asyncio.TimeoutError:
                await message.channel.send('Sorry Took To Long To Respond')
        if message.content.startswith("$actorRandom"):
            await message.channel.send("What Is The Name Of The Actor You Want To Watch?")
            try: 
                msg = await self.wait_for("message", timeout=30)
                actorName = msg.content.lower()
                knownFor = await self.getActor(actorName, message)
                randomMovie =  random.choice(knownFor)
                ageRating = await self.getAgeRating(randomMovie)
                poster = randomMovie["poster_path"]
                await self.getPoster(poster,message)
                await message.channel.send("🎬 **" + randomMovie["title"] + "**\nRelease Date: " + randomMovie["release_date"] + "\nAge Rating: " + ageRating + "\nOverview: " + randomMovie["overview"])
            except asyncio.TimeoutError:
                await message.channel.send('Sorry Took To Long To Respond')
        if message.content.startswith("$actorKnownfor"):
            await message.channel.send("What Is The Name Of The Actor You Want To Watch?")
            try: 
                msg = await self.wait_for("message", timeout=30)
                actorName = msg.content.lower()
                knownFor = await self.getActor(actorName, message)
                for i in knownFor:
                    poster = i["poster_path"]
                    await self.getPoster(poster, message)
                    ageRating = await self.getAgeRating(i)
                    await message.channel.send("🎬 **" + i["title"] + "**\nRelease Date: " + i["release_date"] + "\nAge Rating: " + ageRating + "\nOverview: " + i["overview"])
            except asyncio.TimeoutError:
                await message.channel.send('Sorry Took To Long To Respond')
        if message.content.startswith("$search"):
            await message.channel.send("What Movie Do You Want To Search For?")
            try:
                msg = await self.wait_for("message", timeout=30)
                movieSearch = msg.content.lower()
                url = "https://api.themoviedb.org/3/discover/movie?api_key=" + API_KEY + "&query=" + movieSearch
                response = requests.get(url).json()
                if not response["results"]:
                    await message.channel.send("Sorry, I don't recognize this movie")
                movie = response["results"]
                poster = movie["poster_path"]
                await self.getPoster(poster, message)


            except asyncio.TimeoutError:
                await message.channel.send('Sorry Took To Long To Respond')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
