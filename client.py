import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import random as r
from typing import Optional


load_dotenv()


class RollBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.default())
        # self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def setup_hook(self) -> None:
        # Should really only need to supply the ID for development purposes.
        self.tree.copy_global_to(guild=discord.Object(id=os.getenv("id")))
        await self.tree.sync()

    # async def on_message(self, message):
    #     print(f"Message from {message.author}:{message.content}")

    def roll_results(self, player_input: str):
        result = 0
        indiv_results = []
        # Parse the roll
        count, sides = self.parse_roll(player_input)
        # Needed if someone inputs something that doesn't fit the criteria of the roll
        if count is None or sides is None:
            return None, None

        else:
            while count != 0:
                roll_result = r.randint(1, sides)
                result += roll_result
                indiv_results.append(roll_result)
                count -= 1
            return result, indiv_results

    def parse_roll(self, dice_str: str):
        if "d" in dice_str:
            parts = dice_str.split("d")
            # Todo should put in a check for a 0 d or 0 sides
            count = int(parts[0])
            sides = int(parts[1])
            return count, sides
        else:
            return None, None


bot = RollBot()

"""Roll command for dice roller."""


# Todo would it be better to ask for how many dice and the number of rolls rather than assuming the user knows what to do?
@bot.tree.command(
    name="roll", description="Supply a string with [Num]d[Num] and this will returning the resulting dice roll."
)
async def _roll(interaction: discord.Interaction, roll_amount: str, lowest_needed_roll: Optional[int] = None):
    try:
        result, indiv_roll = bot.roll_results(roll_amount)
        results_dict = {}

        for _ in indiv_roll:
            results_dict[_] = indiv_roll.count(_)

        # Create sorted dict for user readability
        sorted_dict = dict(sorted(results_dict.items()))  # Todo look into how this works

        if not lowest_needed_roll:
            await interaction.response.send_message(f"Total: {result}. Rolled: {sorted_dict}")
        else:
            # Show the hits
            hits = 0
            for key in results_dict.keys():
                if key >= lowest_needed_roll:
                    hits += results_dict[key]
                else:
                    continue
            # Todo maybe remove sorted dict as it makes the message long on large rolls.
            await interaction.response.send_message(f"Hits/Wounds: {hits} with the following rolls: {sorted_dict}")

    except Exception as e:
        print(e)
        return None


# Starts the bot
bot.run(os.getenv("token"))
