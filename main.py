import datetime
import random
import time
import urllib
import urllib.parse
from urllib.request import urlopen

import discord
import youtube_dl
from bs4 import BeautifulSoup
from discord.ext import commands

from commands import *
from youthumbnail import youthumbnail

client = discord.Client()
bot = commands.Bot(command_prefix="?")  # ----------- /!\ important /!\ -----------#
server = discord.Server
bot.remove_command('help')  # ------------- Remove le ?help prédéfini -----------#

global player
musics = []


@bot.event
async def on_ready():
    print('Connecté à')
    print(bot.user.name)
    print(bot.user.id)
    print('------')  # -------------


@bot.event
async def on_message(message):
    member = message.author
    content = message.content
    channel = message.channel
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    print('[', date, '] ', member, "in", channel, "-", content)  # ------ logs console ------#

    await bot.process_commands(message)  # ------ /!\ important sinon ?commandes pas fonctionnelles /!\ ---------- #


@bot.command(pass_context=True)
async def hello(ctx, *arg):
    msg = ' '.join(arg)
    return await bot.say(msg)


@bot.command(pass_context=True)
async def info(ctx, *, utilisateur):
    message = ctx.message  # ------------ récupère l'objet message -------- #
    user = message.server.get_member_named(utilisateur)  # ----------- trouve l'utilisateur -------- #
    if user is None:
        return await bot.say("L'utilisateur **" + utilisateur + "** n'existe pas.")
    else:
        member = user
        nickname_user = user.nick
        print(user.default_avatar_url)
        if user.avatar_url != '':
            avatar_user = user.avatar_url
        else:
            avatar_user = user.default_avatar_url

        if member.nick is None:
            nickname_user = ':x: **AUCUN**'
        else:
            nickname_user = user.nick
        if member.game is None:
            jeu_user = ':x: **AUCUN**'
        else:
            jeu_user = member.game.name

        if member.status == member.status.online:
            status_user = '**EN LIGNE**'

        elif member.status == member.status.idle:
            status_user = '**NE PAS DERANGE**'
        else:
            status_user = '**HORS LIGNE**'
        embed = discord.Embed(color=member.color)
        embed.set_author(name=user.name + '#' + user.discriminator,
                         icon_url='https://image.noelshack.com/fichiers/2017/35/3/1504096952-graphicloads-flat-finance-person.png')
        embed.set_thumbnail(url=avatar_user)
        embed.add_field(name=":busts_in_silhouette: Nickname", value=nickname_user, inline=True)
        embed.add_field(name=":round_pushpin: Rôle", value=member.top_role, inline=True)
        embed.add_field(name=":video_game: Jeu", value=jeu_user, inline=True)
        embed.add_field(name=":white_check_mark: Statut", value=status_user, inline=True)

        return await bot.say(embed=embed)


@bot.command(pass_context=True)
async def help():
    # ------------------- Embed ---------------#

    embed = discord.Embed(color=0x2ecc71)
    embed.set_author(name="LES COMMANDES DE DIDIO\'MATIC",
                     icon_url='https://image.noelshack.com/fichiers/2017/35/1/1503939867-trisomy-21-down-syndrome-kennedi-beahn-presented-by-kraig-beahn2.jpg')
    embed.set_thumbnail(url='http://icons.iconarchive.com/icons/graphicloads/100-flat/256/settings-3-icon.png')

    # --------------- affiche 1 field pour chaque commande ---------------#
    i = 0
    while i < len(NomAllCommande):
        key = NomAllCommande[i]
        value = descriptionAllCommandes[i]
        embed.add_field(name="?" + key + "  " + subCommande[i], value=value, inline=True)
        i = i + 1

    return await bot.say(embed=embed)


@bot.command(pass_context=True)
async def alain():
    return await bot.say("J'ai faim plus que **Alain**.\n https://www.youtube.com/watch?v=BuMCZHyGwXw")


@bot.command(pass_context=True)
async def meme(ctx):
    message = ctx.message  # ------------ récupère l'objet message -------- #
    meme_random = str(random.randint(0, 1020))
    image_meme = "C:\\Users\\samuel\\Documents\\GitHub\\DidiO-matic\\Meme pack by LiquidIllusion\\" + meme_random + '.jpg'
    return await bot.send_file(message.channel, fp=image_meme, content="**NO GOD PLEASE**")


# ----------- commandes bot musiques -------------- #
@bot.group(pass_context=True)
async def yt(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Commande **yt** invalide. Faites **?help** pour plus d\'informations sur cette commande.')


@yt.command(pass_context=True)
async def join(ctx):
    try:
        author = ctx.message.author
        voice_channel = author.voice_channel
        vc = await bot.join_voice_channel(voice_channel)
        channel = voice_channel.name
        await bot.change_presence(game=None, status='idle', afk=False)
        return await bot.say("Connecté au channel vocal **#" + channel + "**.")
    except discord.InvalidArgument:
        return await bot.say('Vous n\'êtes connecté à aucun **channel vocal**.')
    except discord.ClientException:
        channel = voice_channel.name
        return await bot.say('Déjà connecté au channel vocal **#' + channel + '**')


@yt.command(pass_context=True)
async def leave(ctx):
    for x in bot.voice_clients:
        if x.server == ctx.message.server:
            await bot.change_presence(game=None)
            await bot.change_presence(game=None, status='online', afk=False)

            return await x.disconnect()

    return await bot.say("Je ne suis dans aucun **channel vocal**.")


@yt.command(pass_context=True)
async def play(ctx, *, yt_lien):
    global musics
    message = ctx.message  # ------------ récupère l'objet message -------- #
    user = message.author  # ----------- trouve l'utilisateur -------- #
    if user.avatar_url != '':
        avatar_user = user.avatar_url
    else:
        avatar_user = user.default_avatar_url
    for x in bot.voice_clients:
        if x.server == ctx.message.server:
            try:
                player = await x.create_ytdl_player(yt_lien)
                musics.append(player)
            except youtube_dl.utils.DownloadError:
                query = urllib.parse.quote(yt_lien)
                url = "https://www.youtube.com/results?search_query=" + query
                response = urlopen(url)
                html = response.read()
                soup = BeautifulSoup(html, "html.parser")

                for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}, limit=1):
                    if not vid['href'].startswith("https://googleads​"):
                        yt_lien = 'https://www.youtube.com' + vid['href']
                        player = await x.create_ytdl_player(yt_lien)
                        musics = player
            if player.duration > 1200:
                return await bot.say("**" + player.title + "** ne peut être joué, il dépasse les 20 minutes.")
            else:
                player.start()
                music_icone_url = youthumbnail(player.url, 'l')
                music_time = str(datetime.timedelta(seconds=player.duration))
                embed = discord.Embed(title=player.title, color=0xb71402)
                embed.set_thumbnail(url=music_icone_url)
                embed.set_author(name="En lecture", url=player.url, icon_url=avatar_user)
                embed.add_field(name="Artiste", value=player.uploader, inline=True)
                embed.add_field(name="Durée", value=music_time, inline=True)
                embed.set_footer(text="par DiDiO'matic ")
                await bot.change_presence(game=discord.Game(name=player.title))
                await bot.say(embed=embed)


@yt.command(pass_context=True)
async def queue(ctx):
    global musics
    if musics.is_live:
        return await bot.say("Une musique est en train d'être jouée")
    else:
        return await bot.say('Pas de musique jouée.')


@yt.command(pass_context=True)
async def search(ctx, *, music_name):
    query = urllib.parse.quote(music_name)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}, limit=1):
        if not vid['href'].startswith("https://googleads"):
            return await bot.say(
                'Voici le lien de la vidéo correspondant à **' + music_name + '**: https://www.youtube.com' +
                vid['href'])
        else:
            return await bot.say("Aucune vidéo trouvée pour cet élément de recherche")


bot.run('MzUwOTg4MDU5NjQwMjAxMjE2.DIMCow.7PxSQtuGb7t356bAY2D4gobB-60')  # ----------- /!\ important /!\ ------- #
