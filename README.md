# LibrarySpaceBookingSystem 👩‍💻📚

This terminal application was created for CS 4471 at Western University by Connor Haines, Huda Mukhtar, Elaine Liu, and Calvin Dong. See our [final report](FinalReport.pdf).

**Video Demo:** https://www.youtube.com/watch?v=-WtSdmE6s1Y

**Update:** A new web version of this system has been created for CS 4474. See the [interactive report](https://mclhtay.github.io/CS4474-Final-Report/).

## [Run] APPLICATION WITH DOCKER

1. Run Docker Desktop

   - Docker Desktop can be installed at https://www.docker.com/products/docker-desktop/.

2. Pull the Docker image:

   > `docker pull hudamukhtar1/libspacemanagementsystem:latest`

3. Run application:

   > `docker run -v storage:/storage -it libspacemanagementsystem:latest`

### Using the application

- Find user login credentials for students and librarians in [storage/users.json]
- Expired bookings are automatically cleared when the application is started up
- We've added additional bookings for the month of December to ensure there is test data available for marking

## [Build] WITH DOCKER

1.  Run Docker Desktop

    - Docker Desktop can be installed at https://www.docker.com/products/docker-desktop/.

2.  Build image with:

    > `docker build -t "libspacemanagementsystem:latest" .`

3.  Run image inside of a container using:

    > `docker run -v storage:/storage -it libspacemanagementsystem:latest`

**Note:** Since this is a local application, all data is saved _with_ the image. If a new image is created, the data will _not_ carry over.

## [RUN] SOURCE CODE LOCALLY

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

All test cases are in the 'test' directory.

- To collect and run all pytests, run the following command in the main directory:

  > `python -m pytest`
