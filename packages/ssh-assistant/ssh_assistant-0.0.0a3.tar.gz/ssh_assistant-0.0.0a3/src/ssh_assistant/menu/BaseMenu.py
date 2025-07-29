from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, Dict
from ssh_assistant.config import app_data

class BaseMenu(ABC):

    def __init__(self,
                 title: str,
                 no_tags: bool,
                 item_help: bool,
                 text: str = "",
                 cancel_label: str = "Previous Menu",
                 extra_label: str = ""):
        self.title = title
        self.no_tags = no_tags
        self.item_help = item_help
        self.text = text
        self.cancel_label = cancel_label
        self.extra_label = extra_label
        self.choices_data = self._build_choices_data()


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = str(title)

    @property
    def no_tags(self) -> bool:
        return self._no_tags

    @no_tags.setter
    def no_tags(self, no_tags: bool):
        self._no_tags = bool(no_tags)

    @property
    def item_help(self) -> bool:
        return self._item_help

    @item_help.setter
    def item_help(self, item_help: bool):
        self._item_help = bool(item_help)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = str(text)

    @property
    def choices_data(self) -> List[tuple]:
        return self._choices_data

    @choices_data.setter
    def choices_data(self, choices_data: List[tuple]):
        self._choices_data = choices_data

    @property
    def cancel_label(self) -> str:
        return self._cancel_label

    @cancel_label.setter
    def cancel_label(self, cancel_label: str):
        self._cancel_label = str(cancel_label)

    @property
    def extra_label(self) -> str:
        return self._extra_label

    @extra_label.setter
    def extra_label(self, extra_label: str):
        self._extra_label = str(extra_label)

    def run(self):
        loop_menu = True
        while loop_menu:
            code, tag = self._show_menu()
            loop_menu = self._process_selection(code, tag)

    def _show_menu(self) -> Tuple[str, str]:
        d = app_data.CONFIG.dialog
        cmd_dict = {
            "title": self.title,
            "text": self.text,
            "choices": self.choices_data,
            "item_help": self.item_help,
            "no_tags": self.no_tags,
            "cancel_label": self.cancel_label}
        if self.extra_label != "":
            cmd_dict["extra_button"] = True
            cmd_dict["extra_label"] = self.extra_label
        code, tag = d.menu(**cmd_dict)
        return code, tag

    @abstractmethod
    def _build_choices_data(self) -> List[tuple]:
        pass

    @abstractmethod
    def _process_selection(self, code: str, tag: str) -> bool:
        pass
