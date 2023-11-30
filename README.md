# Gobblet AI Player
# Description
In this project, we will explore the game-playing of Gobblet, Gobblet is an abstract game
played on a 4x4 grid with each of the two players having twelve pieces that can nest on
top of one another to create three stacks of four pieces.
Your goal in Gobblet is to place four of your pieces in a horizontal, vertical, or diagonal
row. Your pieces start nested off the board. On a turn, you either play one exposed
piece from your three off-the-board piles or move one piece on the board to any other
spot on the board where it fits. A larger piece can cover any smaller piece. A piece
being played from off the board may not cover an opponent's piece unless it's in a row
where your opponent has three of his color.
Your memory is tested as you try to remember which color one of your larger pieces is
covering before you move it. As soon as a player has four like-colored pieces in a row,
he wins — except in one case: If you lift your piece and reveal an opponent's piece that
finishes a four-in-a-row, you don't immediately lose; you can't return the piece to its
starting location, but if you can place it over one of the opponent's three other pieces in
that row, the game continues..
# Project Directory Structure:

This is a simplified representation of a project directory structure for a data science project.

- **AI-Project/**: The main project directory.
  - **src/**: Python source code for the project.
    - **backend/**:
      - `__init__.py`
      - `player.py`
      - `game.py`
    - **module2/**:
      - `__init__.py`
      - `file1.py`
      - `file2.py`
    - **utils/**: Utility functions and configuration settings.
      - `config.py`
      - `logging_config.py`
      - `helper_functions.py`

  - **tests/**: Testing scripts and files for different project components.
    - `test_data.py`
    - `test_models.py`
    - `test_utils.py`

  - `requirements.txt`: List of Python packages and dependencies.
  - `README.md`: Project overview and instructions.


### Description

- **src/**: Python source code for the project, organized into subdirectories for moduls and utilities.
- **tests/**: Testing scripts and files for different project components.
- **requirements.txt**: A list of Python packages and dependencies.
- **README.md**: Project overview and instructions.


## Project Creation with Miniconda or Anaconda:

**Download Miniconda or Anaconda**:
   Visit the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) website and download the installer for your operating system (e.g., Windows, macOS, Linux). Choose the Python 3.x version.


### Managing `requirements.txt` in a Python Project

This guide provides steps for dealing with the `requirements.txt` file in your Python project, including its creation and updates.

1. **Create a Virtual Environment:**
   Before starting your project, consider creating a virtual environment to isolate dependencies:

   ```bash
   conda create --name myenv /path/to/requirements.txt
   ```
   Make sure to replace /path/to/requirements.txt with the actual path to your requirements.txt file.
2. **Activate the Conda Environment:**
    Activate the environment using the following command:
    ```bash
    conda activate myenv
    ```
3. **Verify Environment Creation:**
    You can verify that the environment has been created and that the packages specified in requirements.txt have been installed:
    ``` bash
    conda list
    ```
4. **Update Dependencies:**
    Whenever you install any packages using `pip` or `conda` 
    make sure to update `requirements.txt` file using:
    ```bash
    pip freeze > requirements.txt
    ```
    And commit the changes to `Github`
5. **Update existed env:**
    If you already have created the enviroment and need to update it from the `requirements.txt` file using this command:
    ```bash
    conda install --file path/to/requirements.txt
    ```
6. **Deactivate the Envirement:**
    deactivate the env when you're done:
    ```bash 
    conda deactiavte
    ```
