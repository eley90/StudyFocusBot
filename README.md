

# StudyFocusBot

This project was developed by **Elmira Moayedi** and **Daniela Cislaru** to simulate a study platform for their bachelor theses, this Discord bot creates a structured and gamified approach to studying, providing users with a sense of accountability, motivation, and feedback to help them achieve their study goals.


## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)


## Project Description

This Discord bot serves as a simulated controlled environment for partner studying. It offers several functions to facilitate and enhance the studying experience.
One of the primary features of the bot is to help users keep track of their study goals. Users can set specific tasks or goals they want to accomplish during their study session. The bot then allows them to log their progress as they complete these tasks. It maintains a record of the tasks and their completion status in a local database file.
The bot also introduces a credit point system to simulate rewards and consequences for the users' studying efforts. Users earn credit points for completing tasks and making progress towards their study goals. These credit points serve as a form of motivation and recognition for their achievements.
On the other hand, users can also lose credit points if they fail to complete their tasks or neglect their study responsibilities. This aspect of the bot encourages users to stay committed and disciplined in their study sessions.
At the end of the study session, the bot provides feedback to the user based on their achievements. It takes into account the tasks completed and the credit points earned to evaluate the user's overall performance. This feedback serves as a way to assess the user's progress and provide them with a sense of accomplishment.
Additionally, the bot includes random pop-up notifications to remind users to check on their study partner. These notifications act as gentle reminders to stay engaged with their study partner and maintain a supportive and collaborative environment.






## Installation

A discord Bot needs be created, following these steps:

1. Set up a Discord Developer Account: If you don't already have one, go to the Discord Developer Portal (https://discord.com/developers/applications) and create an account.

2. Enable the Bot Feature: In your application settings, navigate to the "Bot" tab and click on "Add Bot." This will turn your application into a bot account.

3. Retrieve the Bot Token: Under the "Bot" tab, you will find a section called "Token." Click on the "Copy" button to copy the token. This token is essential for your bot to authenticate and connect to the Discord API.
4. Invite the Bot to Your Server: To add the bot to your Discord server, go to the "OAuth2" tab in your application settings. Under the "Scopes" section, select the "bot" checkbox. This will generate an OAuth2 URL. Copy the URL and open it in your web browser. From there, you can choose a server to invite your bot to.
5. Set Up Your Development Environment: Install Python on your computer if you haven't already. You can download it from the official Python website (https://www.python.org/downloads/). Make sure you have a code editor installed as well, such as Visual Studio Code, PyCharm, or Atom or you can use an online integrated development environment.
6. Install the Discord.py Library: Open a terminal or command prompt and run the following command to install the Discord.py library:     pip install discord.py
7. Paste all the .py files in this repository in your project for the needed libraries see the requirements.txt .
8. Use the Bot Token: in main.py place the Token you copied earlier in the place says ‘TOKEN’
9. Channel_id : go to your Discord server and right click on the general channel, copy the channel_id and paste it in the main.py I all the places that say ‘channel_id”.



## Usage

Provide examples and instructions on how to use your project. You can include code snippets, screenshots, or even GIFs to demonstrate the functionality. Make sure to explain any important configuration or settings that the user needs to be aware of.

## Features

:warning:Available commands:
:arrow_right: **start** - to start a study session

:arrow_right: **task** followed by the task itself - to enter the task for the session

Example: task: read chapter 1 or task do exercise 1

:arrow_right: **show** - to have an overview of your current tasks

:arrow_right: **del** followed by the task - to delete a task

Example: del read chapter 1

:arrow_right: **p** - to send an angry notification if your study partner is distracted

__also available in the chat from the voice-channel__

:arrow_right: **end** - to end the study session

:exclamation: You will receive a reminder towards the end of the study session that it is ending.



