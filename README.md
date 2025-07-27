# TAKE HOME ASSESSMENT

For this assessment, I decided to use Flask as the framework as it is a part of the stack at Xanadu.

I also decided to use PostgreSQL, again because it is a part of the stack at Xanadu.

I decided to use HTML+JS templates for the UI to avoid having two projects and have them communicate.

## Setup

1. Ensure Postgres is installed and create a new database for this project.
2. Once done, go to the project folder and have the virtual environment created and activated for this project.
3. Before proceeding, update the ```DATABASE_URI``` in ```config.py``` to the proper uri for the database created for
this project.
4. Run ```pip install -r requirements.txt```
5. Once done, run ```python database/setup_db.py```. This should populate the database with the data from the json files.
6. Then run ```python app.py```. The app should be running at http://127.0.0.1:5000/


## Project Structure

### database folder

This folder holds the provided json files and a script that populates the database with the data.

### templates

Holds the HTML + JS templates. There are just 3 templates representing the home page, challenges page
(served when logged in as a user) and admin page (served when logged in as an admin).

For the assignment I have just provided two buttons to proceed with respective roles. In production conditions this
would go behind authentication and authorization and flow accordingly.

### tests

I added a few basic unit tests to ensure the api handlers work.

### models.py

This file defines SQLAchemy models for the database.

### app.py

This is the main file for the project. Since it is my first time working with Flask, all the setup and api logic code is
implemented in this file.