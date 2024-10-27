# Minecraft Crafty Controller
This repository is aimed at allowing a user to control CraftyController through a Discord Bot using Python. 

## How to Use
Using this application is very simple and easy. You will need:
- Discord Token from a Bot
- Admin Role
- IP Address
- Crafty Token
 
As well as some pip packages:
- discord
- dotenv
- crafty_client

After configuring the ``.env`` file correctly with the information above, as well as installing the pip packages, you should be free to run the server through the bot! Happy playing!

### Discord Bot & Token:
Make a bot in the [Discord Developer Portal](https://discord.com/developers/applications). Create your bot. In order to access your token, click the tab "Bot", and copy it. ==Never share it with anyone==. If it is leaked, or if your bot is acting strange, please reset your token immediately. Put your token after ``DISCORD_TOKEN`` in your .env file.

### Admin Role
Make a new role in your server. Go to Server Settings > Roles and press "Create Roll". The name of the role you choose to create is what you put in after ``ADMIN_ROLE`` in your .env file.

### IP Address
This is your IP Address or URL of your server. I'm expecting that this is self-hosted, in which your IP Address and Port of the location of CraftyController is needed. This might look like ``https://123.456.7.890:1234/``. Put this address after ``ADDRESS`` in your .env file.

### CraftyController
In order to get the token, you will need to go to Crafty Configuration (accessible through the gear icon on the top right corner) > edit user > API Keys, and CREATE A NEW API TOKEN. Pick a name, check all check boxes, and select full access at the end. After that, press "Get a Token" and copy the token displayed. Put this token after the ``CRAFTY_TOKEN`` in your .env file.

### Pip packages
There are three pip packages neccessary for the functioning of the bot. Use the following commands to install them:
- ``pip install discord.py`` -- Allows for the program to control the bot
- ``pip install python-dotenv`` -- Allows for the program to read the .env file
- ``pip install crafty-client`` -- Allows for the program to access CraftyController.

## Commands
*All commands here are slash commands.*
### Normal Commands:
>These commands can be used by anyone.

- `/start` -- Starts a minecraft server
- `/stop` -- Stops the minecraft server, given that there are no players active on the server.
- `/restart` -- Restarts the minecraft server, given that there are no players active on the server.
- `/status` -- Displays the status of the minecraft server, such as the IP address, port, version, and active players.
- `/say` -- Sends a message to all players on the server
- `/setserver` -- Designates a server in which all commands are sent to. This allows the discord server to access multiple minecraft servers.

### Special Commands:
> These commands can only be used by people with a special discord role. This special role can be set in the .env file.

- `/kill` -- Stops the server regardless of active players.
- `/save` -- Makes a backup in CraftyController.
- `/day` -- Sets the time to day
- `/tpcoordinates` -- Teleports a player to coordinates (x, y, z)
- `/tpplayers` -- Teleports one player to another.
- `/command` -- Allows the user to send the server a command.

## Future Plans & Issues
No plans so far, but feel free to submit some into issues. If you are having problems launching the program, or have questions in general, feel free to also submit them into issues, but please consult this document first. Be sure to tag your issues correctly!
