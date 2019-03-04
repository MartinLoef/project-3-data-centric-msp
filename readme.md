# [Memory Game](https://memorize-me-game.herokuapp.com/)

## Overview

### What is this website for?

This website was made as result of my 3rd project as part of my training towards Full Stack Web Developer at [Code Institute](https://codeinstitute.net).
The goal was to create a site that made use of several different technologies, outlined below. 

-   Flask
-   Database
-   Python

I am a person that like to play games, solves puzzles and also likes the competition in getting the best scores.
This resulted in making a online memory game.

This resulted in this site, where people can:

- Create an account
- Play a memory game in 2 different difficulties
- See the time and moves that they needed to solve the game
- Submit scores to a leaderboard

### What does it do?

When a player visits the site, it can chose to register of signin (if the users already has a login).
After signing in, or signing up, the user get redirected to the game page. Here the player can chose to play a 4 by 4 or 6 by 6 game.

After pressing the button to start the game, a board will appear. Based a the choice the board is 4 by 4 or 6 by 6. The player is supposed to click a tile.
After clicking the tile, it will spin around and shows a picture/icon. Click another tile to find the matching other picture/icon. If the 2 tiles don't match
the tiles will spin back around and hide the icons. If correct the tiles will remain in the open position. The goal is to find all matching pairs.
If succeeded the time, amount of moves and submit score button will appear.

After submitting the score, it will be put onto the leaderbords of 4 by 4 or 6 by 6.
In case that players have the same amount of moves, the fastest time will determine a higher ranking.

### How does it work

The site runs on Flask, with a Mongo DB as backend. 
Programming languages used are Javascript and Python.
Users can create unique accounts with hashed passwords for their protection.
Once the account is in place, users can started a memory game.
The board is created in python as a nested array with numbers.
Every number is existing 2 times, and later transformed (based on the number) to an icon on the tile.
Matching the icons if they are equal is done in the back by verifying if the numbers are equal.

The code used is mostly based on **Flask**, version 1.0.2 and **Python**, version 3.4.3.
Database backend (MongoDB) for the site is hosted with [mLab](https://mlab.com).<br>
Additionally, **jQuery**, version 3.2.1, is used to flip the 'tiles' by adding and removing classes and icons<br>
**Javascript** and **Ajax** were used to let the front-end talk to the backend (JSON objects sending over).
Styling is done using [Materialize](https://materializecss.com), version 1.0.0.<br>
<sup>Additional CSS was to create the flipping tile effects</sup>

The site can be viewed [HERE](https://memorize-me-game.herokuapp.com/).
Git repository can be found [HERE](https://github.com/MartinLoef/project-3-data-centric-msp).

## Features

### Existing Features
- Clear opening page with some explanation, and the option to sign up, or sign in
- Validation of unique username
- Password / User  validation
- Hashed(SHA2) password stored in the database
- Chose a personalized Avatar when signing up

### Features Left to Implement
- Create multiple icon sets so people can chose with what icons they want to play the game
- Possibility to change the chosen avatar
- create more game features like:
    - match 4 instead of 2
    - match 3 instead of 2
    - submit score only when it's a new high score

## Tech Used

### Technologies and outside sources:
- **HTML**, **CSS**, **jQuery** / **Javascript**, **Python**
- [Flask](http://flask.pocoo.org)
  - Base framework for the site
- **MongoDB** hosted by [mLab](https://mlab.com)
  - database backend containing all user and game information
  - separate databases for the development and production environment
- [Materialize](http://materializecss.com/) version 1.0.0
  - Used to give the site a styled and responsive layout
- [JQuery](https://jquery.com) version 3.2.1
  - Used to support the python code using ajax and for styling of the tiles
- [Stack Overflow](https://stackoverflow.com/)
- [Heroku](https://dashboard.heroku.com)
  - Used to host the site

### Database setup
The database used is a NoSQL MongoDB.
The schema is short:
- tblUsers
- tblBeginner
- tblExpert
- tblGamesPlayed
- tblAvatar
Extended information can be found within the Word document in the root of the repository.

## Deployment
Two separate databases exist, one for development and one for production.
Originally the current production database was used in development, in order to quickly fill it with a good amount of data.
Towards the end, a new specific development database was created. Based on the environment the app is executed in, the correct database is loaded.<br>
Both databases have an identical set of tables, to ensure no unnecessary precautions need to be taken.<br>

Git is used for the deployment of the application. The order of steps is:
- Development and testing on Cloud 9
- Commit changes to Git
- When needed, push changes to Github
- Heroku is connected to Github and picks up the new changes
- Heroku kicks off a new build based on the changes

Within the code, measures are taken to ensure that the application uses the correct data for the environment it's running in.
The config file reads environment variables when needed.
Based on the host the application runs on, the config.py offers the correct database link.
Both databases have 1 common table, tblAvatar, to preset the possible avatars to chose from.


## File structure
The root of the structure contains the main app(memorize.py) and its config file(config.py).
A <em>templates</em> directory holds all the HTML files used.
Within a directory <em>static</em> are sub-directories containing CSS files, image files and JS files.
Within the sub-directory <em>images</em> under <em>static</em> are the avatar and other images used within the application.
These images are needed for the startup page, and avatars to chose from.

## Wireframes and User Stories
- In the root of the repository is a document with stories and mockups (hand drawn and scanned)
    -  The document also contains extended information on the testing described below

## Testing
- Testing was done in 2 ways, by continuous testing of every step created, as well as unit tests
  - Manual tests:
    - initial HTML page with just placeholders
    - any subsequent view tested with every change
    - process data onto page placeholders
    - make modifications to the code (whether python, jquery or html) and immediately test results
    - ensure user accounts are always unique by creating an account, retry creation and see and modify responses returned
    - test user creation, user re-creation (for errors)
    - played a game after every change in javascript and python to check is all is still working

  - Unit tests:
    - for a result, see the word document in the root
    - the tests themselves are available in the test_memorize.py file
  
- Testing was done on the following browsers:
  - Safari
  - Google Chrome
  
- Mobile device testing was done:
  - Using Chrome's developer tools, emulating all available formats
  - iPhone 8
    - iOS Safari
    - iOS Opera
    - iOS Chrome
  - iPad Air
    - iOS Safari
    - iOS Opera
    - iOS Chrome

### Credits
Avatar icons were found and downloaded from: (http://www.iconarchive.com/show/buddy-icons-by-iconka.html)