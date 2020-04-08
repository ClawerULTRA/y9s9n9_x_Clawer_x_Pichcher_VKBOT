import random


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
        if t1 == 'Почтовый индекс':  # Если написали заданную фразу
            if event1.from_user:  # Если написали в ЛС
                return "работаем"
            elif event1.from_chat:  # Если написали в Беседе
                return "работаем"