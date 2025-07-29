import sys
from ssh_assistant.config import app_data

def error_and_exit(msg: str, exit_code: int = 1) -> None:
    d = app_data.CONFIG.dialog
    d.msgbox(msg, title=">>>>> ERROR <<<<<")
    if exit_code > 0:
        sys.exit(exit_code)
