import asyncio
import copy
import random
import json

import discord
from discord.ext import commands

import pafy

from bhebot.wrongKey import WrongKey
from bhebot.game import Game
from bhebot.jukebox import Jukebox
from bhebot.singleton import Singleton

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

FILE_MUSIC_FILE = "conf/musiclist.json"
FILE_TOKEN = "conf/token"

with open(FILE_MUSIC_FILE, "r") as musicList :
    songList = json.loads(musicList.read())

botChanel = None

currentSong = ("","")

WrongKey()

@bot.command(
    name='create',
    description='Créer un blind test',
    help='Créer un blind test',
    pass_context=True,
)
async def create(context):
    user=context.message.author

    if user.voice is not None:
        game = Game()
        game.isPlaying = True

        voiceChannel=user.voice.channel
        game.botChanel = await voiceChannel.connect()

        game.start()

        await context.message.channel.send("Allez on s'inscrit ! ($join pour s'inscrie )")
    else:
        await context.message.channel.send("Choisi d'abord un channel !.")

@bot.command(
    name='join',
    description='Rejoinde la partie',
    help='Rejoinde la partie',
    pass_context=True,
)
async def join(context):
    user=context.message.author

    channel=None

    if (user.voice.channel==Game().voiceChannel)and(context.message.channel == Game().textChannel):
        game = Game()
        game.addPlayer(user)
        await game.textChannel.send("{} est de la partie".format(user.mention))
    elif not Game().isPlaying:
        await context.message.channel.send("Attends que le blind test soit lancé quand même !")
    else :
        await context.message.channel.send("Tu n'est pas dans le bon channel.")

@bot.command(
    name='scores',
    description='Obtenir les scores la partie',
    help='Obtenir les scores la partie',
    pass_context=True,
)
async def scores(context):
    await context.message.channel.send(Game().getScores())

@bot.command(
    name='stopbt',
    description='Stop le blind test',
    help='Stop le blind test',
    pass_context=True,
)
async def stopbt(context):
    if Game().isPlaying:
        await Game().botChanel.disconnect()
        Game().isPlaying = False
    else :
        await context.message.channel.send("Joue les commandes dans le bon sens !")

@bot.command(
    name='go',
    description='Jouer le blind test',
    help='Jouer le blind test',
    pass_context=True,
)
async def go(context) :
    game = Game()

    if not game.isPlaying :
        await context.message.channel.send("Joue les commandes dans le bon sens !")
        return

    await context.message.channel.send("Let's goooooooooooooat !")
    await context.message.channel.send(game.getScores())

    playingOrder = list(range(len(songList)))

    random.shuffle(playingOrder)

    for i in playingOrder :
        song = songList[i]
        video = pafy.new(song["url"])
        game.playersGoodSong = []
        game.playersGoodAuthor = []
        best = video.getbestaudio()
        game.setCurrentSong(song["name"], song["author"])
        audioSource = discord.FFmpegPCMAudio(best.url)
        game.isPlaying = True
        game.botChanel.play(audioSource)
        await asyncio.sleep(45)
        game.botChanel.stop()
        await asyncio.sleep(5)
        await game.textChannel.send('{} - {}'.format(song["name"], song["author"]))
        await asyncio.sleep(5)
        playingOrder.remove(i)

    await game.textChannel.send("C'est fini")
    await context.message.channel.send(game.getScores())
    await stop(context)


@bot.command(
    name='jb',
    description='Bhéééééééééééééééééééééééé',
    help='Bhéééééééééééééééééééééééé',
    pass_context=True,
)
async def jb(context):
    user=context.message.author

    if user.voice is not None:
        voiceChannel=user.voice.channel

        localVoiceChannel = await voiceChannel.connect()

        audioSource = discord.FFmpegPCMAudio("ress/chevre.mp3")
        localVoiceChannel.play(audioSource)
        await asyncio.sleep(1.2)
        localVoiceChannel.stop()
        await localVoiceChannel.disconnect()


@bot.command(
    name='play',
    description='Joue une musique',
    help='Joue une musique',
    pass_context=True,
)
async def play(context, *, url):

    if context.message.author.voice :
        await Jukebox().create(context.message.author.voice.channel)
    else :
        await context.message.channel.send("Tu n'est pas connecté à un channel ...")

    urlSearched = Jukebox().play(url)
    if urlSearched :
        await context.message.channel.send(urlSearched)

@bot.command(
    name='nowPlaying',
    aliases=["np"],
    description='Quelle musique est jouée',
    help='Quelle musique est jouée',
    pass_context=True,
)
async def nowPlaying(context):
    songPlay = Jukebox().nowPlaying()
    await context.message.channel.send(songPlay if songPlay is not None else "Aucune musique de lancée")

@bot.command(
    name='stop',
    description='Stop musique est jouée',
    help='Stop musique est jouée',
    pass_context=True,
)
async def stop(context):
    if Jukebox().isCreated :
        await Jukebox().stop()
        Jukebox().isCreated = False

@bot.command(
    name='forceskip',
    aliases=["fs"],
    description='Force le passage de la musique',
    help='Force le passage de la musique',
    pass_context=True,
)
async def forceskip(context):
    error = Jukebox().forceskip()
    if error is not None :
        await context.message.channel.send(error)

@bot.command(
    name='forceplay',
    aliases=["fp", "ps"],
    description='Force le passage de la musique passée en paramètre',
    help='Force le passage de la musique passée en paramètre',
    pass_context=True,
)
async def forceplay(context,*, url):
    error = Jukebox().forceplay(url)
    if error is not None :
        await context.message.channel.send(error)

@bot.command(
    name='clear',
    description='Efface tout la programmation',
    help='Efface tout la programmation',
    pass_context=True,
)
async def clear(context):
    Jukebox().clear()

@bot.command(
    name='cestlafete',
    description='Joue toutes les musique déjà joué en aléatoire',
    help='Joue toutes les musique déjà joué en aléatoire',
    pass_context=True,
)
async def cestLaFete(context):
    await Jukebox().playShuffle(context.message.author.voice.channel)

@bot.command(
    name='plaisir',
    aliases=["afrique", "adieu", "olala"],
    description='Que du bonheur',
    help='Que du plaisir',
    pass_context=True,
)
async def plaisir(context):
    error = Jukebox().forceplay("ge5jsFtXOAY")
    if error is not None :
        await Jukebox().create(context.message.author.voice.channel)
        Jukebox().play("ge5jsFtXOAY")
    await context.message.channel.send("QUE DU PLAISIR !")

@bot.command(
    name='addCurrentBT',
    description='Ajoute la musique courante a la liste des musiques du blind test',
    usage="\"nom\" \"auteur\" [\"meta\"]",
    help='Ajoute la musique courante a la liste des musiques du blind test',
    pass_context=True,
)
async def addCurrentBT(context, name, author, meta=""):
    urlCurrentSong = Jukebox().nowPlaying()
    infoYoutube = pafy.new(urlCurrentSong)
    songList.append({"name": name, "author": author, "url": urlCurrentSong, "id": infoYoutube.videoid, "meta": meta})
    with open(FILE_MUSIC_FILE, 'w') as outfile:
        json.dump(songList, outfile)

@bot.command(
    name='addBT',
    description='Ajoute la musique en paramètre a la liste des musiques du blind test',
    usage="url \"nom\" \"auteur\" [\"meta\"]",
    help='Ajoute la musique en paramètre a la liste des musiques du blind test',
    pass_context=True,
)
async def addBT(context, url, name, author, meta=""):
    infoYoutube = pafy.new(url)
    songList.append({"name": name, "author": author, "url": url, "id": infoYoutube.videoid, "meta": meta})
    with open(FILE_MUSIC_FILE, 'w') as outfile:
        json.dump(songList, outfile)

# Event on channel

@bot.event
async def on_message(message) :
    await bot.process_commands(message)
    game = Game()

    if (message.author == bot.user) or message.content.startswith("$") or (message.channel != game.textChannel) or game.isPlaying == False:
        return

    if not Jukebox().isPlaying :
        await Jukebox().stop()

    if message.author not in game.players.keys() :
        await message.channel.send("Tu n'est pas inscrit {}!".format(message.author.mention))
        await message.delete()
        return

    elif game.botChanel is not None and game.isPlaying and game.currentSong != "" :
        messageCopied = copy.copy(message)
        await message.delete()

        strToSend = processReponse(message)

        await messageCopied.channel.send(strToSend.format(messageCopied.author.mention))

@bot.event
async def on_voice_state_update(member, before, after) :
    if not Jukebox().isPlaying and not member.bot:
        await Jukebox().stop(True)


with open(FILE_TOKEN, "r") as tokenFile :
    bot.run(tokenFile.read())
