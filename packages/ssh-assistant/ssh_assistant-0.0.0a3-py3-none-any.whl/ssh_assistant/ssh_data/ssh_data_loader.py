import re
from pathlib import Path
from typing import List, Dict

from ssh_assistant.config import app_data
from ssh_assistant.ssh_data import ssh_config_data
from ssh_assistant import utils


def load_ssh_data():
    all_raw_data: List[List[str]] = _load_raw_ssh_config_data(app_data.CONFIG.ssh_config_file)
    all_ssh_data: List[ssh_config_data.SSHConfigData] = _create_ssh_config_data(all_raw_data)
    _load_ssh_host_dict(all_ssh_data)
    _load_ssh_tag_dict(all_ssh_data)


########################################################################################################################
# Loading / Creating raw SSH config data
########################################################################################################################
def _load_raw_ssh_config_data(ssh_config_file_path: Path) -> List[List[str]]:
    all_data = []
    with open(str(ssh_config_file_path), "r") as f:
        temp_ssh_section: List[str] = []
        for line in f:
            if _is_new_ssh_section(line):
                all_data.append(temp_ssh_section)
                temp_ssh_section = []
            if not _is_comment_line(line):
                temp_ssh_section.append(line)
    all_data.append(temp_ssh_section)
    return all_data


def _is_new_ssh_section(line: str) -> bool:
    ln = line.strip().lower()
    if (ln.startswith("host ")) or (ln.startswith("match ")):
        return True
    else:
        return False


def _is_comment_line(line: str) -> bool:
    ln = line.strip()
    if ln.startswith("#"):
        pattern = r'^(#\s*\[)([^\]]+)(\])(.+)$'
        match = re.match(pattern, ln)
        if match:
            return False
        else:
            return True
    else:
        return False


########################################################################################################################
# Create SSH Config Data Objects from raw data
########################################################################################################################
def _create_ssh_config_data(raw_data: List[List[str]]) -> List[ssh_config_data.SSHConfigData]:
    all_data: List[ssh_config_data.SSHConfigData] = []
    for section in raw_data:
        ssh_cfg: ssh_config_data.SSHConfigData = ssh_config_data.SSHConfigData(section)
        if ssh_cfg.is_ssh_entry:
            ssh_cfg.menu_tags.add("All")
            all_data.append(ssh_cfg)
    return all_data


########################################################################################################################
# Set application data
########################################################################################################################
def _load_ssh_host_dict(ssh_data_list: List[ssh_config_data.SSHConfigData]) -> None:
    ssh_dict: Dict[str, ssh_config_data.SSHConfigData] = {}
    for ssh_data in ssh_data_list:
        key = ssh_data.ssh_host
        if key in ssh_dict:
            utils.error_and_exit(f"Duplicate SSH Host Entry: {key}", 1)
        ssh_dict[key] = ssh_data
    app_data.SSH_HOST_DICT = ssh_dict


def _load_ssh_tag_dict(ssh_data_list: List[ssh_config_data.SSHConfigData]) -> None:
    ssh_dict: Dict[str, List[ssh_config_data.SSHConfigData]] = {}
    # load data in to dict
    for ssh_data in ssh_data_list:
        for tag in ssh_data.menu_tags:
            if tag not in ssh_dict:
                ssh_dict[tag] = []
            ssh_dict[tag].append(ssh_data)
    # sort tag data
    for tag in ssh_dict.keys():
        ssh_dict[tag].sort()
    app_data.SSH_TAG_DICT = ssh_dict
