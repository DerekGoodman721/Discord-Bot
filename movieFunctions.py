import requests, random, asyncio, os
from dotenv import load_dotenv
from genreData import REVERSED_GENRES

load_dotenv()
API_KEY = os.getenv("MOVIE_API_KEY")

async def getFilmography(actorID, message):
    url = "https://api.themoviedb.org/3/person/" + str(actorID) + "/combined_credits?api_key=" + API_KEY
    response = requests.get(url).json()
    movies = [credit for credit in response["cast"] if credit["media_type"] == "movie"]
    for movie in movies:
            genreNames = await getGenre(movie)
            ageRating = await getAgeRating(movie)
            await message.channel.send("🎬 **__" + movie["title"] + "__\nCharacter Played: **" + movie["character"] +"**\nRelease Date: **" + movie["release_date"] + "**\nAge Rating: **" + ageRating + "**\nGenres: **"+ ", ".join(g.capitalize() for g in genreNames) + "\n")


async def getRandomMovie(genreID):
    url = "https://api.themoviedb.org/3/discover/movie?api_key=" + API_KEY + "&with_genres=" + str(genreID) + "&language=en-US"
    response =  requests.get(url).json()
    randomMovie = random.choice(response["results"])
    return randomMovie
    
async def getMovieSearch(movieSearch, message):
    url = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query=" + movieSearch
    response = requests.get(url).json()
    if not response["results"]:
        await message.channel.send("Sorry, I don't recognize this movie")
    movie = response["results"][0]
    return movie

async def userInput(client, prompt, message):
    await message.channel.send(prompt)
    try:
        msg = await client.wait_for("message", timeout = 30)
        return msg.content.lower()
    except asyncio.TimeoutError:
        await message.channel.send('Sorry Took To Long To Respond')

async def getMovieDetails(movie, message):
    ageRating = await getAgeRating(movie)  
    genreNames = await getGenre(movie)
    poster = movie["poster_path"]
    await getPoster(poster, message)
    await message.channel.send("🎬 **__" + movie["title"] + "__\nRelease Date: **" + movie["release_date"] + "**\nAge Rating: **" + ageRating + "**\nGenres: **"+ ", ".join(g.capitalize() for g in genreNames) +"**\nOverview: **" + movie["overview"])
        
async def getActor(actorName, message):
    url = "https://api.themoviedb.org/3/search/person?api_key=" + API_KEY + "&query=" + actorName
    response = requests.get(url).json()
    if not response["results"]:
        await message.channel.send("Sorry, I don't recognize this actor")
    knownFor = []
    for n in response["results"]:
        for m in n["known_for"]:
            knownFor.append(m)
            
    return knownFor

async def getActorID(actorName, message):
    url = "https://api.themoviedb.org/3/search/person?api_key=" + API_KEY + "&query=" + actorName
    response = requests.get(url).json()
    if not response["results"]:
        await message.channel.send("Sorry, I don't recognize this actor")
    actorID = response["results"][0]["id"]
    return actorID

async def getGenre(movie):
    genreNames = []
    for genreID in movie["genre_ids"]:
        if genreID in REVERSED_GENRES:
            genreNames.append(REVERSED_GENRES[genreID])
    genreNames = [g.capitalize() for g in genreNames]
    return genreNames 


async def getPoster(poster, message):
    if poster:
        img = "https://image.tmdb.org/t/p/w500" + poster
        await message.channel.send(img)
    else:
        await message.channel.send("Sorry no poster found")

async def getAgeRating(movie):
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