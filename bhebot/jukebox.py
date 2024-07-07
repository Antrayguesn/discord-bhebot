from collections import deque
import json
import random

import discord
import youtube_dl

from bhebot.singleton import Singleton

from youtubesearchpython import VideosSearch

FILE_STATSONG = 'conf/statSong.json'
YOUTUBE_LINK="https://www.youtube.com/watch?v={}"

class Jukebox(metaclass = Singleton) :

    isPlaying = False
    isCreated = False

    botVoiceChannel = None
    voiceChannel = None

    queueSong = deque()


    currentSong = ""
    urlSong = {}
    statSong = {}

    # Create the bot
    async def create(self, voiceChannel) :
        if not self.isCreated :
            try :
                with open(FILE_STATSONG, 'r') as musicList :
                    self.statSong = json.loads(musicList.read())
            except json.decoder.JSONDecodeError :
                pass
            except FileNotFoundError:
                statSong = {}

            self.voiceChannel = voiceChannel
            self.botVoiceChannel = await voiceChannel.connect()
            self.isCreated = True
        
    # Return the current song url
    def nowPlaying(self) :
        if self.isPlaying :
            return self.urlSong[self.currentSong]
            "https://www.youtube.com/watch?v="
        return None

    # Skip the song
    def forceskip(self) :
        if not self.isCreated :
            return "Aucune musique en cours"
        self.botVoiceChannel.stop()
        return None

    # Get the youtube ID song
    def getCurrentSongID(self):
        return pafy.new(self.urlSong[self.currentSong]).videoid

    # Add the song to the queue :)
    def addSongToQueue(self, shearedSong, force=False) :
        audioYoutube = None

        url=None
        urlJson = VideosSearch(shearedSong, limit = 1, region = 'FR').result()
        url = urlJson['result'][0]['link']


        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          infoYoutube = ydl.extract_info(url, download=False)
        print(infoYoutube)
        audioYoutube = infoYoutube.getbestaudio()


        if force :
            self.queueSong.appendleft(audioYoutube)
        else :
            self.queueSong.append(audioYoutube)

        if url[:4] == "http":
            self.urlSong[audioYoutube] = url
        else :
            self.urlSong[audioYoutube] = YOUTUBE_LINK.format(url)

        try :
            self.statSong[infoYoutube.videoid]["played"] += 1
        except KeyError :
            self.statSong[infoYoutube.videoid] = {"name": infoYoutube.title, "url": url, "played": 1}

        with open(FILE_STATSONG, 'w') as outfile:
            json.dump(self.statSong, outfile)

        return url

    # Put your song on the top of the queue and play it
    def forceplay(self, url) :
        if not self.isCreated :
            return "Pas de musique en cours"
        self.addSongToQueue(url, True)
        self.botVoiceChannel.stop()
        return None

    async def stop(self, force = False) :
        if self.isPlaying or force :
            self.botVoiceChannel.stop()
            self.isPlaying = False

            self.voiceChannel = None
            await self.botVoiceChannel.disconnect()
            self.botVoiceChannel = None
            self.isCreated = False
    
    # Clear playlist
    def clear(self) :
        self.queueSong.clear()

    # Shuffle the playlist
    async def playShuffle(self, voiceChannel=None):

        if not self.isCreated :
            await self.create(voiceChannel)

        newOrder = list(self.statSong.keys())
        random.shuffle(newOrder)

        for song in newOrder :
            self.play(song)
    
    # Play the next song
    def nextSong(self, error = None):
        if error is not None:
            print(error)
        if self.isPlaying:
            if len(self.queueSong) != 0 :
                try :
                    self.urlSong.pop(self.currentSong)
                except KeyError:
                    pass
                self.currentSong = self.queueSong.popleft()
                audioSource = discord.FFmpegPCMAudio(self.currentSong.url, options="-filter:a loudnorm")
                self.botVoiceChannel.play(audioSource, after=self.nextSong)
            else :
                self.isPlaying = False

    # Play the song
    def play(self, url) :
        if self.isCreated :
            urlShearched = self.addSongToQueue(url)
            if not self.isPlaying :
                self.isPlaying = True
                self.nextSong(None)
            return urlShearched
