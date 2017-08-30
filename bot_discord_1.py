import discord
import time
from discord.ext import commands
NomAllCommande = []
descriptionAllCommandes = []
bot = commands.Bot(command_prefix="?")
bot.remove_command('help')

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
        print('[', date, '] ', member, "in", channel , "-", content)
        await bot.process_commands(message)

@bot.command(pass_context=True)
async def hello(ctx, *arg):

    msg = ' '.join(arg)
    return await bot.say(msg)
descriptionCommande = "Répond par votre message."
descriptionAllCommandes.append(descriptionCommande)

@bot.command(pass_context=True)
async def test(ctx, *arg):
    msg = ' '.join(arg)
    return await bot.say(msg)
descriptionCommande = "Répond par votre message, aussi."
descriptionAllCommandes.append(descriptionCommande)


@bot.command(pass_context=True)
async def help():

    embed = discord.Embed(color=0x2ecc71)
    embed.set_author(name="LES COMMANDES DE DIDIO\'MATIC", icon_url='https://image.noelshack.com/fichiers/2017/35/1/1503939867-trisomy-21-down-syndrome-kennedi-beahn-presented-by-kraig-beahn2.jpg')
    embed.set_thumbnail(url='http://icons.iconarchive.com/icons/graphicloads/100-flat/256/settings-3-icon.png')
    i = 0
    for key in bot.commands:
        NomAllCommande.append((key))
    while i<len(bot.commands):
        embed.add_field(name="?"+ NomAllCommande[i],value=descriptionAllCommandes[i], inline=True)
        i = i + 1


    return await bot.say(embed=embed)
descriptionCommande = "Vous affiche la liste des commandes."
descriptionAllCommandes.append(descriptionCommande)

bot.run('MzUwOTg4MDU5NjQwMjAxMjE2.DIMCow.7PxSQtuGb7t356bAY2D4gobB-60')
