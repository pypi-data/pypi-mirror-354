from pathlib import Path
from typing import List, Set
import re
from dataclasses import dataclass, field
from ssh_assistant import utils


@dataclass(init=True, repr=True, eq=True, order=True, frozen=False)
class SSHConfigData:
    ssh_raw_data: List[str] = field(init=True, repr=True, compare=False)
    ssh_host: str = field(init=True, repr=True, compare=True, default="")
    ssh_hostname: str = field(init=True, repr=True, compare=False, default="")
    ssh_user: str = field(init=True, repr=True, compare=False, default="")
    ssh_password_file: Path = field(init=True, repr=True, compare=False, default=None)
    menu_title: str = field(init=True, repr=True, compare=False, default="")
    menu_desc: str = field(init=True, repr=True, compare=False, default="")
    menu_tags: Set[str] = field(init=True, repr=True, compare=False, default_factory=set)

    def __post_init__(self):
        for line in self.ssh_raw_data:
            ln = line.strip()
            if len(ln) > 0:
                if ln.startswith("#"):
                    self._load_ssh_comment_line(ln)
                else:
                    self._load_ssh_non_comment_line(ln)

    def _load_ssh_comment_line(self, line: str):
        pattern = r'^(#\s*\[)([^\]]+)(\])(.+)$'
        match = re.match(pattern, line)
        if match:
            command_orig_case = match.group(2)
            command = command_orig_case.lower()
            data = match.group(4).strip()
            if command == "menutitle":
                self.menu_title = data
            elif command == "menudesc":
                self.menu_desc = data
            elif command == "menutags":
                tags = set([tag.strip() for tag in data.split(',')])
                self.menu_tags.update(tags)
            elif command == "passwordfile":
                file = Path(data).expanduser().resolve()
                if not file.exists():
                    utils.error_and_exit(f"Password file does not exist:\n\n{file}", 1)
                elif not file.is_file():
                    utils.error_and_exit(f"Password file is not a file:\n\n{file}", 1)
                else:
                    self.ssh_password_file = file
            else:
                utils.error_and_exit(f"Unknown SSH Config command:\n\n{command_orig_case}", 0)

    def _load_ssh_non_comment_line(self, line: str):
        line_parts = line.split()  # this handles multiple-spaces as 1 field separator
        line_parts[0] = line_parts[0].lower()
        if line_parts[0] == "host":
            self.ssh_host = line_parts[1]
        elif line_parts[0] == "hostname":
            self.ssh_hostname = line_parts[1]
        elif line_parts[0] == "user":
            self.ssh_user = line_parts[1]

    @property
    def is_ssh_entry(self) -> bool:
        if (self.ssh_host != "") and (len(self.menu_tags) > 0):
            return True
        return False
