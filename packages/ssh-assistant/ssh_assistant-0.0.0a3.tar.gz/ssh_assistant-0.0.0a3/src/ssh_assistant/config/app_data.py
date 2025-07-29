from typing import Dict, List

from ssh_assistant.config.config import Config
from ssh_assistant.ssh_data.ssh_config_data import SSHConfigData


CONFIG: Config

# host: ssh-data
SSH_HOST_DICT: Dict[str, SSHConfigData]

# tag: list[ssh-data]
SSH_TAG_DICT: Dict[str, List[SSHConfigData]]
