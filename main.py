import requests
import datetime

from aiogram.types import ReplyKeyboardMarkup, Location, KeyboardButton
from magic_filter import F

from config import BOT_TOKEN, weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

button_loc = KeyboardButton("Share your location", request_location=True)
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(button_loc)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Hello {message.from_user.full_name}!\nIm a weather forecast bot. Please write the city in '
                         f'which you live', reply_markup=main)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def loc(message: Location):
    lat = message.location.latitude
    lon = message.location.longitude
    code_to_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_token}&units=metric"
        )
        data = r.json()
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Look out the window, I don’t understand what the weather is like there!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Weather in your location ({lat}, {lon}):\nTemperature: {cur_weather}C° {wd}\n"
                            f"Humidity: {humidity}%\nPressure: {pressure}  millimeters of mercury:\nWind: {wind} m/s\n"
                            f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nLength of day: {length_of_the_day}\n"
                            f"Have a good day!"
                            )

    except:
        await message.reply("😵‍💫 Check the city name 😵‍💫")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Look out the window, I don’t understand what the weather is like there!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Weather in the city: {city}\nTemperature: {cur_weather}C° {wd}\n"
              f"Humidity: {humidity}%\nPressure: {pressure}  millimeters of mercury:\nWind: {wind} m/s\n"
              f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nLength of day: {length_of_the_day}\n"
              f"Have a good day!"
              )

    except:
        await message.reply("😵‍💫 Check the city name 😵‍💫")


if __name__ == '__main__':
    executor.start_polling(dp)







