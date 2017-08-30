import discord
import time
from discord.ext import commands



NomAllCommande = []
descriptionAllCommandes = []

bot = commands.Bot(command_prefix="?")      #----------- /!\ important /!\ -----------#
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
descriptionCommande = "Répond par votre message."
descriptionAllCommandes.append(descriptionCommande)

@bot.command(pass_context=True)
async def info(ctx, *utilisateur):
    user = message.server.get_member_named(utilisateur)
    Member = user
    try:

        if user.nick != None:
            nicknameUser = user.nick

        else:
            nicknameUser = 'Aucun nickname.'

        if Member.game == None:
            Member.game = 'Ne joue pas

        if Member.status == Member.status.online:
            Member.status=':large_blue_circle: En ligne'

        elif Member.status == Member.status.idle:
            Member.status =':black_circle: Ne pas déranger '

        else:
            Member.status =':red_circle: Déconnecté'
            embed = discord.Embed(color=Member.color)
            embed.set_author(name=utilisateur +'#'+ user.discriminator,icon_url='https://image.noelshack.com/fichiers/2017/35/1/1503939867-trisomy-21-down-syndrome-kennedi-beahn-presented-by-kraig-beahn2.jpg')
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Nickname",value=nicknameUser,inline=True)
            embed.add_field(name="Rôle", value=Member.top_role, inline=True)
            embed.add_field(name="Jeu", value=Member.game, inline=True)
            embed.add_field(name="Statut", value=Member.status, inline=True)
            
            return await bot.say(embed=embed)

        except AttributeError:
            return await bot.say('**Cet utilisateur n\'existe pas, vérifiez les majuscules.**')

descriptionCommande = "Donne des informations concernant un membre du serveur discord."
descriptionAllCommandes.append(descriptionCommande)


@bot.command(pass_context=True)
async def help():

    #------------------- Embed ---------------#

    embed = discord.Embed(color=0x2ecc71)
    embed.set_author(name="LES COMMANDES DE DIDIO\'MATIC", icon_url='https://image.noelshack.com/fichiers/2017/35/1/1503939867-trisomy-21-down-syndrome-kennedi-beahn-presented-by-kraig-beahn2.jpg')
    embed.set_thumbnail(url='http://icons.iconarchive.com/icons/graphicloads/100-flat/256/settings-3-icon.png')

    #--------------- affiche 1 field pour chaque commande ---------------#

    i = 0
    for key in bot.commands:
        NomAllCommande.append((key))
    while i<len(bot.commands):
        embed.add_field(name="?"+ NomAllCommande[i],value=descriptionAllCommandes[i], inline=True)
        i = i + 1


    return await bot.say(embed=embed)
descriptionCommande = "Vous affiche la liste des commandes."
descriptionAllCommandes.append(descriptionCommande)



bot.run('MzUwOTg4MDU5NjQwMjAxMjE2.DIMCow.7PxSQtuGb7t356bAY2D4gobB-60')  # ----------- /!\ important /!\ ------- #
