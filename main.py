import discord
from discord import app_commands
from drawing import generate_board
from data import units, players, unit_key, units_by_team, borders, place_unit
from my_utils import MoveButton, MySelect, ButtonInfo
from bot_server_info import TOKEN, server_id


# Define intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# x = [team, unit, moves, last_addition]
place_unit((10, 119), [1, 1, 4, 0])
place_unit((10, 120), [1, 2, 4, 0])
place_unit((10, 121), [1, 3, 6, 0])

for y in range(40, 100, 5):
    for x in range(10, 10, 4):
        place_unit((x, y), [1, 1, 4, 0])


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print(f'Logged in as {client.user.name}')


def get_team(disc_id):
    game_id = -1 if disc_id not in players else players.index(disc_id)
    return game_id


def create_team(disc_id):
    if get_team(disc_id) == -1:
        game_id = len(players)
        players.append(disc_id)
        return game_id


@tree.command(name="inspect", description="Inspect your armies", guild=discord.Object(id=server_id))
async def inspect_army(interaction: discord.Interaction):
    team_id = get_team(interaction.user.id)
    if team_id == -1:
        embed = discord.Embed(
            title="Player Does not Exist",
            description="Please use /joingame to join the game before attempting to play.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return

    embed = discord.Embed(
        title="Inspect Armies",
        description="Placeholder",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://example.com/sample.jpg")
    view = discord.ui.View()
    button_info = ButtonInfo(embed,
                             view,
                             interaction.user.id,
                             team_id)
    button_left = MoveButton("Left",
                             button_info,
                             label="<-",
                             style=discord.ButtonStyle.primary)
    button_right = MoveButton("Right",
                              button_info,
                              label="->",
                              style=discord.ButtonStyle.primary)
    button_up = MoveButton("Up",
                           button_info,
                           label="/|\\",
                           style=discord.ButtonStyle.primary)
    button_down = MoveButton("Down",
                             button_info,
                             label="\\|/",
                             style=discord.ButtonStyle.primary)

    options = []
    army_no = 1
    for _, unit, moves, last_add, _ in units_by_team[team_id]:
        options.append(
            discord.SelectOption(label=f"Army {army_no}", value=f"{army_no}", default=(army_no == 1))
        )
        if army_no == 1:
            embed.description = f"Army {army_no} ({unit_key[unit][0]}) has {moves} move(s) left!"
        army_no += 1

    button_info.options = options

    team_choose = MySelect(
        button_info,
        placeholder="Choose army to inspect...",
        min_values=1,
        max_values=1,
        options=options[:25]
    )
    view.add_item(button_left)
    view.add_item(button_up)
    view.add_item(button_down)
    view.add_item(button_right)
    view.add_item(team_choose)
    if len(options) > 25:
        view.add_item(ListButton("Left",
                                  button_info,
                                  label="Previous Army List",
                                  style=discord.ButtonStyle.primary,
                                  row=3))
        view.add_item(ListButton("Right",
                                  button_info,
                                  label="Next Army List",
                                  style=discord.ButtonStyle.primary,
                                  row=3))


    army_no = 1
    img = generate_board(units_by_team[team_id][army_no - 1][0])

    file = discord.File('images/board.png', filename="image.png")
    embed.set_image(url="attachment://image.png")

    await interaction.response.send_message(file=file, embed=embed, view=view)


# Run the bot
client.run(TOKEN)

