# WEATHER BOT FOR TELEGRAM
Author: Adam Labedzki
Location: Poland, Gdynia
Video demo: https://youtu.be/lkOROoZOl7k

## Description
A final project for CS50P course from HarvardX. An attempt to write an app without Front-end (only command line interface) and with some external APIs communication (API for geocoding, API for weather forecast, API for telegram bot). Initially wanted to create a Natural Language Processing (NLP) bot using RASA framework but was unsure if CS50P would accept all the project files as RASA framework requires a certain files organization so decided to do a simple Telegram chatbot instead.

File project.py has all the codebase of the project.
Modules:
- I have imported requests module to handle communication with external APIs and parse received JSON data
- Modules os & dotenv are used for keeping needed credentials (APIs tokens) in a separate .env file that is git ignored (as it should be so they will not be visible in the sorurce code in the repository).
- Module datetime is used to manipulate dates as user is able to specify a day for which he wants to get weather forecast
- Module telebot is from pyTelegramAPIbot project to use functions that handle usage of Telegram bot API.

Functions:
- there are 3 functions related to weather data (geocoding location name provided by the user, getting the forecast data for a given location, stripping weather forecast for only the needed data)
- there are 3 functions to handle basic Telegram bot API usage (send user the welcome message with the instructions, get & try to localize the location name from the user, get and validate the forecast date from the user, get and display the actual forecast)

## App purpose
Quickly check weather forecast for a given location for up to 6 days using Telegram bot

## deployment
1. Create free account at https://openweathermap.org and get API token
2. Register telegram bot with @bot_father user and get bot token
3. park both tokens in template.env file and rename it to .env
4. launch projet.py & start chatting with your bot using telegram communicator

## Tech stack
- python
- pyTelegramBotAPI
- openweathermap geocoding API
- open-meteo weather forecast API