import vk_api
import random
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType


TOKEN = "06e9b8d2117f137dbccef94c64dca32ccd261b4423eb3cedc2421d0ee39ef899d1cd30cbadb4068272b09"
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
i = 1

class Razgovor:
    @staticmethod
    def simple(event1):
        all_phrazes = ["привет", "хай", "hi", "hello", "прив", "привки", "как дела?", "кд?", "кд", "как дела",
                       "почтовый индекс-(здесь пишете нужный адрес)", 'где находится-(здесь пишете нужный запрос)',
                       "расположение - (здесь пишете нужный запрос)", "хеллоу", "понятно"]
        privet = ["привет", "хай", "hi", "hello", "прив", "привки", "хеллоу"]
        kak_dela = ["как дела?", "кд?", "кд", "как дела"]
        otv = ["норм", "сойдёт", "у бота хорошо а у меня неплохо)", "неплохо"]
        t1 = event1.text
        if t1 == 'Pichcher top':  # Если написали заданную фразу
            if event1.from_user:  # Если написали в ЛС
                return "А ты шаришь в ютубе)"
            elif event1.from_chat:  # Если написали в Беседе
                return "А ты шаришь в ютубе)"
        if t1 == 'Понятно':  # Если написали заданную фразу
            if event1.from_user:  # Если написали в ЛС
                return "И мне понятно)"
            elif event1.from_chat:  # Если написали в Беседе
                return "И мне понятно)"
        if t1.split()[0].lower() in privet:  # Если написали заданную фразу
            if event1.from_user:  # Если написали в ЛС
                return random.choice(privet)
            elif event1.from_chat:  # Если написали в Беседе
                return random.choice(privet)
        if t1.lower() in kak_dela:  # Если написали заданную фразу
            if event1.from_user:  # Если написали в ЛС
                return random.choice(otv)
            elif event1.from_chat:  # Если написали в Беседе
                return random.choice(otv)
        if t1.lower() == "все команды" or t1.lower() == "список команд":
            if event1.from_user:  # Если написали в ЛС
                return "\n".join(all_phrazes)
            elif event1.from_chat:  # Если написали в Беседе
                return "\n".join(all_phrazes)


def poisk_yandex_map_api(mesto, what):
    try:
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={mesto}&format=json"

        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()


            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

            if what == 1:
                toponym_coodrinates = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                return f"Почтовый индекс {mesto} - {toponym_coodrinates}"
            elif what == 2:
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                toponym_coodrinates = toponym["Point"]["pos"]
                return f"{toponym_address} имеет координаты: {toponym_coodrinates}"

    except Exception:
        return "Ошибка выполнения запроса"


def yandex_weather(mesto):
    try:
        geo_weather_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={mesto}&format=json"
        response = requests.get(geo_weather_request)
        if response:
            json_geo_response = response.json()
            toponym = json_geo_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            coords = toponym.split()
            weather_request = f'https://api.weather.yandex.ru/v1/informers?lat={coords[1]}&lon={coords[0]}'
            headers = {'X-Yandex-API-Key': '6b0f78de-b1d6-42b7-9d71-2ca438a5c250'}
            response_weather = requests.get(weather_request, headers=headers)
            if response_weather:
                json_weather_response = response_weather.json()
                weather = json_weather_response
                print(weather)



    except Exception:
        return "Ошибка выполнения запроса"

for event in longpoll.listen():
    i += 1
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        t1 = event.text
        if t1.split("-")[0].rstrip().lower() == "почтовый индекс" or t1.split("-")[0].lower() == "почтовый индекс ":
            if event.from_user:  # Если написали в ЛС
                vk.messages.send(user_id=event.user_id, message=poisk_yandex_map_api(t1.split("-")[1].lstrip(), 1),
                                 random_id=i)
            elif event.from_chat:  # Если написали в Беседе
                vk.messages.send(user_id=event.user_id, message=poisk_yandex_map_api(t1.split("-")[1].lstrip(), 1),
                                 random_id=i)
        elif t1.split("-")[0].rstrip().lower() == "где находится" or t1.split("-")[0].lower() == "расположение":
            if event.from_user:  # Если написали в ЛС
                vk.messages.send(user_id=event.user_id, message=poisk_yandex_map_api(t1.split("-")[1].lstrip(), 2),
                                 random_id=i)
            elif event.from_chat:  # Если написали в Беседе
                vk.messages.send(user_id=event.user_id, message=poisk_yandex_map_api(t1.split("-")[1].lstrip(), 2),
                                 random_id=i)
        elif t1.split("-")[0].rstrip().lower() == 'погода' or t1.split("-")[0].rstrip().lower() == 'погода ':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=poisk_yandex_map_api(t1.split("-")[1].lstrip(), 2),
                                 random_id=i)

            elif event.from_chat:  # Если написали в Беседе
                pass
        else:
            try:
                vk.messages.send(user_id=event.user_id, message=Razgovor.simple(event), random_id=i)
            except Exception:
                pass

