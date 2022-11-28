# LibrarySpaceBookingSystem

To install all needed requirements:

1. Ensure you have python3 installed.

   - `python --version`

   - If you do not have python 3.X installed, please install it from python.org.

2. Ensure you have pip installed. If you install Python from source, you should already have pip.

   - `pip --version`

3. Install pipenv to manage a virtual environment.

   - Mac: `sudo pip install pipenv`

   - Windows: `pip install pipenv --user`

4. Start up your pipenv shell.

   - Mac: `pipenv shell`

   - Windows: `python -m pipenv shell`

   - If you are getting errors with this command, try installing pipenv again with `sudo pip install pipenv` and then running `pipenv shell` again.

5. To run the program:
   - `python -m mainMenu`

## [PIPENV] FOR DEVELOPERS:

- To delete/recreate pipenv shell:
  `pipenv --rm` (This deletes the virtual environment and its Pipfile)
  `pipenv install --python 3.X`

- To start up the pipenv shell:
  `pipenv shell`

- To install requirements into virtual environment:
  `pip install -r requirements.txt`

- To install a new requirement and add it to the Pipfile:
  `pipenv install <requirement>`

- To exit the virtual shell:
  `exit`

## [TESTING] FOR DEVELOPERS:

- To collect and run all pytests:
  Run `pytest` while in the main directory
