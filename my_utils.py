import math
import discord
from data import units, units_by_team, unit_key, unit_from_id, unit_id_from_id, delete_unit_from_id
from drawing import generate_board


class ButtonInfo:
    def __init__(self, embed, view, user_id, team_id, unit_id=0, list_id=0):
        self.embed = embed
        self.view = view
        self.user_id = user_id
        self.team_id = team_id
        self.options = None

        self.list_id = list_id

        self.unit_id = unit_id

        self.unit_unique_ids = {}
        # TODO: Implement self.units in the button/select functions to account for units that die in the middle of use
        i = 0
        for unit in units_by_team[team_id]:
            print(unit)
            self.unit_unique_ids[i] = unit[4]
            i += 1

    def get_unit(self, unit_id=None):
        self.update_unit_list()
        unit_id = self.unit_id if unit_id is None else unit_id
        if unit_id in self.unit_unique_ids:
            unit = unit_from_id(self.team_id, self.unit_unique_ids[unit_id])
            return unit
        else:
            return -1

    def get_unit_id(self):
        self.update_unit_list()
        if self.unit_id in self.unit_unique_ids:
            unit_id = unit_id_from_id(self.team_id, self.unit_unique_ids[self.unit_id])
            return unit_id
        else:
            return -1

    def update_unit_list(self):
        for uid in self.unit_unique_ids:
            if unit_from_id(self.team_id, self.unit_unique_ids[uid]) == -1:
                del self.unit_unique_ids[uid]


directions = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}


class MoveButton(discord.ui.Button):
    def __init__(self, direction, button_info: ButtonInfo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bi = button_info
        self.direction = direction

    async def callback(self, interaction: discord.Interaction):
        # What should happen when the button is clicked?
        if self.bi.user_id == interaction.user.id:
            unit_info = self.bi.get_unit()
            if unit_info != -1 and unit_info[2] > 0:
                old_x, old_y = unit_info[0]
                dx, dy = directions[self.direction]
                new_x, new_y = old_x + dx, old_y + dy
                try:
                    if units[new_x][new_y] != 0 and units[new_x][new_y][0] == self.bi.team_id:
                        await interaction.response.defer()
                        return
                except IndexError:
                    await interaction.response.defer()
                    return

                if units[new_x][new_y] != 0:
                    # Attack function
                    win_attack = True
                    if not win_attack:
                        units[old_x][old_y] = 0
                        units_by_team[self.bi.team_id].pop(self.bi.get_unit_id())
                        await interaction.response.defer()
                        return
                    pass

                units[old_x][old_y], units[new_x][new_y] = 0, units[old_x][old_y]
                units_by_team[self.bi.team_id][self.bi.get_unit_id()][0] = new_x, new_y

                img = generate_board(unit_info[0])

                unit_info[2] += 1

                file = discord.File('images/board.png', filename="image2.png")
                self.bi.embed.description = f"Army {self.bi.unit_id + 1} ({unit_key[unit_info[1]][0]}) has {unit_info[2]} move(s) left!"
                self.bi.embed.set_image(url="attachment://image2.png")
                await interaction.response.edit_message(embed=self.bi.embed, attachments=[file])
            else:
                await interaction.response.defer()


class ListButton(discord.ui.Button):
    def __init__(self, direction, button_info: ButtonInfo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bi = button_info
        self.direction = direction

    async def callback(self, interaction: discord.Interaction):
        # What should happen when the button is clicked?
        if self.bi.user_id == interaction.user.id:
            options = self.bi.options
            list_id = self.bi.list_id

            max_list_id = math.ceil(len(self.bi.unit_unique_ids) / 10) - 1

            if list_id > max_list_id:
                list_id = max_list_id
            elif 0 <= list_id < max_list_id and self.direction == "Right":
                list_id += 1
            elif 0 < list_id <= max_list_id and self.direction == "Left":
                list_id -= 1

            options_to_have = []
            # for i in

            unit_info = units_by_team[self.bi.team_id][self.bi.get_unit_id()]
            if unit_info != -1 and unit_info[2] > 0:
                old_x, old_y = unit_info[0]
                dx, dy = directions[self.direction]
                new_x, new_y = old_x + dx, old_y + dy
                try:
                    if units[new_x][new_y] != 0 and units[new_x][new_y][0] == self.bi.team_id:
                        await interaction.response.defer()
                        return
                except IndexError:
                    await interaction.response.defer()
                    return

                if units[new_x][new_y] != 0:
                    # Attack function
                    win_attack = True
                    if not win_attack:
                        units[old_x][old_y] = 0
                        units_by_team[self.bi.team_id].pop(self.bi.get_unit_id())
                        await interaction.response.defer()
                        return
                    pass

                units[old_x][old_y], units[new_x][new_y] = 0, units[old_x][old_y]
                units_by_team[self.bi.team_id][self.bi.get_unit_id()][0] = new_x, new_y
                try:
                    img = generate_board(units_by_team[self.bi.team_id][self.bi.get_unit_id()][0])
                except IndexError:
                    self.bi.unit_id -= 1
                    img = generate_board(units_by_team[self.bi.team_id][self.bi.get_unit_id()][0])

                unit_info[2] -= 1

                file = discord.File('images/board.png', filename="image2.png")
                self.bi.embed.description = f"Army {self.bi.unit_id + 1} ({unit_key[unit_info[1]][0]}) has {unit_info[2]} move(s) left!"
                self.bi.embed.set_image(url="attachment://image2.png")
                await interaction.response.edit_message(embed=self.bi.embed, attachments=[file])
            else:
                await interaction.response.defer()


class MySelect(discord.ui.Select):
    def __init__(self, button_info: ButtonInfo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bi = button_info

    async def callback(self, interaction: discord.Interaction):
        # What should happen when the select is changed?
        selected_value = int(self.values[0]) - 1
        self.bi.unit_id = selected_value
        unit_info = units_by_team[self.bi.team_id][self.bi.get_unit_id()]
        generate_board(units_by_team[self.bi.team_id][self.bi.get_unit_id()][0])

        file = discord.File('images/board.png', filename="image2.png")
        self.bi.embed.description = f"Army {self.bi.unit_id + 1} ({unit_key[unit_info[1]][0]}) has {unit_info[2]} move(s) left!"
        self.bi.embed.set_image(url="attachment://image2.png")

        # Update the select options to reflect the new selection
        for option in self.options:
            if option.value == self.values[0]:
                option.default = True
            else:
                option.default = False
        await interaction.response.edit_message(view=self.bi.view, embed=self.bi.embed, attachments=[file])
