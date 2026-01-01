import discord
from discord import app_commands
from discord.ext import commands
import flask # type: ignore
import threading

# -------------------------------
# Discord Bot Setup
# -------------------------------
TOKEN = "MTQ1NjA0NDE4MzI0MzQ1NjU3NA.GIZpyk.MThDhRb-BC6beg0zWTF6U4BZqBY2hbNqUWqlzo"  # <-- Put your Discord bot token here
ALLOWED_CHANNEL_ID = 1456062237822287972  # Only allow commands in this channel

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store the latest message from /run
latest_message = ""

# -------------------------------
# Flask Server Setup
# -------------------------------
app = flask.Flask(__name__)

@app.route("/get_message", methods=["GET"])
def get_message():
    # Return the latest message as JSON
    return flask.jsonify({"msg": latest_message})

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Start Flask in a separate thread
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# -------------------------------
# Discord Slash Command
# -------------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()  # sync slash commands with Discord
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.tree.command(name="runs", description="Execute Code !")
@app_commands.describe(msg="your code to execute blud")
async def run(interaction: discord.Interaction, msg: str):
    global latest_message

    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            "Hey Diddy Blud! Make sure to go to the Cmds channel to use the bot!", 
            ephemeral=True
        )
        return

   
    latest_message = msg
    await interaction.response.send_message(
        f"Executing your code: {msg}", 
        ephemeral=True
    )
    print(f"Message from {interaction.user}: {msg}")

bot.run(TOKEN)
