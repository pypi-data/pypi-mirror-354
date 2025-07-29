import subprocess
from typing import List
from ssh_assistant.menu.BaseMenu import BaseMenu
from ssh_assistant.config import app_data


class SSHMenu(BaseMenu):

    def __init__(self, category: str):
        self._category = category
        super().__init__(title=f"SSH Category: {category}",
                         no_tags=False,
                         item_help=True,
                         extra_label="Info")

    def _build_choices_data(self) -> List[tuple]:
        choices = []
        host_list = app_data.SSH_TAG_DICT[self._category]
        for host in host_list:
            menu_title = host.menu_title if host.menu_title != "" else host.ssh_host
            menu_user = host.ssh_user if host.ssh_user != "" else app_data.CONFIG.current_user
            menu_title += f" ({menu_user})"
            menu_desc = host.menu_desc
            if menu_desc != "":
                menu_desc += " "
            menu_desc += f"({host.ssh_hostname})"
            choices.append((host.ssh_host , menu_title, menu_desc))
        return choices

    def _process_selection(self, code: str, tag: str) -> bool:
        d = app_data.CONFIG.dialog
        if code in (d.CANCEL, d.ESC):
            return False
        elif code == d.OK:
            SSHMenu._ssh_to_host(host=tag)
            return True
        elif code == d.EXTRA:
            SSHMenu._show_raw_ssh_config_data(host=tag)
            return True
        else:
            return False

    @staticmethod
    def _ssh_to_host(host: str) -> None:
        ssh_cfg_file = app_data.CONFIG.ssh_config_file
        ssh_cfg_data = app_data.SSH_HOST_DICT[host]
        cmd = "clear; "
        if (ssh_cfg_data.ssh_password_file is not None) and (app_data.CONFIG.sshpass is not None):
            cmd += f'sshpass -f "{ssh_cfg_data.ssh_password_file}" '
        cmd += f'ssh -F "{ssh_cfg_file}" {ssh_cfg_data.ssh_host}'
        subprocess.run(args=cmd, shell=True)
        print()
        input("Press ENTER to return to SSH Assistant...")

    @staticmethod
    def _show_raw_ssh_config_data(host: str) -> None:
        d = app_data.CONFIG.dialog
        ssh_cfg_data_raw = app_data.SSH_HOST_DICT[host].ssh_raw_data
        text = ""
        for line in ssh_cfg_data_raw:
            text += line
        d.scrollbox(text=text,
                    title=f"RAW SSH Config Data For Host: {host}",
                    exit_label="OK")
