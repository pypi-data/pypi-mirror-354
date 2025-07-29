import locale, subprocess, sys

from ssh_assistant.config import config
from ssh_assistant.config import app_data
from ssh_assistant.ssh_data import ssh_data_loader
from ssh_assistant.menu.MainMenu import MainMenu


########################################################################################################################
# Main Program Logic
########################################################################################################################
def run():
    try:
        initialize()
        run_main_menu()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Detected")
    except Exception as e:
        raise e
    finally:
        finalize()
    sys.exit(0)


########################################################################################################################
# Run the program
########################################################################################################################
def run_main_menu():
    main_menu = MainMenu()
    main_menu.run()


########################################################################################################################
# Initialization
########################################################################################################################
def initialize():
    locale.setlocale(locale.LC_ALL, '')  # pythondialog docs strongly recommends this
    app_data.CONFIG = config.load_config_data()
    ssh_data_loader.load_ssh_data()


########################################################################################################################
# Finalization
########################################################################################################################
def finalize():
    print("\nSSH Assistant Ended\n")
    choice = input("Do you wish to clear the screen? (Y/n): ")
    if len(choice) > 0:
        choice = choice[0].lower()
    else:
        choice = "y"
    if choice == "y":
        subprocess.run(args="clear", shell=False)
