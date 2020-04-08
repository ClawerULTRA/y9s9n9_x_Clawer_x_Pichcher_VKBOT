import vk_api
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType


TOKEN = "06e9b8d2117f137dbccef94c64dca32ccd261b4423eb3cedc2421d0ee39ef899d1cd30cbadb4068272b09"

TARGET_POSTCODE = 0
TARGET_COORDINATES = 1

welcome_messages = ["привет", "хай", "hi", "hello", "прив", "привки", "хеллоу"]
how_are_you_messages = ["как дела?", "кд?", "кд", "как дела"]
responses = ["норм", "сойдёт", "у бота хорошо а у меня неплохо)", "неплохо"]
all_phrases = welcome_messages + how_are_you_messages + \
              ["почтовый индекс-(здесь пишете нужный адрес)", 'где находится-(здесь пишете нужный запрос)',
               "расположение - (здесь пишете нужный запрос)", "хеллоу", "понятно"]

vk_session = vk_api.VkApi(token=TOKEN)
vk_long_poll = VkLongPoll(vk_session)
vk = vk_session.get_api()
i = 1


class Conversation:
    @staticmethod
    def reply_to(message) -> str:
        text = message.text
        if text == 'Pichcher top':
            return "А ты шаришь в ютубе)"
        if text == 'Понятно':
            return "И мне понятно)"
        if text.split()[0].lower() in welcome_messages:
            return random.choice(welcome_messages)
        if text.lower() in how_are_you_messages:
            return random.choice(responses)
        if text.lower() == "все команды" or text.lower() == "список команд":
            return "\n".join(all_phrases)


# yandex map api
def map_search(place, search_target) -> str:
    # noinspection PyBroadException
    try:
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/" \
            f"?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={place}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            if search_target == TARGET_POSTCODE:
                toponym_coodrinates = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                return f"Почтовый индекс {place} - {toponym_coodrinates}"
            elif search_target == TARGET_COORDINATES:
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                toponym_coodrinates = toponym["Point"]["pos"]
                return f"{toponym_address} имеет координаты: {toponym_coodrinates}"
        else:
            # raising exception because response is not success
            raise Exception
    except Exception:
        return "Ошибка выполнения запроса"


# yandex weather api
def weather(place):
    # noinspection PyBroadException
    try:
        geo_weather_request = f"http://geocode-maps.yandex.ru/1.x/" \
            f"?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={place}&format=json"
        response = requests.get(geo_weather_request)
        if response:
            json_geo_response = response.json()
            toponym = \
                json_geo_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            coords = toponym.split()
            weather_request = f'https://api.weather.yandex.ru/v1/informers?lat={coords[1]}&lon={coords[0]}'
            headers = {'X-Yandex-API-Key': '6b0f78de-b1d6-42b7-9d71-2ca438a5c250'}
            response_weather = requests.get(weather_request, headers=headers)

            if response_weather:
                print(response_weather.json())
            else:
                # raising exception because response is not success
                raise Exception
        else:
            # raising exception because response is not success
            raise Exception

    except Exception:
        return "Ошибка выполнения запроса"


for event in vk_long_poll.listen():
    i += 1
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        t1 = event.text
        if t1.split("-")[0].rstrip().lower() == "почтовый индекс" or t1.split("-")[0].lower() == "почтовый индекс ":
            vk.messages.send(user_id=event.user_id, message=map_search(t1.split("-")[1].lstrip(), TARGET_POSTCODE),
                             random_id=i)
        elif t1.split("-")[0].rstrip().lower() == "где находится" or t1.split("-")[0].lower() == "расположение":
            vk.messages.send(user_id=event.user_id, message=map_search(t1.split("-")[1].lstrip(), TARGET_COORDINATES),
                             random_id=i)
        elif t1.split("-")[0].rstrip().lower() == 'погода' or t1.split("-")[0].rstrip().lower() == 'погода ':
            vk.messages.send(user_id=event.user_id, message=map_search(t1.split("-")[1].lstrip(), 2),
                             random_id=i)
        else:
            # noinspection PyBroadException
            try:
                vk.messages.send(user_id=event.user_id, message=Conversation.reply_to(event), random_id=i)
            except Exception:
                pass
