#!/usr/bin/env python
import discord, aiohttp, datetime
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from discord.errors import InvalidArgument, HTTPException
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


bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print("My body is ready")
    print(f"Logged in as: {bot.user}")
    
@bot.event
async def on_member_join(member):
    if member.bot: #If the member who join is a bot....
        if str(type(config['roles']['bot-roles'])) == "<class 'int'>":
            role = member.guild.get_role(config['roles']['user-roles'])
            if role != None:
                await member.add_roles(role, reason="BOT autorole")
                if config['webhook']['enabled']:
                    webhook_url = str(config['webhook']['url'])
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))

                        embed = discord.Embed(title=f"{member} is a bot", description=f"Bot detected, role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow()) #You can edit this embed message
                        try:
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                        except HTTPException:
                            print("Specify a valid image url on the config file")
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'])

            elif role == None:
                raise TypeError("You have to give me a valid id")
    
        elif str(type(config['roles']['bot-roles'])) == "<class 'list'>":
            role = member.guild.get_role(config['roles']['bot-roles'])
            if role != None:

                await member.add_roles(role, reason="BOT autorole")
                if config['webhook']['enabled']:
                    webhook_url = str(config['webhook']['url'])
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))

                        embed = discord.Embed(title=f"{member} is a bot", description=f"Bot detected, role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow()) #You can edit this embed message
                        try:
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                        except HTTPException:
                            print("Specify a valid image url on the config file")
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'])

            elif role == None:
                raise TypeError("You have to give me a valid id")
    
    elif not member.bot: #If the member who join is not a bot....
    
        if str(type(config['roles']['user-roles'])) == "<class 'int'>":
            role = member.guild.get_role(config['roles']['user-roles'])
            if role != None:

                await member.add_roles(role, reason="Autorole")
                if config['webhook']['enabled']:
                    webhook_url = str(config['webhook']['url'])
                    async with aiohttp.ClientSession() as session:
                        try:
                            webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))
                        except InvalidArgument:
                            print("Specify a valid webhook url")

                        embed = discord.Embed(title=f"{member} joined", description=f"Role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow()) #You can edit this embed message

                        try:
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                        except HTTPException:
                            print("Specify a valid image url on the config file")
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'])
                        
            elif role == None:
                raise TypeError("You have to give me a valid id")
        elif str(type(config['roles']['user-roles'])) == "<class 'list'>":
            for role_id in config['roles']['user-roles']:
                role = member.guild.get_role(role_id)
                if role != None:
                    await member.add_roles(role, reason="Autorole")
                    if config['webhook']['enabled']:
                    
                        webhook_url = str(config['webhook']['url'])
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(webhook_url , adapter=AsyncWebhookAdapter(session))

                            embed = discord.Embed(title=f"{member} joined", description=f"Role {role.mention} assigned", color=0x23cf4b,timestamp=datetime.datetime.utcnow()) #You can edit this embed message

                        try:
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'], avatar_url=config['webhook']['custom-image'])
                        except HTTPException:
                            print("Specify a valid image url on the config file")
                            await webhook.send(embed=embed, username=config['webhook']['custom-username'])
                elif role == None:
                    raise TypeError("You have to give me a valid id")
            


@bot.event
async def on_command_error(ctx, error): #Ignore errors on commands because we dont have any commands
    pass

bot.run(config['bot']['token']) #Just run the bot with the given token on config.json
