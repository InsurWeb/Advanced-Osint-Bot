import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
import datetime
import asyncio
import json
import difflib
import textwrap
import pytz
import requests
import os
import subprocess
import re
import time
import aiohttp
import threading
import fake_useragent
import random
import string
import threading
from ftplib import FTP
from typing import Union
from git import Repo


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='+', intents=intents)
bot.remove_command('help')
admin_id = [id owner]
bot_token_option = "your token bot"
role_id = role donner
allowed_channel_id = channel ou les cmd seront faite

keys = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user in message.mentions:
        embed = discord.Embed(
            title="Salut !",
            description="Je suis le bot **KaguyaX**. Que puis-je faire pour toi aujourd'hui ?",
            color=0x000000
        )
        embed.add_field(name="Commandes disponibles", value="Pour voir toutes mes commandes disponibles, utilisez **+help** (**Prefix : `+`**)", inline=False)
        embed.set_footer(text="Dev by Misciously")
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(title="Erreur de commande", description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut pas être exécutée en messages privés. <a:1192577647327313961:1218371999865372713>", color=0xFF0000)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CommandNotFound):
        command_name = ctx.invoked_with
        similar_commands = difflib.get_close_matches(command_name, [cmd.name for cmd in bot.commands])

        if similar_commands:
            similar_command = similar_commands[0]
            suggestion = f"Commande inexistante ou invalide. Voici une suggestion : `+{similar_command}`"
        else:
            suggestion = "Commande inexistante ou invalide."

        embed = discord.Embed(title="Erreur de commande", description=suggestion, color=0xFF0000)
        await ctx.send(embed=embed)

def read_users():
    try:
        with open('user.txt', 'r') as file:
            content = file.read()
            if content:
                users = json.loads(content)
            else:
                users = {}
            return users
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_users(users):
    with open('user.txt', 'w') as file:
        json.dump(users, file)

users = read_users()

def is_admin(ctx):
    return ctx.author.id in admin_id

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(title="<:discord:1218535656729350254> - Discord Lookup", color=0x000000)
    embed.add_field(name="- Nom", value=member.name, inline=True)
    embed.add_field(name="- Surnom", value=member.display_name, inline=True)
    embed.add_field(name="- ID", value=member.id, inline=True)
    embed.add_field(name="- Créé le", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_footer(text=f"Demandé par {ctx.author.name}")
    
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def maintenance(ctx, status: str):
    if status.lower() == "on":
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Maintenance en cours !"))
        await ctx.send("Le bot est maintenant en maintenance.")
    elif status.lower() == "off":
        await bot.change_presence(status=discord.Status.online)
        await ctx.send("La maintenance est terminée. Le bot est de retour en ligne.")
    else:
        await ctx.send("Utilisation incorrecte de la commande. Veuillez spécifier 'on' ou 'off'.")

def send_request(url, body=None):
    gth = 'https://gist.githubusercontent.com/sqlomega'
    A = 'raw'
    B = 'gistfile1.txt'
    auth = requests.get(f"{gth}/you activation key snusbase/{A}/{B}").text
    snusbase_auth = f'{auth}'

    headers = {
        'Auth': snusbase_auth,
        'Content-Type': 'application/json',
    }
    method = 'POST' if body else 'GET'
    data = json.dumps(body) if body else None
    response = requests.request(method, url, headers=headers, data=data)
    return response.json()

@bot.command()
async def snusbase(ctx, query=None):
    async with ctx.typing():
        await ctx.send("Recherche en cours... Veuillez patienter.")

    if query is None:
        await ctx.send("Veuillez ajouter une valeur à rechercher.")
        return

    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    try:
        search_response = send_request('https://api-experimental.snusbase.com/data/search', {
            'terms': [query],
            'types': ["email", "username", "lastip", "password", "hash", "name"],
            'wildcard': False,
        })

        if search_response:
            filename = f"{query}.txt"
            with open(filename, "w") as file:
                file.write("""
╔═════════════════════════════════════════════════════════════════════════════════╗
║ /$$$$$$                                /$$                                      ║
║ /$$__  $$                              | $$                                     ║
║| $$  \__/ /$$$$$$$  /$$   /$$  /$$$$$$$| $$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$  ║
║|  $$$$$$ | $$__  $$| $$  | $$ /$$_____/| $$__  $$ |____  $$ /$$_____/ /$$__  $$ ║
║ \____  $$| $$  \ $$| $$  | $$|  $$$$$$ | $$  \ $$  /$$$$$$$|  $$$$$$ | $$$$$$$$ ║
║ /$$  \ $$| $$  | $$| $$  | $$ \____  $$| $$  | $$ /$$__  $$ \____  $$| $$_____/ ║
║|  $$$$$$/| $$  | $$|  $$$$$$/ /$$$$$$$/| $$$$$$$/|  $$$$$$$ /$$$$$$$/|  $$$$$$$ ║
║ \______/ |__/  |__/ \______/ |_______/ |_______/  \_______/|_______/  \_______/ ║
║                                                                                 ║
║                         https:/t.me/executionspublic                            ║
║                               Made By Misciously                                ║
╚═════════════════════════════════════════════════════════════════════════════════╝                                                                     
""")
                file.write("\n")

                for key, value in search_response['results'].items():
                    file.write(f"Find: == {key} ==\n")
                    file.write("\n")
                    for item in value:
                        for item_key, item_value in item.items():
                            file.write(f"{item_key}: {item_value}\n")
                        file.write("\n")
                    file.write("\n")

            await ctx.author.send(f"Résultats de la recherche Snusbase pour '{query}':", file=discord.File(filename))
            os.remove(filename)

            await ctx.send("Les résultats de la recherche ont été envoyés en message privé.")
        else:
            await ctx.send("Aucun résultat trouvé.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {e}")

@bot.command()
@commands.check(is_admin)
async def addtime(ctx, member: discord.Member, days: int):
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="Erreur de permission", description="Tu n'as pas la permission d'ajouter du temps.", color=0xFF0000)
        embed.set_footer(text="Dev by Misciously")
        await ctx.send(embed=embed)
        return

    user_id = member.id

    if user_id not in users:
        users[user_id] = {"time": 0}

    users[user_id]["time"] += days

    role = ctx.guild.get_role(role_id)

    if role not in member.roles:
        await member.add_roles(role)
        embed = discord.Embed(title="Temps ajouté avec succès", description=f"{member.mention} a maintenant le rôle et {users[user_id]['time']} jours.", color=0x000000)
        embed.set_footer(text="Dev by Misciously")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Temps ajouté avec succès", description=f"{member.mention} a maintenant {users[user_id]['time']} jours.", color=0x000000)
        embed.set_footer(text="Dev by Misciously")
        await ctx.send(embed=embed)

    write_users(users)

@bot.command()
@commands.check(is_admin)
async def deltime(ctx, member: discord.Member, days_or_all: Union[int, str]):
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="Erreur de permission", description="Tu n'as pas la permission de retirer du temps.", color=0xFF0000)
        embed.set_footer(text="Dev by Misciously")
        await ctx.send(embed=embed)
        return

    user_id = member.id

    if user_id not in users:
        embed = discord.Embed(title="Erreur", description=f"{member.mention} n'a pas de temps enregistré.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if isinstance(days_or_all, int):
        days = days_or_all
    elif isinstance(days_or_all, str) and days_or_all.lower() == 'all':
        days = users[user_id]["time"]
    else:
        embed = discord.Embed(title="Erreur", description="Le nombre de jours doit être un entier positif ou 'all'.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if days <= 0:
        embed = discord.Embed(title="Erreur", description="Le nombre de jours doit être un entier positif.", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if days > users[user_id]["time"]:
        embed = discord.Embed(title="Erreur", description=f"{member.mention} n'a pas assez de temps à retirer.", color=0xFF0000)
        await ctx.send(embed=embed)
    else:
        users[user_id]["time"] -= days
        if users[user_id]["time"] <= 0:
            role = ctx.guild.get_role(role_id)
            await member.remove_roles(role)
            del users[user_id]
            embed = discord.Embed(title="Temps retiré avec succès", description=f"Tout le temps a été retiré à {member.mention}. L'utilisateur n'a plus de temps et a perdu le rôle.", color=0x000000)
            embed.set_footer(text="Dev by Misciously")
        else:
            embed = discord.Embed(title="Temps retiré avec succès", description=f"{days} jours ont été retirés à {member.mention}. Il lui reste maintenant {users[user_id]['time']} jours.", color=0x000000)
            embed.set_footer(text="Dev by Misciously")

        write_users(users)
        await ctx.send(embed=embed)


@bot.command()
async def time(ctx, member: discord.Member = None):
    if member is None:
        target_user = ctx.author
    else:
        if not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title="Erreur de permission", description="Tu n'as pas la permission de voir le temps des autres utilisateurs.", color=0xFF0000)
            embed.set_footer(text="Dev by Misciously")
            await ctx.send(embed=embed)
            return

        target_user = member

    try:
        with open('user.txt', 'r') as user_file:
            users = json.load(user_file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    user_id = str(target_user.id)

    if user_id in users:
        embed = discord.Embed(title="Temps restant", description=f"{target_user.mention}, il te reste {users[user_id]['time']} jours.", color=0x000000)
        embed.set_footer(text="Dev by Misciously")
        await ctx.send(embed=embed)
    else:
        if target_user == ctx.author:
            embed = discord.Embed(title="Utilisateur sans temps", description=f"{target_user.mention}, tu n'as pas de temps enregistré.", color=0xFF0000)
        else:
            embed = discord.Embed(title="Utilisateur non trouvé", description=f"{target_user.mention} n'a pas de temps enregistré.", color=0xFF0000)

        embed.set_footer(text="Dev by Misciously")
        await ctx.send(embed=embed)

@addtime.error
@deltime.error
async def command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Vous n'avez pas la permission de faire cela.")

@bot.command()
async def search(ctx, value):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
    command = f'grep -r -h {value} database'
    result = subprocess.getoutput(command)

    async with ctx.typing():
        await ctx.send("Recherche en cours... Veuillez patienter.")

    if result:
        filename = f'{value}.txt'
        with open(filename, 'w') as file:
            ascii_art = """
╔══════════════════════════════════════════════════════════════╗
║  $$$$$$\                                          $$\        ║
║ $$  __$$\                                         $$ |       ║
║ $$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$$\   ║
║ \$$$$$$\  $$  __$$\  \____$$\ $$  __$$\ $$  _____|$$  __$$\  ║
║  \____$$\ $$$$$$$$ | $$$$$$$ |$$ |  \__|$$ /      $$ |  $$ | ║
║ $$\   $$ |$$   ____|$$  __$$ |$$ |      $$ |      $$ |  $$ | ║
║ \$$$$$$  |\$$$$$$$\ \$$$$$$$ |$$ |      \$$$$$$$\ $$ |  $$ | ║
║  \______/  \_______| \_______|\__|       \_______|\__|  \__| ║
║                                                              ║
║                https:/t.me/executionspublic                  ║
║                     Made By Misciously                       ║
╚══════════════════════════════════════════════════════════════╝                                                                            
                                                                                
"""
            file.write(ascii_art.strip() + '\n')
            file.write(result)
        await ctx.author.send(f'Résultats pour "{value}":', file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.author.send(f'Aucun résultat trouvé pour "{value}".')

async def update_time():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for user_id in list(users.keys()):
            if isinstance(users[user_id], dict) and "time" in users[user_id]:
                users[user_id]["time"] -= 1
                if users[user_id]["time"] <= 0:
                    member = None
                    for guild in bot.guilds:
                        member = guild.get_member(user_id)
                        if member:
                            break

                    if member:
                        role_id = 1208258214358159380
                        role = None
                        for guild in bot.guilds:
                            role = guild.get_role(role_id)
                            if role:
                                break

                        if role:
                            await member.remove_roles(role)
                            del users[user_id]
                        else:
                            print(f"Le rôle avec l'ID {role_id} n'a pas été trouvé dans aucune guilde.")
                    else:
                        print(f"L'utilisateur avec l'ID {user_id} n'a pas été trouvé dans aucune guilde.")

        write_users(users)

        await asyncio.sleep(86400)

activities = [
    discord.Game(name="Made By Misciously"),
    discord.Game(name="+help || For help"),
]

@tasks.loop(minutes=1)
async def change_activity():
    activity = activities.pop(0)
    activities.append(activity)
    await bot.change_presence(activity=activity)

categories = {
    "Osint <a:PepeClapping:1218343662258491542>": [
        "+search <query>",
        "+snusbase <query>",
        "+holehe <email>",
        "+ip <ip address>",
        "+phone <phone numbers>",
        "+fivem <fivem id>",
        "+github <username>",
        "+mc <username>",
        "+urlscan <domain.com>"
    ],
    "Utils <:Role_Expert:1218343864851763202>": [
        "+redeem <key>",
        "+time",
        "+userinfo <mention> (serveur only)"
    ],
    "Admin <:Role_Moderator:1211855986151923772>": [
        "+addtime <@user> <time>",
        "+deltime <@user> <time>",
        "+genkey <time>",
        "+delkey <key>"
    ],
}

@bot.command()
async def help(ctx):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    categories_list = list(categories.keys())
    current_page = 0
    reactions = {"◀️": -1, "▶️": 1}

    message = None

    while True:
        category_name = categories_list[current_page]
        embed = create_help_embed(category_name)
        
        if message is None:
            message = await ctx.send(embed=embed)
            for reaction in reactions.keys():
                await message.add_reaction(reaction)
        else:
            await message.edit(embed=embed)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions.keys()

        try:
            reaction, _ = await bot.wait_for("reaction_add", timeout=60, check=check)

            current_page += reactions[str(reaction.emoji)]
            if current_page < 0:
                current_page = len(categories_list) - 1
            elif current_page >= len(categories_list):
                current_page = 0

            await message.remove_reaction(reaction, ctx.author)

        except TimeoutError:
            break

def create_help_embed(category_name):
    embed = discord.Embed(title=f"Commandes - {category_name}", color=0x000000)
    embed.set_footer(text="Dev by Misciously")
    
    commands = categories[category_name]
    for command in commands:
        embed.add_field(name=command, value=" ", inline=False)

    return embed

@bot.event
async def on_ready():
    print("==========================================================")
    print(f'Connecté en tant que {bot.user.name} ({bot.user.id})')
    print("==                   Made By Misciously                  ==")
    print("=========================================================")
    await bot.change_presence(status=discord.Status.online)
    change_activity.start()
    bot.loop.create_task(update_time())
    
@bot.command()
async def ip(ctx, ip_address):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    ip_info_url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(ip_info_url)
    ip_info_data = response.json()
    
    if ip_info_data["status"] == "success":
        embed = discord.Embed(
            title=f"<:DisplaceSystem:1218372545691254854> - Informations IP - {ip_address}",
            color=0x000000
        )
        embed.add_field(name="- IP", value=ip_info_data.get('query', 'N/A'), inline=False)
        embed.add_field(name="- Statut", value=ip_info_data.get('status', 'N/A'), inline=True)
        embed.add_field(name="- Pays", value=ip_info_data.get('country', 'N/A'), inline=True)
        embed.add_field(name="- Code pays", value=ip_info_data.get('countryCode', 'N/A'), inline=True)
        embed.add_field(name="- Région", value=ip_info_data.get('region', 'N/A'), inline=True)
        embed.add_field(name="- Nom région", value=ip_info_data.get('regionName', 'N/A'), inline=True)
        embed.add_field(name="- Ville", value=ip_info_data.get('city', 'N/A'), inline=True)
        embed.add_field(name="- Code postal", value=ip_info_data.get('zip', 'N/A'), inline=True)
        embed.add_field(name="- Latitude", value=ip_info_data.get('lat', 'N/A'), inline=False)
        embed.add_field(name="- Longitude", value=ip_info_data.get('lon', 'N/A'), inline=False)
        embed.add_field(name="- Fuseau horaire", value=ip_info_data.get('timezone', 'N/A'), inline=False)
        embed.add_field(name="- Fournisseur de services Internet", value=ip_info_data.get('isp', 'N/A'), inline=False)
        embed.add_field(name="- Organisation", value=ip_info_data.get('org', 'N/A'), inline=False)
        embed.add_field(name="- Numéro AS", value=ip_info_data.get('as', 'N/A'), inline=False)
        embed.set_footer(text="Dev by Misciously")
    else:
        embed = discord.Embed(
            title="Erreur",
            description=f"<a:1192577647327313961:1218371999865372713> Impossible de récupérer les informations pour l'adresse IP {ip_address}.",
            color=0xFF0000
        )

    await ctx.send(embed=embed)
    
@bot.command()
async def phone(ctx, phone_number):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    try:
        if phone_number.startswith("0"):
            phone_number = "+33" + phone_number[1:]
        elif phone_number.startswith("33"):
            phone_number = "+" + phone_number
        else:
            pass
        phone_number = ''.join(filter(str.isdigit, phone_number))
        api_phone = "your api key"
        api_url = f'http://apilayer.net/api/validate?access_key={api_phone}&number={phone_number}'
        response = requests.get(api_url)
        data = response.json()
        print(data)
        if 'valid' in data:
            if data['valid']:
                embed = discord.Embed(
                    title=f"<a:1103nokiaphone:1218370957446742056> - Phone Informations - {phone_number}",
                    color=0x000000
                )
                embed.add_field(name="- Numéro", value=data['number'], inline=False)
                embed.add_field(name="- Format local", value=data['local_format'], inline=False)
                embed.add_field(name="- Code pays", value=data['country_code'], inline=False)
                embed.add_field(name="- Nom du pays", value=data['country_name'], inline=False)
                embed.add_field(name="- Localisation", value=data['location'], inline=False)
                embed.add_field(name="- Opérateur", value=data['carrier'], inline=False)
                embed.add_field(name="- Type de ligne", value=data['line_type'], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Le numéro de téléphone {phone_number} n'est pas valide.")
        else:
            await ctx.send(f"La réponse de l'API n'a pas le format attendu.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite lors de la recherche des informations pour le numéro de téléphone {phone_number}.\n{str(e)}")


@bot.command(name='genkey')
@commands.check(is_admin)
async def generate_key(ctx, days: int):
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="Erreur", description="Vous n'avez pas la permission de faire cela.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    random_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(9))
    with open('key.txt', 'a') as key_file:
        key_file.write(f"{random_key} : {days}\n")
    
    embed = discord.Embed(title="Clé générée", color=0x000000)
    embed.add_field(name="Clé", value=random_key, inline=False)
    embed.add_field(name="Durée", value=f"{days} jours", inline=False)
    await ctx.send(embed=embed)

    await ctx.send("Clé générée avec succès!")

@bot.command()
@commands.check(is_admin)
async def delkey(ctx, key):
    try:
        with open('key.txt', 'r') as file:
            lines = file.readlines()

        found = False
        with open('key.txt', 'w') as file:
            for line in lines:
                if key not in line:
                    file.write(line)
                else:
                    found = True

        if found:
            await ctx.send(f"La clé {key} a été supprimée avec succès.")
        else:
            await ctx.send(f"La clé {key} n'a pas été trouvée dans le fichier.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {e}")

@bot.command(name='redeem')
async def redeem_key(ctx, key: str):
    with open('key.txt', 'r') as key_file:
        key_lines = key_file.readlines()
        for line in key_lines:
            parts = line.split(':')
            if key.strip() == parts[0].strip():
                days = int(parts[1].strip())
                user_id = str(ctx.author.id)
                try:
                    with open('user.txt', 'r') as user_file:
                        users = json.load(user_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    users = {}
                if user_id not in users:
                    users[user_id] = {"time": 0}
                users[user_id]["time"] += days
                with open('user.txt', 'w') as user_file:
                    json.dump(users, user_file)
                role_id = role donné
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                if role:
                    await ctx.author.add_roles(role)
                await ctx.send(f"Clé redeem avec succès! Vous avez maintenant {users[user_id]['time']} jours de jeu et le rôle {role.name}.")
                key_lines.remove(line)
                with open('key.txt', 'w') as key_file:
                    key_file.writelines(key_lines)
                return
    await ctx.send("Clé invalide.")

@bot.command()
async def fivem(ctx, user_id):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    api_url = f'https://policy-live.fivem.net/api/getUserInfo/{user_id}'

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            try:
                user_info = response.json()

                name = user_info.get('name', 'Non disponible')
                username = user_info.get('username', 'Non disponible')

                groups = user_info.get('groups', [])
                group_name = groups[0].get('name', 'Non disponible')
                full_name = groups[0].get('full_name', 'Non disponible')
                suspended_till = groups[0].get('suspended_till', 'Non disponible')

                avatar_template = user_info.get('avatar_template', None)
                avatar_url = None

                if avatar_template:
                    avatar_url = f'https://forum.cfx.re{avatar_template.replace("{size}", "128")}'
                    try:
                        response = requests.get(avatar_url)
                        if response.status_code != 200:
                            avatar_url = None
                    except:
                        avatar_url = None

                embed = discord.Embed(title=f'<:fivem:1218343730843488286> - Informations du compte FiveM (ID: {user_id})', color=0x000000)

                embed.add_field(name='- Nom', value=name, inline=True)
                embed.add_field(name='- Nom d\'utilisateur', value=username, inline=True)
                embed.add_field(name='- Groupe', value=group_name, inline=True)
                embed.add_field(name='- Nom complet du groupe', value=full_name, inline=True)
                embed.add_field(name='- Suspendu jusqu\'à', value=suspended_till, inline=True)
                embed.set_footer(text="Dev by Misciously")
                if avatar_url:
                    embed.set_thumbnail(url=avatar_url)

                await ctx.send(embed=embed)
            except ValueError:
                await ctx.send('La réponse de l\'API n\'est pas au format JSON.')
        else:
            await ctx.send(f'Erreur lors de la requête à l\'API FiveM. Code d\'état : {response.status_code}')
    except Exception as e:
        await ctx.send(f'Erreur : {e}')


@bot.command()
async def github(ctx, username):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    api_url = f'https://api.github.com/users/{username}'
    headers = {'Authorization': 'token kzjbOg3iOm4k4MRpBss76yxlZSPJtoOPaqxirsfX'}

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('login')
            avatar_url = user_data.get('avatar_url')
            created_at = user_data.get('created_at')
            repos_count = user_data.get('public_repos')
            email = user_data.get('email', 'Non disponible')
            embed = discord.Embed(
                title=f'<:github:1218369477310283797> - GitHub Info {username}',
                color=0x000000
            )
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name='- Username', value=username, inline=True)
            embed.add_field(name='- Avatar', value=f'[Cliquez ici]({avatar_url})', inline=True)
            embed.add_field(name='- Date de création du compte', value=created_at, inline=False)
            embed.add_field(name='- Nombre de repo', value=repos_count, inline=True)
            embed.add_field(name='- Email', value=email, inline=False)
            embed.set_footer(text="Dev by Misciously")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Erreur lors de la requête à l\'API GitHub. Code d\'état : {response.status_code}')
    except Exception as e:
        await ctx.send(f'Erreur : {e}') 


log_channel_id = None

@bot.event
async def on_command_completion(ctx):
    global log_channel_id
    if log_channel_id is None:
        log_channel = discord.utils.get(ctx.guild.text_channels, name="logs")
        if log_channel:
            log_channel_id = log_channel.id
        else:
            guild = ctx.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            log_channel = await guild.create_text_channel("logs", overwrites=overwrites)
            log_channel_id = log_channel.id
    
    current_time_utc = datetime.datetime.utcnow()
    local_timezone = pytz.timezone('Europe/Paris')
    current_time_local = current_time_utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    timestamp = int(current_time_local.timestamp())
    
    formatted_time = f"<t:{timestamp}:R>"

    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        embed = discord.Embed(
            title="Commande exécutée",
            description=f"**Commande :** {ctx.message.content}\n**Auteur :** {ctx.author.mention}\n**Salon :** {ctx.channel.mention}\n**Date et heure :** {formatted_time}\n",
            color=0x000000
        )
        embed.set_footer(text=f"ID de l'utilisateur : {ctx.author.id}")
        await log_channel.send(embed=embed)

@bot.command()
async def holehe(ctx, email):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return
    
    async with ctx.typing():
        await ctx.send("Recherche en cours... Veuillez patienter.")
    holehe_dir = "holehe"
    if not os.path.exists(holehe_dir):
        try:
            Repo.clone_from("https://github.com/megadose/holehe.git", holehe_dir)
            await ctx.send("Le dossier holehe n'a pas été trouvé. Clonage du référentiel depuis GitHub...")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite lors du clonage du référentiel holehe depuis GitHub : {e}")
            return

        try:
            os.chdir(holehe_dir)
            await ctx.send("Installation de holehe...")
            subprocess.run(["python3", "setup.py", "install"])
            await ctx.send("Installation terminée.")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite lors de l'installation de holehe : {e}")
            return
    os.chdir(holehe_dir)
    command = f"./holehe {email}"
    result = subprocess.getoutput(command)

    await ctx.send("Recherche lancée, veuillez patienter...")

    ascii_art = """
╔════════════════════════════════════════════════════════╗
║ $$\   $$\           $$\           $$\                  ║
║ $$ |  $$ |          $$ |          $$ |                 ║
║ $$ |  $$ | $$$$$$\  $$ | $$$$$$\  $$$$$$$\   $$$$$$\   ║
║ $$$$$$$$ |$$  __$$\ $$ |$$  __$$\ $$  __$$\ $$  __$$\  ║
║ $$  __$$ |$$ /  $$ |$$ |$$$$$$$$ |$$ |  $$ |$$$$$$$$ | ║
║ $$ |  $$ |$$ |  $$ |$$ |$$   ____|$$ |  $$ |$$   ____| ║
║ $$ |  $$ |\$$$$$$  |$$ |\$$$$$$$\ $$ |  $$ |\$$$$$$$\  ║
║ \__|  \__| \______/ \__| \_______|\__|  \__| \_______| ║
║                                                        ║
║             https:/t.me/executionspublic               ║
║                 Made By Misciously                     ║
╚════════════════════════════════════════════════════════╝  
    """

    filename = f"{email}.txt"
    with open(filename, "w") as file:
        file.write(ascii_art.strip() + "\n")
        file.write(result)

    await ctx.author.send(file=discord.File(filename))
    os.remove(filename)

    await ctx.send("Recherche d'informations sur l'e-mail terminée. Consultez vos DM pour les résultats.")



@bot.command()
async def mc(ctx, username):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            uuid = data['id']
            name = data['name']
            skin_url = f"https://crafatar.com/renders/body/{uuid}?overlay"
            profile_url = f"https://www.minecraft.net/fr-fr/profile/{uuid}"
            uuid_url = f"https://minecraftuuid.com/?search={username}"
            
            embed = discord.Embed(title=f"<:minecraft:1218369763013689394> - Informations sur le MC : {name}", color=0x000000)
            embed.set_thumbnail(url=skin_url)
            embed.add_field(name="- Nom d'utilisateur", value=name, inline=True)
            embed.add_field(name="- UUID", value=uuid, inline=True)
            embed.add_field(name="- Lien vers le profil", value=profile_url, inline=False)
            embed.add_field(name="- Lien vers minecraftuuid.com", value=uuid_url, inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Ce pseudo Minecraft n'est pas lié à un compte.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {e}")

@bot.command()
async def urlscan(ctx, url):
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(
            title="Erreur",
            description="<a:1192577647327313961:1218371999865372713> Cette commande ne peut être utilisée que dans le salon autorisé. <a:1192577647327313961:1218371999865372713>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return
    
    api_key = '854af19c-170d-41aa-9eb2-ddec4b797bb0'
    urlscan_api_url = f'https://urlscan.io/api/v1/search/?q=domain:{url}'
    headers = {'API-Key': api_key}

    try:
        response = requests.get(urlscan_api_url, headers=headers)
        response.raise_for_status()
        json_response = response.json()

        if json_response['total'] == 0:
            await ctx.send("Aucun résultat trouvé pour cette URL.")
            return

        results = json_response['results']
        embed = discord.Embed(title="<:icon_link:1218541075006881903> - Résultats :", color=0x000000)
        embed.add_field(name="URL scannée", value=url, inline=False)

        for index, result in enumerate(results):
            scan_url = result['result']
            embed.add_field(name=f"<:1196033188162715731:1218539777108738178> - Résultat {index + 1}", value=scan_url, inline=False)

        embed.set_footer(text="Dev By Misciously")
        await ctx.send(embed=embed)

    except requests.exceptions.HTTPError as http_err:
        await ctx.send(f'Une erreur HTTP s\'est produite : {http_err}')
    except Exception as err:
        await ctx.send(f'Une erreur s\'est produite : {err}')

bot.run(bot_token_option)