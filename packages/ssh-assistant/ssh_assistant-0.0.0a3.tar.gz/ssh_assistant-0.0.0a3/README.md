# SSH Assistant

_SSH Assistant_ a set of utilities related to SSH.

## Pre-Requisites

* Required
  * ssh
  * dialog
* Recommended
  * sshpass
  * man
  * vim, nano, emacs, or other console text editor

## Installation Instructions

```text
pip install ssh-assistant
ssh-assistant
```

## SSH Menu

The main reason _SSH Assistant_ was created, this provides a full menu system around the Host entries in your
SSH Config file.

### SSH Menu: Features

* No need to keep a separate file for menu entries.
* _SSH Assistant_-specific statements look like comments to SSH.
* SSH Host entries are grouped by categories (tags).
* Utilize password files to avoid being prompted (and thus remembering) each password.

### SSH Menu: SSH Config File Commands

There are 4 _SSH Assistant_ commands you can put within the ```Host``` entries of you SSH config file. But, you only
need to add 1 tag entry to incorporate a SSH Host entry in to the menu. If you do not, the SSH Host entry will be
skipped.

Also note, there is a category called ```All``` which is automatically created for you, which contains all entries.

| Command                                   | Required | Description                                                                                                                                                                          |
|-------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ```# [MenuTitle] <text>```                | no       | Short description. This is the text that appears as the menu item. If this is not provided, the host entry name is used. The user that will be used to login is also displayed here. |
| ```# [MenuDesc] <text>```                 | no       | Long description. This is help text that appears at the bottom of the screen for the menu item. The host address is also shown here.                                                 |
| ```# [MenuTags] <comma-separated list>``` | yes      | A comma-separated list of categories (tags) to group the SSH host entries together. At least 1 tag is required, and it can be "All" if desired.                                      |
| ```# [PasswordFile] <filename>```         | no       | The file name passed to ```sshpass```. Note that you are responsible for storing this securely.                                                                                      |

### SSH Menu: Example SSH Entries in Config File

```text
# This is the minimum required for an entry to appear in the SSH Menu.
#   Menu entry text:  devws1 (current_user)
#   Menu help text:   (localhost)
#   Menu categories:  All
#   Password:         Will be prompted if needed
Host devws1
    Hostname localhost
    # [MenuTags] All


# This is an example using an SSH key for connection.
#   Menu entry text:  ProLUG Rocky 9.5 Home Server + (root)
#   Menu help text:   My personal Rocky Linux install for ProLUG labs (vm00)
#   Menu categories:  ProLUG, VirtualBox, Rocky Linux, All
#   Password:         Will be prompted if needed
Host vm00
    Hostname vm00
    User root
    IdentityFile ~/.ssh/id_ed25519
    # [MenuTags] ProLUG, VirtualBox, Rocky Linux
    # [MenuTitle] ProLUG Rocky 9.5 Home Server
    # [MenuDesc] My personal Rocky Linux install for ProLUG labs


# This is an example where a password file will be used with sshpass.
#   Menu entry text:  Proxmox 2 (root)
#   Menu help text:   (proxmox2)
#   Menu categories:  Bare Metal, Debian, All
#   Password:         Will be retrieved from file /home/joey/.ssh/passwords/proxmox2-root.pw
Host proxmox2
    Hostname proxmox2
    User root
    # [PasswordFile] /home/joey/.ssh/passwords/proxmox2-root.pw
    # [MenuTitle] Proxmox 2
    # [MenuTags]  Bare Metal, Debian
```

### SSH Menu: Common Menu Hotkeys

| Hotkey                                                 | Description                                                         |
|--------------------------------------------------------|---------------------------------------------------------------------|
| ```Tab```<br />```Left Arrow```<br />```Right Arrow``` | Move Between Buttons                                                |
| ```Esc```                                              | Go Back                                                             |
| ```Control + C```                                      | Quit Immediately                                                    |
| ```Enter```                                            | Select Menu Item                                                    |
| Letter Keys<br />```Up Arrow```<br />```Down Arrow```  | Navigate Between Menu Items                                         |
| Mouse Control                                          | Depending on your system setup, the mouse may work within the menus |

## Utility Features

* Edit your SSH config file with your favorite text editor.
* Pull up the man page for the SSH config file.
