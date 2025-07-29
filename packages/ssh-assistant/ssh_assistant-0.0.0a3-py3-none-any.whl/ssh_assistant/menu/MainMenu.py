from typing import List
import subprocess
from ssh_assistant.menu.BaseMenu import BaseMenu
from ssh_assistant.menu.CategoriesMenu import CategoriesMenu
from ssh_assistant.config import app_data, vim


class MainMenu(BaseMenu):

    def __init__(self):
        super().__init__(title="Main Menu",
                         no_tags=True,
                         item_help=True,
                         cancel_label="Quit")

    def _build_choices_data(self) -> List[tuple]:
        cfg = app_data.CONFIG
        choices = []
        if len(app_data.SSH_HOST_DICT) > 0:
            choices.append(("ssh", "SSH to Servers", "Go through menu of servers, choose one to connect to and log in"))
        else:
            choices.append(("ssh", "NO: SSH to Servers", "No SSH entries found"))
        if app_data.CONFIG.editor is None:
            choices.append(("edit", "NO: Edit SSH Config File", "Text editor executable not found on system"))
        else:
            choices.append(("edit", "Edit SSH Config File", f"Edit the SSH Config File: {cfg.ssh_config_file}"))
        if app_data.CONFIG.man is None:
            choices.append(("man_ssh_cfg", "NO: Man page: SSH Config File", "man executable not found on system"))
        else:
            choices.append(("man_ssh_cfg", "Man page: SSH Config File", "Open and read the man page for the ssh config file"))
        choices.append(("about", "About SSH Assistant", "Information about SSH Assistant"))
        return choices

    def _process_selection(self, code: str, tag: str) -> bool:
        d = app_data.CONFIG.dialog
        if code in (d.CANCEL, d.ESC):
            return False
        elif code == d.OK:
            if tag == "edit":
                if app_data.CONFIG.editor is not None:
                    # If the editor is vim (or a variant), we need to do some initialization
                    # If the editor is not vim, it will just return
                    vim.initialize_vim()
                    self._edit_ssh_config_file()
                return True
            elif tag == "ssh":
                if len(app_data.SSH_HOST_DICT) > 0:
                    categories_menu = CategoriesMenu()
                    categories_menu.run()
                return True
            elif tag == "man_ssh_cfg":
                if app_data.CONFIG.man is not None:
                    subprocess.run(args=f"man ssh_config", shell=True)
                return True
            elif tag == "about":
                MainMenu._display_about_info()
                return True
            else:
                raise RuntimeError(f"Unexpected tag in MainMenu: {tag}")
        else:
            return False

    def _edit_ssh_config_file(self) -> None:
        cfg = app_data.CONFIG
        cmd = f'{cfg.editor} '
        cmd += f'"{cfg.ssh_config_file}"'
        subprocess.run(args=cmd, shell=True)
        from ssh_assistant.ssh_data.ssh_data_loader import load_ssh_data
        load_ssh_data()
        # Reload menu data in case it has changed
        self.choices_data = self._build_choices_data()


    @staticmethod
    def _display_about_info() -> None:
        from ssh_assistant.__about__ import __about_box__
        d = app_data.CONFIG.dialog
        d.scrollbox(text=__about_box__,
                    title="About SSH Assistant",
                    exit_label="OK")
