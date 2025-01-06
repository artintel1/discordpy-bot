# This example requires the 'message_content' privileged intents

import os
import requests
import discord
from discord.ext import commands

# GLIF Simple API endpoint
GLIF_API_URL = "https://simple-api.glif.app"

# Function to call the GLIF API
def generate_image(prompt):
    # Hardcoded aspect ratio (9:16)
    aspect_ratio = "9:16"
    
    # Prepare the payload for the GLIF API
    payload = {
        "id": "cm3ugmzv2002gnckiosrwk6xi",  # GLIF ID
        "inputs": [prompt, aspect_ratio]  # Passing the prompt and the fixed aspect ratio
    }

    # Set up headers with the API token
    headers = {
        "Authorization": f"Bearer {os.getenv('GLIF_API_KEY')}"
    }

    # Make the request to the GLIF API
    response = requests.post(GLIF_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # Parse the response
        response_data = response.json()
        if "output" in response_data:
            # Return the image URL
            return response_data["output"]
        elif "error" in response_data:
            # Handle errors (even though the status code is 200)
            return f"Error: {response_data['error']}"
    else:
        return f"API request failed with status code: {response.status_code}"

# Initialize the bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
    await ctx.send("Choo choo! 🚅")

@bot.command()
async def generate(ctx, *, prompt: str):
    """Generate an image based on the provided prompt using the GLIF API."""
    await ctx.send(f"Generating image for prompt: '{prompt}'...")
    
    # Call the GLIF API to generate the image
    image_url = generate_image(prompt)
    
    if image_url.startswith("http"):
        # Successfully generated the image
        await ctx.send(image_url)
    else:
        # Handle errors from the GLIF API
        await ctx.send(f"Failed to generate image: {image_url}")

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
