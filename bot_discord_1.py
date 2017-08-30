import discord
import time
from discord.ext import commands
from commands import *


bot = commands.Bot(command_prefix="?")      #----------- /!\ important /!\ -----------#
server = discord.Server
bot.remove_command('help')           #------------- Remove le ?help prédéfini -----------#


@bot.event
async def on_ready():
    print('Connecté à')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

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
async def info(ctx, utilisateur):
    message = ctx.message  #------------ récupère l'objet message -------- #
    user = message.server.get_member_named(utilisateur) #----------- trouve l'utilisateur -------- #
    Member = user
    nicknameUser = user.nick
    print(user.default_avatar_url)
    if user.avatar_url != '':
        avatarUser = user.avatar_url
    else:
        avatarUser = user.default_avatar_url

    if Member.nick == None:
        nicknameUser = ':x: **Aucun**'
    else:
        nicknameUser = user.nick
    if Member.game == None:
        jeuUser = 'Ne joue pas.'
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
"""
        if user.nick != None:
            nicknameUser = user.nick

        else:
            nicknameUser = 'Aucun nickname.'

        if Member.game == None:
            Member.game = 'Ne joue pas.'

        if Member.status == Member.status.online:
            Member.status=':large_blue_circle: En ligne'

        elif Member.status == Member.status.idle:
            Member.status =':black_circle: Ne pas déranger'

        else:


        return await bot.say(embed=embed)
"""

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
        embed.add_field(name="?"+ key + "  " + subCommande[i],value=value, inline=True)
        i = i + 1



    return await bot.say(embed=embed)




bot.run('MzUwOTg4MDU5NjQwMjAxMjE2.DIMCow.7PxSQtuGb7t356bAY2D4gobB-60')  # ----------- /!\ important /!\ ------- #
