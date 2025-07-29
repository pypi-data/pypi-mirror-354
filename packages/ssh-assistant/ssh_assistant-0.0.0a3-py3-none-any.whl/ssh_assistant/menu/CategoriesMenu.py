from typing import List
from ssh_assistant.menu.BaseMenu import BaseMenu
from ssh_assistant.menu.SSHMenu import SSHMenu
from ssh_assistant.config import app_data


class CategoriesMenu(BaseMenu):

    def __init__(self):
        super().__init__(title="SSH Categories",
                         no_tags=True,
                         item_help=False)

    def _build_choices_data(self) -> List[tuple]:
        choices = []
        categories = []
        for tag in app_data.SSH_TAG_DICT.keys():
            categories.append(tag)
        categories.sort()
        for category in categories:
            choices.append((category, category))
        return choices


    def _process_selection(self, code: str, tag: str) -> bool:
        d = app_data.CONFIG.dialog
        if code in (d.CANCEL, d.ESC):
            return False
        elif code == d.OK:
            ssh_menu = SSHMenu(category=tag)
            ssh_menu.run()
            return True
        else:
            return False
