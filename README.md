# LibrarySpaceBookingSystem

## CREDENTIALS

- Find user login credentials for students and librarians in [storage/users.json]

## [Run] WITH DOCKER

1.  Run Docker Desktop

2.  Build image with:

    > `docker build -t "libmanagesystem:Dockerfile" .`

3.  Run image inside of a container using:

    > `docker run -v ~storage:/storage -it libmanagesystem:Dockerfile`

**Note:** Since this is a local applicaiton, all data is saved _with_ the image. If a new image is created, the data will _not_ carry over.

## [RUN] LOCALLY

To install all needed requirements:

1.  Ensure you have python3 installed.

    > `python --version`

- If you do not have python 3.X installed, please install it from python.org.

2.  Ensure you have pip installed. If you install Python from source, you should already have pip.

    > `pip --version`

3.  Install the required packages.

    > `pip install -r requirements.txt`

4.  To run the program:

    > `python mainMenu.py`

## [TESTING] FOR DEVELOPERS:

- To collect and run all pytests, run the following command in the main directory:

  > `python -m pytest`
