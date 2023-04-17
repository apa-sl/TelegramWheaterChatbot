"""

APIs:
1. geocoding:
openweathermap geocoding api: https://openweathermap.org/api/geocoding-api

2. weather:
open-meteo.com API: https://api.open-meteo.com/v1/forecast

3. Telegram bot API support library: https://pypi.org/project/pyTelegramBotAPI/
"""
import requests
import telebot
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
BOT_TELEGRAM_TOKEN = os.environ.get("BOT_TELEGRAM_TOKEN")
OPENWEATHERMAP_TOKEN = os.environ.get("OPENWEATHERMAP_TOKEN")
bot = telebot.TeleBot(BOT_TELEGRAM_TOKEN)


def geolocate(location_name):
    """
    converts the specified name of a location or zip/post code into the exact geographical coordinates
    
    :return: lat+long value
    :rtype: float
    """

    try:
        params = {
            "q" : location_name,
            "limit" : "1",
            "appid" : OPENWEATHERMAP_TOKEN
        }
        response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params = params)
    except requests.RequestException:
        print("RequestException")
    except requests.ConnectionError:
        print("Connection Error")
    except requests.HTTPError:
        print("HTTP Error")
    except requests.URLRequired:
        print("URL is requrired")
    except requests.Timeout:
        print("The request timed out")
    else:
        try:
            location = response.json()
            location = location[0]
        except IndexError:
            print("Location has not been found")
        else:
            return location


def trim_weather_forcast_to_a_day(location_name, date, forecast):
    """
    trims received forecast data to selected date & basic weather parameters

    :return: Dictionaries with units & data
    :rtype: dict
    """
    try:
        #check if provided date is in the forecast data
        if date in forecast["daily"]["time"]:
            forecast_date_index = forecast["daily"]["time"].index(date)
            sunrise = forecast["daily"]["sunrise"][forecast_date_index]
            sunrise = sunrise[11:]
            sunset = forecast["daily"]["sunset"][forecast_date_index]
            sunset = sunset[11:]
            location = {
                "location":location_name
            }
            units = {
                "temp":forecast["daily_units"]["temperature_2m_max"],
                "windspeed":forecast["daily_units"]["windspeed_10m_max"],
                "precipitation":forecast["daily_units"]["precipitation_sum"],
                "probability":forecast["daily_units"]["precipitation_probability_max"],
            }
            day_full_forecast = {
                "temp_min":forecast["daily"]["temperature_2m_min"][forecast_date_index],
                "temp_max":forecast["daily"]["temperature_2m_max"][forecast_date_index],
                "temp_apparent_min":forecast["daily"]["temperature_2m_min"][forecast_date_index],
                "temp_apparent_mmax":forecast["daily"]["temperature_2m_min"][forecast_date_index],
                "sunrise":sunrise,
                "sunset":sunset,
                "precipitation_probability":forecast["daily"]["precipitation_probability_max"][forecast_date_index],
                "precipitation_sum":forecast["daily"]["temperature_2m_min"][forecast_date_index],
                "windspeed_max":forecast["daily"]["temperature_2m_min"][forecast_date_index],
                }
        return location, day_full_forecast, units
    except UnboundLocalError:
        raise UnboundLocalError("Invalid date not in the range of today or next 6 days")


def get_weather_forecast(location, date):
    """
    returns weather forecast for a given location & day (temp min-max, feels max, sunrise&sunset, precipation probability, precipation sum, max windspeed)

    :return: Dictionaries with units & data
    :rtype: dict
    """

    location = geolocate(location)

    try:
        #TODO parse API response to get only what is needed
        params = {
            "latitude" : location["lat"],
            "longitude" : location["lon"],
            "daily" : "temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_probability_max,precipitation_sum,windspeed_10m_max",
            "timezone" : "auto",
        }
        response = requests.get("https://api.open-meteo.com/v1/forecast", params = params)
    except requests.RequestException:
        print("RequestException")
    except requests.ConnectionError:
        print("Connection Error")
    except requests.HTTPError:
        print("HTTP Error")
    except requests.URLRequired:
        print("URL is requrired")
    except requests.Timeout:
        print("The request timed out")
    else:
        return trim_weather_forcast_to_a_day(location["name"], date, response.json())

@bot.message_handler(commands=["weather", "forecast", "weather_forecast"])
def bot_location_handler(message):
    """
    Bot function handling weather forecast commands and getting the location for the forecast from the user
    """
    msg_txt = "For what location do you need forecast? Enter it's *name* (eg. city name)."
    sent_msg = bot.send_message(message.chat.id, msg_txt, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, bot_date_handler)

@bot.message_handler(func=lambda m: True)
def bot_welcome(message):
    msg_txt = "Hi, I can give weather forecast for a given location for up to 6 days. Type /weather or /forecast command to get one!"
    #bot.reply_to(message, msg_txt)
    bot.send_message(message.chat.id, msg_txt, parse_mode="Markdown")
        
def bot_date_handler(message):
    """
    Bot function checking if location is known & getting date of the forecast from the user
    """
    # store location name procided by the user in the message
    location = message.text
    # check if provided location name can be geocoded, if not ask for a new location name
    if geolocate(message.text) is None:
        msg_txt = "Location has not been found, please try with a different name."
        sent_msg = bot.send_message(message.chat.id, msg_txt, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, bot_date_handler)
    # else ask user for the forecast date
    else:
        msg_txt = "For what day do you want forecast? Enter in *YYYY-MM-DD* format or today/tomorrow word"
        sent_msg = bot.send_message(message.chat.id, msg_txt, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, bot_fetch_forecast, location)


def bot_fetch_forecast(message, location):
    """
    Bot function checking if date is correct & fetching forecast data for a given location & date and passing results to the user in a message
    """
    # store date provided by the user in the message
    date = message.text
    # create list of valid_dates for user inputed date validation
    valid_dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(7)]
    valid_dates = [valid_dates[i].strftime("%Y-%m-%d") for i in range(7)]
    # check if user provided today/tomorrow keyword and translate those into actual date
    if date.lower() == "today":
        date = datetime.date.today().strftime("%Y-%m-%d")
    elif date.lower() == "tomorrow":
        date = datetime.date.today() + datetime.timedelta(days=1)
        date = date.strftime("%Y-%m-%d")

    # check if date is not inrange/wrong format - ask user for the date again
    if date not in valid_dates:
        msg_txt = "Inccorect date, please provide a date up to 6 days from now in YYYY-MM-DD format or enter today/tomorrow"
        sent_msg = bot.send_message(message.chat.id, msg_txt, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, bot_fetch_forecast, location)
    # else date is correct, fetch the forecast & send it to the user
    else:
        forecast = get_weather_forecast(location, date)
        location_name = forecast[0]["location"]
        forecast_message = f"Temp min-max: {forecast[1]['temp_min']}{forecast[2]['temp']} - {forecast[1]['temp_max']}{forecast[2]['temp']} \\\nPrecipitation: {forecast[1]['precipitation_sum']}{forecast[2]['precipitation']} (Prob. {forecast[1]['precipitation_probability']}{forecast[2]['probability']}) \\\nWindspeed: {forecast[1]['windspeed_max']}{forecast[2]['windspeed']} \\\nSunrise: {forecast[1]['sunrise']}, Sunset: {forecast[1]['sunset']}"
        bot.send_message(message.chat.id, f"Here is weather forecast for {location_name} on {date}:")
        bot.send_message(message.chat.id, forecast_message, parse_mode="Markdown")


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()