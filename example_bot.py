import discord
from dotenv import load_dotenv
import os
from typing import Optional, Union
import random as r

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


# client.run(os.getenv("token"))


def roll(player_input: str):
    result = 0
    count, sides = parse_roll(player_input)
    print(sides)
    if count is None or sides is None:
        return None

    else:
        while count != 0:
            roll_result = r.randint(1, sides)
            print(roll_result)
            result += roll_result
            count -= 1
        return result


def parse_roll(dice_str: str):
    if "d" in dice_str:
        parts = dice_str.split("d")
        # Todo should put in a check for a 0 d or 0 sides
        count = int(parts[0])
        sides = int(parts[1])
        return count, sides
    else:
        return None, None


if __name__ == "__main__":
    result = roll("2d6")
    print(f"The result is: {result}")
