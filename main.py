

import discord
import time
from discord.ext import commands
from commands import *
import random
import youtube_dl
import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import re
from youthumbnail import youthumbnail

client = discord.Client()
bot = commands.Bot(command_prefix="?")      #----------- /!\ important /!\ -----------#
server = discord.Server
bot.remove_command('help')           #------------- Remove le ?help prédéfini -----------#


@bot.event
async def on_ready():
    print('Connecté à')
    print(bot.user.name)
    print(bot.user.id)
    print('------')  #-------------

@bot.event
async def on_message(message):
    member = message.author
    content = message.content
    channel = message.channel
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    print('[', date, '] ', member, "in", channel , "-", content)   #------ logs console ------#

    await bot.process_commands(message) # ------ /!\ important sinon ?commandes pas fonctionnelles /!\ ---------- #

@bot.command(pass_context=True)
async def hello(ctx, *arg):

    msg = ' '.join(arg)
    return await bot.say(msg)


@bot.command(pass_context=True)
async def info(ctx,*, utilisateur):
    message = ctx.message  #------------ récupère l'objet message -------- #
    user = message.server.get_member_named(utilisateur) #----------- trouve l'utilisateur -------- #
    if user == None:
        return await bot.say("L'utilisateur **"+utilisateur+"** n'existe pas.")
    else:
        Member = user
        nicknameUser = user.nick
        print(user.default_avatar_url)
        if user.avatar_url != '':
            avatarUser = user.avatar_url
        else:
            avatarUser = user.default_avatar_url

        if Member.nick == None:
            nicknameUser = ':x: **AUCUN**'
        else:
            nicknameUser = user.nick
        if Member.game == None:
            jeuUser = ':x: **AUCUN**'
        else:
            jeuUser = Member.game.name

        if Member.status == Member.status.online:
            StatusUser='**EN LIGNE**'

        elif Member.status == Member.status.idle:
            StatusUser ='**NE PAS DERANGE**'
        else:
            StatusUser = '**HORS LIGNE**'
        embed = discord.Embed(color=Member.color)
        embed.set_author(name=user.name +'#'+ user.discriminator,icon_url='https://image.noelshack.com/fichiers/2017/35/3/1504096952-graphicloads-flat-finance-person.png')
        embed.set_thumbnail(url=avatarUser)
        embed.add_field(name=":busts_in_silhouette: Nickname",value=nicknameUser,inline=True)
        embed.add_field(name=":round_pushpin: Rôle", value=Member.top_role, inline=True)
        embed.add_field(name=":video_game: Jeu", value=jeuUser, inline=True)
        embed.add_field(name=":white_check_mark: Statut", value=StatusUser, inline=True)

        return await bot.say(embed=embed)


@bot.command(pass_context=True)
async def help():

    #------------------- Embed ---------------#

    embed = discord.Embed(color=0x2ecc71)
    embed.set_author(name="LES COMMANDES DE DIDIO\'MATIC", icon_url='https://image.noelshack.com/fichiers/2017/35/1/1503939867-trisomy-21-down-syndrome-kennedi-beahn-presented-by-kraig-beahn2.jpg')
    embed.set_thumbnail(url='http://icons.iconarchive.com/icons/graphicloads/100-flat/256/settings-3-icon.png')

    #--------------- affiche 1 field pour chaque commande ---------------#
    i = 0
    while i < len(NomAllCommande):
        key = NomAllCommande[i]
        value = descriptionAllCommandes[i]
        embed.add_field(name="?" + key + "  " + subCommande[i],value=value, inline=True)
        i = i + 1



    return await bot.say(embed=embed)
@bot.command(pass_context=True)
async def alain():
    return await bot.say("J'ai faim plus que **Alain**.\n https://www.youtube.com/watch?v=BuMCZHyGwXw")

@bot.command(pass_context=True)
async def meme(ctx):
    message = ctx.message  #------------ récupère l'objet message -------- #
    memeRandom = str(random.randint(0, 1020))
    imageMeme = "C:\\Users\\samuel\\Documents\\GitHub\\DidiO-matic\\Meme pack by LiquidIllusion\\" + memeRandom + '.jpg'
    return await bot.send_file(message.channel, fp=imageMeme, content="**NO GOD PLEASE**")

#----------- commandes bot musiques -------------- #
@bot.group(pass_context=True)
async def yt(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Commande **yt** invalide. Faites **?help** pour plus d\'informations sur cette commande.')

@yt.command(pass_context=True)
async def join(ctx):
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await bot.join_voice_channel(voice_channel)
    channel = voice_channel.name

    return await bot.say("Connecté au channel vocal **#" + channel + "**.")

@yt.command(pass_context = True)
async def leave(ctx):
    for x in bot.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()

    return await bot.say("Je ne suis dans aucun **channel vocal**.")
@yt.command(pass_context = True)
async def play(ctx, ytLien):
    message = ctx.message  #------------ récupère l'objet message -------- #
    user = message.author #----------- trouve l'utilisateur -------- #
    if user.avatar_url != '':
        avatarUser = user.avatar_url
    else:
        avatarUser = user.default_avatar_url
    for x in bot.voice_clients:
        if(x.server == ctx.message.server):
                player = await x.create_ytdl_player(ytLien)
                if player.duration > 1200:
                    return await bot.say("**"+player.title+"** ne peut être joué, il dépasse les 20 minutes.")
                else:
                    player.start()
                    MusicIconeUrl = youthumbnail(player.url, 'l')
                    musicTime = str(datetime.timedelta(seconds=player.duration))
                    embed=discord.Embed(title=player.title, color=0xb71402)
                    embed.set_thumbnail(url=MusicIconeUrl)
                    embed.set_author(name="En lecture", url=player.url, icon_url=avatarUser)
                    embed.add_field(name="Artiste", value=player.uploader, inline=True)
                    embed.add_field(name="Durée", value=musicTime, inline=True)
                    embed.set_footer(text="par DiDiO'matic ")
                    await bot.say(embed=embed)

@yt.command(pass_context=True)
async def search(ctx, *, MusicName):
    query = urllib.parse.quote(MusicName)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}, limit=1):
        if not vid['href'].startswith("https://googleads.g.doubleclick.net/‌​"):
            return await bot.say('Voici le lien de la vidéo correspondant à **' + MusicName + '**: https://www.youtube.com' + vid['href'])





bot.run('MzUwOTg4MDU5NjQwMjAxMjE2.DIMCow.7PxSQtuGb7t356bAY2D4gobB-60')  # ----------- /!\ important /!\ ------- #
