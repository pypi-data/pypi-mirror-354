import os, getpass, shutil, sys
from dataclasses import dataclass, field, InitVar
from pathlib import Path
from typing import Optional
from dialog import Dialog


########################################################################################################################
# Config Object
########################################################################################################################
@dataclass(init=True, repr=True, eq=False, order=False, frozen=False)
class Config:
    current_user: str = field(init=False, repr=True, compare=False, default=None)
    dialog: Dialog = field(init=False, repr=True, compare=False, default=None)
    editor: Optional[Path] = field(init=False, repr=True, compare=False, default=None)
    ssh: Path = field(init=False, repr=True, compare=False, default=None)
    sshpass: Optional[Path] = field(init=False, repr=True, compare=False, default=None)
    man: Optional[Path] = field(init=False, repr=True, compare=False, default=None)
    ssh_config_file: Path = field(init=False, repr=True, compare=False, default=None)
    vim_warning: bool = field(init=False, repr=False, compare=False, default=True)

    dialog_path: InitVar[str] = "dialog"
    ssh_config_file_path: InitVar[str] = str(Path.home()) + "/.ssh/config"
    editor_path: InitVar[Optional[str]] = os.getenv("EDITOR")
    ssh_path: InitVar[str] = "ssh"
    sshpass_path: InitVar[str] = "sshpass"
    man_path: InitVar[str] = "man"

    def __post_init__(self,
                      dialog_path: str,
                      ssh_config_file_path: str,
                      editor_path: str,
                      ssh_path: str,
                      sshpass_path: str,
                      man_path: str):
        self.dialog = Config._initialize_dialog(dialog_path)
        self.ssh_config_file = Config._initialize_ssh_config_file(ssh_config_file_path)
        self.current_user = getpass.getuser()
        # The text editor is searched for in the following order, first found is the one used
        # 1. User-supplied editor
        # 2. Value of $EDITOR environment variable
        # 3. vim
        # 4. vi
        # 5. nano
        # 6. emacs
        if editor_path is not None:
            self.editor = Config._get_binary(editor_path, "Text Editor")
        if self.editor is None:
            self.editor = Config._get_binary("vim", "Text Editor")
        if self.editor is None:
            self.editor = Config._get_binary("vi", "Text Editor")
        if self.editor is None:
            self.editor = Config._get_binary("none", "Text Editor")
        if self.editor is None:
            self.editor = Config._get_binary("emacs", "Text Editor")
        self.ssh = Config._get_binary(ssh_path, "SSH Executable", error=True)
        self.sshpass = Config._get_binary(sshpass_path, "SSH Password Executable")
        self.man = Config._get_binary(man_path, "Man Page Executable")

    # Initialization methods
    @staticmethod
    def _get_binary(binary_path: str, binary_desc: str, error=False) -> Optional[Path]:
        bin_path: Path
        bin_path_str = shutil.which(binary_path)
        if bin_path_str is not None:
            bin_path = Path(bin_path_str)
        else:
            bin_path = Path(binary_path).expanduser().resolve()
        if not bin_path.exists():
            if error:
                msg = f"{binary_desc} not found, exiting: {binary_path}"
                print(f"{msg}", file=sys.stderr)
                sys.exit(1)
            else:
                return None
        return bin_path

    @staticmethod
    def _initialize_dialog(dialog_path: str) -> Dialog:
        import dialog
        dlog: Dialog
        try:
            from ssh_assistant.__about__ import __version__
            dlog = Dialog(dialog=dialog_path, autowidgetsize=True)
            dlog.set_background_title(f"SSH Assistant v{__version__}")
            dlog.add_persistent_args(["--aspect", "15"])
            return dlog
        except dialog.ExecutableNotFound:
            msg = f"ERROR: Dialog binary not found, exiting: {dialog_path}"
            print(f"{msg}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def _initialize_ssh_config_file(ssh_config_file_path: str) -> Path:
        cfg_file: Path
        cfg_file = Path(ssh_config_file_path).expanduser().resolve()
        if not cfg_file.exists():
            msg = f"ERROR: SSH config file does not exist: {ssh_config_file_path}"
            print(f"{msg}", file=sys.stderr)
            sys.exit(1)
        return cfg_file


########################################################################################################################
# Load Config Data
########################################################################################################################
def load_config_data() -> Config:
    cfg: Config = Config(ssh_config_file_path=str(Path.home()) + "/.ssh/config")
    return cfg
