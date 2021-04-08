#!/usr/bin/env python
import discord, aiohttp, datetime
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import json

with open("config.json") as configuration_file:
    config = json.load(configuration_file)

def get_prefix(bot, message):
    config_file = open("config.json")
    config = json.load(config_file)    
    config_file.close()
    return str(config['bot']['prefix'])


intents = discord.Intents.default()
intents.members = True
intents.reactions = True


bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print("My body is ready")
    print(f"Logged in as: {bot.user}")
    
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.event
async def on_member_join(member):
    if member.bot:
        try:

            for role_id in config['roles']['bot-roles']:
                role = member.guild.get_role(role_id)
                await member.add_roles(role, reason="BOT autorole")
                if config['webhook']['enabled']:
                    try:
                        webhook_url = str(config['webhook']['url'])


                        async with aiohttp.ClientSession() as session:

                            webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))

                            embed = discord.Embed(title=f"{member} is a bot", description=f"Bot detected, role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow())
                            if str(config['webhook']['custom-image']).startswith("https") or str(config['webhook']['custom-image']).startswith("http"):

                                await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                            else:
                                await webhook.send(embed=embed, username=config['webhook']['custom-username'])

                    except Exception as e:
                        print(e)
    
        except TypeError:
            role = member.guild.get_role(config['roles']['bot-roles'])
            await member.add_roles(role, reason="BOT autorole")
            if config['webhook']['enabled']:
                try:
                    webhook_url = str(config['webhook']['url'])


                    async with aiohttp.ClientSession() as session:

                        webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))

                        embed = discord.Embed(title=f"{member} is a bot", description=f"Bot detected, role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow())
                        if str(config['webhook']['custom-image']).startswith("https") or str(config['webhook']['custom-image']).startswith("http"):


                            await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                        else:
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'])

                except Exception as e:
                    print(e)

    elif not member.bot:
        try:


            for role_id in config['roles']['user-roles']:
                role = member.guild.get_role(role_id)
                await member.add_roles(role, reason="Autorole")
                if config['webhook']['enabled']:
                    try:
                        webhook_url = str(config['webhook']['url'])


                        async with aiohttp.ClientSession() as session:

                            webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))

                            embed = discord.Embed(title=f"{member} joined", description=f"Role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow())
                            if str(config['webhook']['custom-image']).startswith("https") or str(config['webhook']['custom-image']).startswith("http"):

                                await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                            else:
                                await webhook.send(embed=embed, username=config['webhook']['custom-username'])



                    except Exception as e:
                        print(e)
        except TypeError:
            role = member.guild.get_role(config['roles']['user-roles'])
            await member.add_roles(role, reason="Autorole")

            if config['webhook']['enabled']:
                try:
                    webhook_url = str(config['webhook']['url'])


                    async with aiohttp.ClientSession() as session:

                        webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))

                        embed = discord.Embed(title=f"{member} joined", description=f"Role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow())
                        if str(config['webhook']['custom-image']).startswith("https") or str(config['webhook']['custom-image']).startswith("http"):

                            await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                        else:
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'])



                except Exception as e:
                    print(e)


@bot.event
async def on_command_error(ctx, error):
    pass

bot.run(config['bot']['token'])
