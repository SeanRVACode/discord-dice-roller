import discord
from discord.app_commands import commands

from dotenv import load_dotenv
import os
from typing import Optional, Union
import random as r

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# bot = commands.Bot(command_prefix="/", intents=intents)


def roll_results(player_input: str):
    result = 0
    indiv_results = []

    count, sides = parse_roll(player_input)
    print(sides)
    if count is None or sides is None:
        return None, None

    else:
        while count != 0:
            roll_result = r.randint(1, sides)
            print(roll_result)
            result += roll_result
            indiv_results.append(roll_result)
            count -= 1
        return result, indiv_results


def parse_roll(dice_str: str):
    if "d" in dice_str:
        parts = dice_str.split("d")
        # Todo should put in a check for a 0 d or 0 sides
        count = int(parts[0])
        sides = int(parts[1])
        return count, sides
    else:
        return None, None


@commands.context_menu()
async def roll(ctx, player_input: str):
    try:
        result, indiv_roll = roll_results(player_input)
        results_dict = {}
        for _ in indiv_roll:
            results_dict[_] = indiv_roll.count(_)
        await ctx.send(f"Total: {result}. Rolled: {results_dict}")
    except Exception as e:
        print(e)
        return None


# Runs the bot using its token.
client.run(os.getenv("token"))
# bot.run(os.getenv("token"))
