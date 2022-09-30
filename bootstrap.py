import subprocess
from typing import List, Tuple
import src.constants as constants

PYTHON_CMD = "python3"
REQUIREMENTS_FILE_NAME = "requirements.txt"
VENV_FOLDER_NAME = ".venv"

ENVIRONMENT_VAR_FILE_NAME = ".env"

SRC_DIR = "src"
ENV_VAR_PYTHONPATH = "PYTHONPATH"

NEWLINE = "\n"


def create_venv():
    """ Creates virtual environment with name given from constant. """

    command = f"{PYTHON_CMD} -m venv {VENV_FOLDER_NAME}"

    print(f"Executing command '{command}'.")
    execute_command(command)


def upgrade_pip():
    """ Upgrades pip. """

    command = "pip install --upgrade pip"

    print(f"Executing command '{command}'.")
    execute_command(command)


def install_dependencies():
    """ Installs dependencies from requirements file. 

        Make sure to have activated the virtual environment before executing this.

        See https://docs.python.org/3/library/venv.html for more."""

    command = f"pip install -r {REQUIREMENTS_FILE_NAME}"

    print(f"Executing command '{command}'.")
    execute_command(command)


def execute_command(command: str):
    """ Executes the given command. """

    try:
        subprocess.run([command], shell=True, check=True)
    except CalledProcessError as e:
        print(f"Command '{command}' returned error code '{e.returncode}'.")


def args_given(args: List[Tuple[str, bool]]):
    """ Checks whether at least one argument was given out of a list of boolean arguments. """

    for (_, arg_was_given) in args:
        assert type(arg_was_given) == bool
        if arg_was_given == True:
            return True
    return False


def create_env_file_template(env_file_name=".env_44"):
    """ Creates an empty `.env` file that can be populated with data afterwards. 
        This data will be used in the program."""

    template = build_template()

    print(f"Created template:")
    print(f"{template}")

    succeeded = write_to_file(env_file_name, template)

    if succeeded:
        print("Wrote template to file.")
    else:
        print(f"Aborting. File already exists. Delete the file and try again or adjust it manually.")


def build_template():
    """ Builds `.env` file templte. """

    template = ""
    template += f"{ENV_VAR_PYTHONPATH}=\"{SRC_DIR}\" {NEWLINE}"
    template += f"{constants.DB_USER_NAME}=\"\" {NEWLINE}"
    template += f"{constants.DB_PASSWORD}=\"\" {NEWLINE}"
    template += f"{constants.DB_HOST}=\"\" {NEWLINE}"
    template += f"{constants.DB_NAME}=\"\" {NEWLINE}"

    return template


def write_to_file(file_name: str, file_content: str):
    """ Writes content to file. Returns status on the success of the operation. """

    from pathlib import Path
    import os

    status = False

    root_path = Path(__file__).parent
    path_to_file = str(root_path.joinpath(file_name))

    print(f"Using file: '{path_to_file}'.")

    if not os.path.exists(path_to_file):
        file_handle = open(file_name, "w")
        file_handle.write(file_content)
        file_handle.close()
        status = True

    return status


if __name__ == "__main__":
    import argparse
    argparse = argparse.ArgumentParser("Setup helper.")
    argparse.add_argument("--create-venv", dest="create_venv", action='store_true',
                          help="Creates a virtual environment in project root.")
    argparse.add_argument("--upgrade-pip", dest="upgrade_pip", action='store_true', help="Upgrades pip.")
    argparse.add_argument("--install-dependencies", dest="install_dependencies",
                          action='store_true', help="Installs dependencies from requirements file.")
    argparse.add_argument("--scaffold-env-file", dest="scaffold_env_file",
                          action='store_true', help="Creates a template for `.env` file.")

    args = argparse.parse_args()

    if args.create_venv:
        create_venv()

    if args.upgrade_pip:
        upgrade_pip()

    if args.install_dependencies:
        install_dependencies()

    if args.scaffold_env_file:
        create_env_file_template()

    arg_lst = list(args.__dict__.items())
    if not args_given(arg_lst):
        print("Got no arguments. Add '-h' as argument for help.")
        print("Terminating...")
