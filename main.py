from random import randrange
import requests
import telebot
from jikanpy import Jikan

anime_bot = telebot.TeleBot('TOKEN')


@anime_bot.message_handler(content_types=['text'])
def get_command(message):
    jikan = Jikan()
    if message.text == "/start":
        anime_bot.send_message(message.from_user.id,
                               'はじめまして! In Japanese it means: "Nice to meet you"! \n'
                               'This bot can help you to choose an anime to watch, a manga to read or '
                               'find a nice quote from them. \nPlease, write "/help" - if '
                               'you need help, "/quote" - if you want to find a random anime quote,'
                               '"/anime - if you want to find a random anime, "/manga" - if you want to find '
                               'a random '
                               'manga, /character - if you want to discover any profile or /schedule - '
                               'if you want to get a schedule for a particular day. Have a good day!')
    elif message.text == "/help":
        anime_bot.send_message(message.from_user.id, 'Please, write /help" - if you '
                                                     'need help, "/quote" - if you want to find a random anime quote,'
                                                     '"/anime - if you want to find a random anime, "/manga" - '
                                                     'if you want to find a random manga, /character - if you'
                                                     ' want to discover any profile or /schedule - if you want to'
                                                     'get a schedule for a particular day. If nothing happened, '
                                                     'do not worry, bot can think for a few seconds. Have a good day!')
    elif message.text == "/anime":
        anime_id = randrange(0, 10000)
        url = requests.get("https://myanimelist.net/anime/" + str(anime_id) + "/")
        while url.status_code == 404:
            anime_id = randrange(0, 10000)
            url = requests.get("https://myanimelist.net/anime/" + str(anime_id) + "/")
        anime = jikan.anime(anime_id)
        anime_description = " "
        for elem in anime:
            if elem == "title":
                anime_description += ("The title: " + str(anime[elem]) + ". \n")
            if elem == "title_japanese":
                anime_description += ("The original title: " + str(anime[elem]) + ". \n")
            if elem == "status":
                anime_description += ("The status: " + str(anime[elem]) + ". \n")
            if elem == "type":
                anime_description += ("The type: " + str(anime[elem]) + ". ")
            if elem == "episodes":
                anime_description += ("The amount of episodes: " + str(anime[elem]) + ". \n")
            if elem == "rating":
                anime_description += ("The rating: " + str(anime[elem]) + ". \n")
            if elem == "score":
                anime_description += ("The score: " + str(anime[elem]) + ". \n")
            if elem == "synopsis":
                anime_description += ("The synopsis: " + str(anime[elem]) + ". \n")
            if elem == "premiered":
                anime_description += ("The anime was premiered: " + str(anime[elem]) + ". \n")
            if elem == "genres":
                genre = ""
                for genres in anime[elem]:
                    genre += genres["name"] + ", "
                anime_description += ("The genres are: " + genre[:-2] + ". \n")
        anime_description += ("\nRead more on " + "https://myanimelist.net/anime/" + str(anime_id) + "/")
        anime_bot.send_message(message.from_user.id, anime_description)
    elif message.text == "/manga":
        manga_id = randrange(0, 10000)
        url = requests.get("https://myanimelist.net/manga/" + str(manga_id) + "/")
        while url.status_code == 404:
            manga_id = randrange(0, 10000)
            url = requests.get("https://myanimelist.net/manga/" + str(manga_id) + "/")
        manga = jikan.manga(manga_id)
        manga_description = ""
        for elem in manga:
            if elem == "title":
                manga_description += ("The title: " + str(manga[elem]) + ". \n")
            if elem == "title_japanese":
                manga_description += ("The original title: " + str(manga[elem]) + ". \n")
            if elem == "status":
                manga_description += ("The status: " + str(manga[elem]) + ". \n")
            if elem == "volumes":
                manga_description += ("The amount of volumes: " + str(manga[elem]) + ". \n")
            if elem == "chapters":
                manga_description += ("The amount of chapters: " + str(manga[elem]) + ". \n")
            if elem == "score":
                manga_description += ("The score: " + str(manga[elem]) + ". \n")
            if elem == "synopsis":
                manga_description += ("The synopsis: " + str(manga[elem]) + ". \n")
        manga_description += ("\nRead more on " + "https://myanimelist.net/manga/" + str(manga_id) + "/")
        anime_bot.send_message(message.from_user.id, manga_description)

    elif message.text == "/quote":
        req = requests.get('https://animechan.vercel.app/api/random')
        quote = req.text.split('"')
        answer = "The Title: " + quote[3] + " . \nThe character: " + quote[7] + ". \nThe quote: '" + quote[11] + "'. \n"
        anime_bot.send_message(message.from_user.id, answer)
    elif message.text == "/character":
        character_id = randrange(0, 10000)
        url = requests.get("https://myanimelist.net/character/" + str(character_id) + "/")
        while url.status_code == 404:
            charcter_id = randrange(0, 10000)
            url = requests.get("https://myanimelist.net/character/" + str(charcter_id) + "/")
        character = jikan.character(character_id)
        character_description = ""
        for elem in character:
            if elem == "name":
                character_description += ("Name: " + str(character[elem]) + ".\n")
            if elem == "name_kanji":
                character_description += ("Name written in kanji: " + str(character[elem]) + ".\n")
            if elem == "about":
                character_description += ("Information about the character: " + str(character[elem]) + ".\n")
        character_description += "\nRead more on " + "https://myanimelist.net/character/" + str(character_id) + "/"
        anime_bot.send_message(message.from_user.id, character_description)
    elif message.text == "/schedule":
        schedule_text = "Please, write the day of the week (for example: 'monday') \
                         and then you will get the schedule of anime for that day."
        anime_bot.send_message(message.from_user.id, schedule_text)
    elif message.text == "monday":
        schedule = jikan.schedule(day="monday")
        schedule_monday = "The schedule for Monday is: \n"
        for i in range(len(schedule["monday"])):
            schedule_monday += (str(i + 1) + ". " + schedule["monday"][i]["title"] + "\n")
        anime_bot.send_message(message.from_user.id, schedule_monday)
    elif message.text == "tuesday":
        schedule = jikan.schedule(day="tuesday")
        schedule_tuesday = "The schedule for Tuesday is: \n"
        for i in range(len(schedule["tuesday"])):
            schedule_tuesday += (str(i + 1) + ". " + schedule["tuesday"][i]["title"] + "\n")
        anime_bot.send_message(message.from_user.id, schedule_tuesday)
    elif message.text == "wednesday":
        schedule = jikan.schedule(day="wednesday")
        schedule_wednesday = "The schedule for Wednesday is: \n"
        for i in range(len(schedule["wednesday"])):
            schedule_wednesday += (str(i + 1) + ". " + schedule["wednesday"][i]["title"] + "\n")
        anime_bot.send_message(message.from_user.id, schedule_wednesday)
    elif message.text == "thursday":
        schedule = jikan.schedule(day="thursday")
        schedule_thursday = "The schedule for Thursday is: \n"
        for i in range(len(schedule["thursday"])):
            schedule_thursday += (str(i + 1) + ". " + schedule["thursday"][i]["title"] + "\n")
        anime_bot.send_message(message.from_user.id, schedule_thursday)
    elif message.text == "friday":
        schedule = jikan.schedule(day="friday")
        schedule_friday = "The schedule for Friday is: \n"
        for i in range(len(schedule["friday"])):
            schedule_friday += (str(i + 1) + ". " + schedule["friday"][i]["title"] + "\n")
        anime_bot.send_message(message.from_user.id, schedule_friday)
    elif message.text == "saturday":
        schedule = jikan.schedule(day="saturday")
        schedule_saturday = "The schedule for Saturday is: \n"
        for i in range(len(schedule["saturday"])):
            schedule_saturday += (str(i + 1) + ". " + schedule["saturday"][i]["title"] + "\n")
        anime_bot.send_message(message.from_user.id, schedule_saturday)
    elif message.text == "sunday":
        schedule = jikan.schedule(day="sunday")
        schedule_sunday = "The schedule for Sunday is: \n"
        for i in range(len(schedule["sunday"])):
            schedule_sunday += (str(i + 1) + ". " + schedule["sunday"][i]["title"] + "\n")
        anime_bot.send_message(message.from_user.id, schedule_sunday)
    else:
        anime_bot.send_message(message.from_user.id, "Sorry, I don't understand you. Please, write /help.")


anime_bot.polling(none_stop=True, interval=0)
