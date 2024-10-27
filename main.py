# Import Everything
import discord
from discord import app_commands
from discord.ui import Select, View

from dotenv import load_dotenv
import os

from crafty_client import Crafty4

import ast

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Loads neccessary information from bot.env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN = os.getenv("ADMIN_ROLE")

URL = os.getenv("ADDRESS")
CRAFTYTOKEN = os.getenv("CRAFTY_TOKEN")

# Icky Bot Stuff
crafty = Crafty4(URL, CRAFTYTOKEN)
servers = crafty.list_mc_servers()

try:
    workingServerId = servers[0]["server_id"] # Sets the working server (server in which all commands from discord are sent) to the first one.
except:
    raise Exception("There are no servers in your crafty account. In order to proceed, please add one.")
    

nameToId = {}
for i in range(len(servers)):
    nameToId[servers[i]["server_name"]] = servers[i]["server_id"]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await tree.sync()


# Commands
@tree.command(name = "help", description = "Lists all the commands available on the bot.")
async def slash_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", description="List of available commands", color = discord.Color.blue())
    embed.add_field(name = "Normal Commands", value = "", inline = False)
    embed.add_field(name = "/start:", value = "Starts the minecraft server.", inline = False)
    embed.add_field(name = "/stop:", value = "Stops the minecraft server, provided that there are no active players.", inline = False)
    embed.add_field(name = "/restart:", value = "Restarts the minecraft server, provided that there are no active players.", inline = False)
    embed.add_field(name = "/status:", value = "Displays the status of the server, and lists all active players on the server", inline = False)
    embed.add_field(name = "/say:", value = "Sends a message to all players on the server.", inline = False)
    embed.add_field(name = "/setserver:", value = "Designates a server in which all commands are sent to.", inline = False)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Special Commands", value = "", inline = False)
    embed.add_field(name = "/kill:", value = "Immediately shuts down the server. May or may not make players mad.", inline = False)
    embed.add_field(name = "/save:", value = "Backs up the minecraft server. This is automated, however.", inline = False)
    embed.add_field(name = "/day:", value = "Sets time to day.", inline = False)
    embed.add_field(name = "/tpcoordinates:", value = "Teleports a player to coordinates (x, y, z).", inline = False)
    embed.add_field(name = "/tpplayers:", value = "Teleports a player to another player.", inline = False)
    embed.add_field(name = "/command:", value = "Sends a command to the terminal.", inline = False)

    await interaction.response.send_message(embed=embed)


@tree.command(name = "start", description = "Starts the minecraft server.")
async def slash_command(interaction: discord.Interaction):
    crafty.start_server(workingServerId)
    await interaction.response.send_message("Starting the minecraft server...")

@tree.command(name = "stop", description = "Stops the minecraft server, given that there are no players on the server.")
async def slash_command(interaction: discord.Interaction):
    if (crafty.get_server_stats(workingServerId)["online"] != 0):
        await interaction.response.send_message("Unable to stop, as there are still players on the server.")
    else:
        crafty.stop_server(workingServerId)
        await interaction.response.send_message("Stopping the minecraft server...")

@tree.command(name = "restart", description = "Restarts the minecraft server, given that there are no players on the server.")
async def slash_command(interaction: discord.Interaction):
    crafty.restart_server()
    await interaction.response.send_message("Restarting the minecraft server...")

@tree.command(name = "status", description = "List the status, as well as any active players on the server")
async def slash_command(interaction: discord.Interaction):
    serverinfo = crafty.get_server_stats(workingServerId)
    embed = discord.Embed(title=serverinfo["world_name"], color = discord.Color.blue())
    embed.add_field(name = "Online:  ", value = serverinfo["running"])
    embed.add_field(name = "World Type  ", value = serverinfo["server_id"]["type"])
    embed.add_field(name = "IP Address:  ", value = serverinfo["server_id"]["server_ip"])
    embed.add_field(name = "Port:  ", value = serverinfo["server_id"]["server_port"])
    embed.add_field(name = "Version:  ", value = serverinfo["version"])

    try:
        players = (', '.join(ast.literal_eval(serverinfo["players"])))
    except:
        players = "False"

    embed.add_field(name = "Players Online:  " + str(serverinfo["online"]), value = players)
    embed.add_field(name = "Updating:  ", value = serverinfo["updating"])
    embed.add_field(name = "Crashed:  ", value = serverinfo["crashed"])
    
    await interaction.response.send_message(embed = embed)

@tree.command(name = "say", description = "Sends a text message to all players on the server")
async def slash_command(interaction: discord.Interaction, command: str):
    crafty.run_command(workingServerId, f"/say {command}")
    await interaction.response.send_message("Executing command...")

@tree.command(name = "setserver", description = "Designates a server in which all commands are sent to. Also updates server list.")
async def slash_command(interaction: discord.Interaction):
    global servers
    global nameToId
    servers = crafty.list_mc_servers()

    nameToId = {}
    for i in range(len(servers)):
        nameToId[servers[i]["server_name"]] = servers[i]["server_id"]

    servernames = []

    for i in range(len(servers)):
        servernames.append(discord.SelectOption(label = servers[i]["server_name"]))

    select = Select(
        placeholder = "Choose a server in which commands are sent to:",
        options=servernames
    )

    async def select_callback(interaction: discord.Interaction):
        global workingServerId

        workingServerId = nameToId[select.values[0]]

        await interaction.response.send_message(f"Set the working server to ``{select.values[0]}``.")

    select.callback = select_callback

    view = View()
    view.add_item(select)

    for key, value in nameToId.items():
        if value == workingServerId:
            name = key
    embed = discord.Embed(title="Server", description=f"The working server is: {name}. To change the working server, please select from the dropdown menu below.", color = discord.Color.green())

    await interaction.response.send_message(embed = embed, view = view)

@tree.command(name = "kill", description = "Kills the minecraft server, regardless of any active players. Requires special permissions.")
async def slash_command(interaction: discord.Interaction):
    required_role = discord.utils.get(interaction.guild.roles, name = ADMIN)
    if required_role in interaction.user.roles:
        crafty.stop_server(workingServerId)
        await interaction.response.send_message("Killing the minecraft server...")
    else:
        await interaction.response.send_message("You do not have the required permissions to use this command.")

@tree.command(name = "save", description = "Backs up the server in the hard drive, just in case.")
async def slash_command(interaction: discord.Interaction):
    required_role = discord.utils.get(interaction.guild.roles, name = ADMIN)
    if required_role in interaction.user.roles:
        crafty.backup_server()
        await interaction.response.send_message("Backing up the server...")
    else:
        await interaction.response.send_message("You do not have the required permissions to use this command.")

@tree.command(name = "day", description = "Sets time to day. Requires special permissions.")
async def slash_command(interaction: discord.Interaction):
    required_role = discord.utils.get(interaction.guild.roles, name = ADMIN)
    if required_role in interaction.user.roles:
        crafty.run_command(server_id=workingServerId, cmd = "/time set day")
        await interaction.response.send_message("Setting time to day...")
    else:
        await interaction.response.send_message("You do not have the required permissions to use this command.")

@tree.command(name = "tpcoordinates", description = "Teleports a player to coordinates x, y, and z. Requires special permissions.")
async def slash_command(interaction: discord.Interaction, victimplayer: str, x_coordinate: int, y_coordinate: int, z_coordinate: int):
    required_role = discord.utils.get(interaction.guild.roles, name = ADMIN)
    if required_role in interaction.user.roles:
        crafty.run_command(server_id=workingServerId, cmd = f"/tp {victimplayer} {x_coordinate} {y_coordinate} {z_coordinate}")
        await interaction.response.send_message(f"Teleporting ``{victimplayer}`` to ``({x_coordinate}, {y_coordinate}, {z_coordinate})``")
    else:
        await interaction.response.send_message("You do not have the required permissions to use this command.")

@tree.command(name = "tpplayers", description = "Teleports a player to another player. Requires special permissions.")
async def slash_command(interaction: discord.Interaction, victimplayer: str, targetplayer: str):
    required_role = discord.utils.get(interaction.guild.roles, name = ADMIN)
    if required_role in interaction.user.roles:
        crafty.run_command(server_id=workingServerId, cmd = f"/tp {victimplayer} {targetplayer}")
        await interaction.response.send_message(f"Teleporting ``{victimplayer}`` to ``{targetplayer}``")
    else:
        await interaction.response.send_message("You do not have the required permissions to use this command.")

@tree.command(name = "command", description = "Inputs a command in a console. Requires special permissions.")
async def slash_command(interaction: discord.Interaction, command: str):
    required_role = discord.utils.get(interaction.guild.roles, name = ADMIN)
    if required_role in interaction.user.roles:
        crafty.run_command(serverid=workingServerId, cmd = f"/{command}")
        await interaction.response.send_message("Running command...")
    else:
        await interaction.response.send_message("You do not have the required permissions to use this command.")


# Run the bot
client.run(TOKEN)