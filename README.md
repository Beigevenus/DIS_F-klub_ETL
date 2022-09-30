# DIS_F-klub_ETL

## Setup

```zsh
# Create a virtual environment.
python3 bootstrap.py --create-venv

# Activate the virtual environment manually (see https://docs.python.org/3/library/venv.html for help on this).

# After activation of virtual environment, install dependencies as follows.
python3 bootstrap.py --install-dependencies

# Optionally, upgrade pip.
python3 bootstrap.py --upgrade-pip

# Lastly, create a default `.env` file for configuring parts of the program.
python bootstrap.py --scaffold-env-file
```

