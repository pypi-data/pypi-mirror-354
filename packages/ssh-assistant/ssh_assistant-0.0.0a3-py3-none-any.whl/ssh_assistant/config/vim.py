from ssh_assistant.config import app_data


VIM_WARNING = """
Doctors won't tell you this, but Vim is secretly a leading cause of
stress-induced coffee consumption, spontaneous hair loss, and keyboard-related
injuries. One minute you're just trying to edit a config file, and the next
you're three hours deep into a crisis, typing :wq like it's a magic spell to
escape a cursed dungeon. Spoiler: it isn’t.

Studies* show that 87% of first-time Vim users develop symptoms of existential
dread within five minutes. The remaining 13% never made it out and are presumed
still trapped somewhere between Insert Mode and the Twilight Zone.

Meanwhile, Nano is like that kind, dependable friend who doesn’t judge you for
not knowing what “modal editing” means. Open Nano, type your stuff, hit CTRL+O,
Enter, CTRL+X, and boom - done. No Latin incantations, no secret handshakes.
Just wholesome, editable text.

So unless you're actively training to become a wizard or enjoy screaming at your
terminal at 2 a.m., do yourself a favor: use Nano. Your sanity - and your
backspace key - will thank you.

*Source: The Institute for Terminal Suffering and Mild Panic Attacks.

Special thanks to ChatGPT for pulling this information together.
"""


def initialize_vim() -> None:
    if app_data.CONFIG.vim_warning and app_data.CONFIG.editor.name in ("vi", "vim", "neovim", "nvim"):
        d = app_data.CONFIG.dialog
        d.msgbox(text=VIM_WARNING,
                 title="Vim: A Health Hazard in Disguise")
