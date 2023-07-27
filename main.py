import re
import datetime
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from buttons import *
from config import get_tokens
from managment_database import *


class DatingBot:
    def __init__(self, user_token, group_token, db_token):
        self.db_token = db_token
        self.data_management_vk = DataManagementVK()
        self.user_vk = vk_api.VkApi(token=user_token)
        self.group_vk = vk_api.VkApi(token=group_token)
        self.user_vk_api = self.user_vk.get_api()
        self.group_vk_api = self.group_vk.get_api()
        self.longpoll = VkLongPoll(self.group_vk)
        self.event = None
        self.request = ""

    @staticmethod
    def _create_user_vk(token):
        """
        Метод _create_user_vk(token) используется для создания экземпляра объекта VkApi, который устанавливает
        подключение к серверам VKontakte с помощью токена доступа пользователя.
        """

        try:
            return vk_api.VkApi(token=token)
        except vk_api.VkApiError as error:
            print(f"Произошла ошибка при подключении пользователя VkApi: {error}")

    @staticmethod
    def _create_group_vk(token):
        """
        Метод _create_group_vk(token) используется для создания экземпляра объекта VkApi, который устанавливает
        подключение к серверам VKontakte с помощью токена доступа приложения.
        """

        try:
            return vk_api.VkApi(token=token)
        except vk_api.VkApiError as error:
            print(f"Произошла ошибка при подключении группы VkApi: {error}")

    def send_message(self, user_id, message, keyboard=None):
        """
        Функция send_message используется для отправки сообщений пользователю VK. Аргументы: user_id (int):
        идентификатор пользователя VK, которому отправляется сообщение. message (str): текст сообщения, который будет
        отправлен пользователю. Keyboard (объект Keyboard, необязательно): объект клавиатуры, который будет
        прикреплен к сообщению. По умолчанию равен None. Возвращаемое значение: отсутствует.
        """

        post = {"user_id": user_id, "message": message, "random_id": randrange(10**7)}
        if keyboard is not None:
            post["keyboard"] = keyboard.get_keyboard()
        else:
            post = post

        self.group_vk.method("messages.send", post)

    def get_user_name(self, user_id):
        """
        Функция get_user_name используется для получения имени пользователя VK по его user_id.
        Аргументы:
        user_id: идентификатор пользователя VK.
        Возвращаемое значение:
        name: имя пользователя VK.
        """

        try:
            user_info = self.group_vk_api.users.get(user_id=user_id)
            name = user_info[0]["first_name"]
            return name
        except (KeyError, vk_api.VkApiError) as error:
            print(f"Произошла ошибка при получении информации о пользователе: {error}")

    def declination_of_years(self, years, till=True):
        """
        Эта функция принимает параметр 'years' и возвращает правильное склонение лет, основанное на значении флага
        'till'. Параметры: - years: целое число, представляющее количество лет. - till: логический флаг. Если 'till'
        имеет значение True, функция вернет склонение лет для регистра 'до'. Если значение 'till' равно False,
        функция вернет склонение лет для регистра 'от'. Возвращается: - Строка, представляющая правильное склонение
        лет на основе входных значений.
        """

        if till:
            name_years = [1, 21, 31, 41, 51, 61, 71, 81, 91, 101]
            if years in name_years:
                return f"{years} год"
            else:
                return f"{years} лет"
        else:
            name_years = [
                2,
                3,
                4,
                22,
                23,
                24,
                32,
                33,
                34,
                42,
                43,
                44,
                52,
                53,
                54,
                62,
                63,
                64,
            ]
            if years == 1 or years % 10 == 1:
                return f"{years} год"
            elif years in name_years:
                return f"{years} года"
            else:
                return f"{years} лет"

    def search_enter_age(self, user_id, age: str):
        """
        Функция search_enter_age принимает идентификатор пользователя user_id и возраст в виде строки age. Функция
        извлекает числа из строки возраста и сохраняет их в список age_list. Далее функция пытается преобразовать
        первый и второй элемент списка age_list в целые числа age_from и age_to. Если age_from и age_to равны,
        функция отправляет пользователю сообщение с указанием поиска пользователей в возрасте age_to (используя
        функцию declination_of_years для получения правильной формы склонения). В противном случае,
        функция отправляет сообщение пользователю с указанием поиска пользователей в возрасте от age_from до age_to
        (опять же, используя функцию declination_of_years). Если возникла ошибка IndexError, функция считает,
        что второе число в строке возраста не указано, и присваивает переменной age_to значение первого числа. Затем
        функция отправляет сообщение пользователю с указанием поиска пользователей в возрасте age_to. Если возникла
        ошибка NameError, функция считает, что строка возраста была неверно введена, и отправляет пользователю
        сообщение с указанием правильного формата ввода возраста. Если возникла ошибка ValueError, функция считает,
        что строка возраста содержит неверное значение, и отправляет пользователю сообщение с указанием правильного
        формата ввода возраста.
        """

        global age_from, age_to
        pattern = r"\d+"
        age_list = []
        for element in age.split():
            if re.match(pattern, str(element)):
                age_list.append(element)
        try:
            age_from = int(age_list[0])
            age_to = int(age_list[1])
            if age_from == age_to:
                self.send_message(
                    user_id,
                    f"Поиск пользователей в возрасте {self.declination_of_years(age_to, False)}",
                )
                return
            self.send_message(
                user_id,
                f" Поиск пользователей в возрасте от {age_from} и до {self.declination_of_years(age_to, True)}",
            )
            return
        except IndexError as error:
            age_to = int(age)
            self.send_message(
                user_id,
                f"Поиск пользователей в возрасте {self.declination_of_years(age_to, False)}",
            )
            return
        except NameError as error:
            self.send_message(
                user_id,
                f"Возникла ошибка {error}. Укажите возраст в формате: 'от <число> до <число>'",
            )
            return
        except ValueError as error:
            self.send_message(
                user_id,
                f"Возникла ошибка {error}. Укажите возраст в формате: 'от <число> до <число>'",
            )
            return

    def get_person_age(self, bdate: str):
        """
        Функция get_person_age принимает в качестве аргумента строку bdate, представляющую дату рождения в формате
        "день.месяц.год". Функция разбивает строку bdate на отдельные компоненты (день, месяц, год) с помощью метода
        split. Затем функция создает объект типа datetime.date с обратной датой рождения (год, месяц, день). Далее
        функция получает текущую дату с помощью datetime.date.today и вычисляет разницу в годах между текущей датой и
        датой рождения. Если месяц дня рождения меньше текущего месяца или если месяцы равны, но день рождения меньше
        или равен текущему дню, то количество лет уменьшается на 1. Затем функция вызывает метод declination_of_years
        с аргументами years (количество лет) и False (отвечает за форму склонения). Метод declination_of_years
        возвращает строку с правильной формой склонения для слова "год". Если возникает ошибка IndexError,
        это означает, что в строке bdate не указан компонент месяца, и функция попытается получить соответствующий
        месяц из словаря month_dict. Затем функция создает строку с указанием только дня рождения и месяца (если
        месяц найден в словаре), иначе возвращается None. Функция возвращает полученные значения в виде строки с
        указанием возраста или None, если возникла ошибка при обработке даты рождения.
        """

        month_dict = {
            "1": "января",
            "2": "февраля",
            "3": "марта",
            "4": "апреля",
            "5": "мая",
            "6": "июня",
            "7": "июля",
            "8": "августа",
            "9": "сентября",
            "10": "октября",
            "11": "ноября",
            "12": "декабря",
        }
        try:
            birth_date_split = bdate.split(".")
            month = ""
            rev_birth_date = datetime.date(
                int(birth_date_split[2]),
                int(birth_date_split[1]),
                int(birth_date_split[0]),
            )
            today = datetime.date.today()
            years = today.year - rev_birth_date.year
            if (
                rev_birth_date.month == today.month
                and rev_birth_date.day <= today.day
                or rev_birth_date.month < today.month
            ):
                years -= 1
            return self.declination_of_years(years, False)
        except IndexError:
            month = month_dict.get(month_dict[1])
            day = int(month_dict[0])
            return f"День рождения {day} {month}." if month else None

    def get_user_age(self, user_id):
        """
        Функция get_user_age принимает в качестве аргумента user_id и получает информацию о пользователе с помощью
        метода users.get из API ВКонтакте. Из полученной информации извлекается значение поля "bdate", представляющее
        дату рождения пользователя. Затем функция вызывает функцию get_person_age, которая вычисляет возраст
        пользователя на основе даты рождения. Полученный возраст сохраняется в переменные age_from и age_to. Если
        возраст пользователя не удалось определить (поле "bdate" не заполнено или скрыто настройками приватности),
        функция отправляет пользователю сообщение с просьбой указать возраст в формате "от <число> до <число>". Далее
        функция ожидает ответа пользователя и передает полученный возраст в функцию search_enter_age для дальнейшей
        обработки. Если возраст пользователя удалось определить, функция вызывает функцию declination_of_years для
        получения строки с правильной формой склонения для слова "год". Если при обработке информации возникает
        ошибка KeyError, то это означает, что поле "bdate" не присутствует в информации о пользователе или является
        пустым. В этом случае функция также отправляет пользователю сообщение с просьбой указать возраст в формате
        "от <число> до <число>" и ожидает ответа пользователя для дальнейшей обработки. В конце функция возвращает
        строку с возрастом пользователя или None, если возникла ошибка при обработке даты рождения.
        """

        global age_from, age_to
        try:
            information = self.user_vk_api.users.get(
                user_ids=user_id,
                fields="bdate",
            )[
                0
            ]["bdate"]
            user_age = self.get_person_age(information).split()[0]
            age_from = user_age
            age_to = user_age
            if user_age == "День":
                self.send_message(
                    user_id,
                    f"Я не знаю Ваш возраст потому что вы скрыли год рождения в настройках приватности.\n"
                    f"Поэтому придется использовать руки. Укажити возраст в формате: 'от <число> до <число>' ",
                )
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return self.search_enter_age(user_id, age)
            return self.declination_of_years(age_to)
        except KeyError:
            self.send_message(
                user_id,
                f"Я не знаю Ваш возраст потому что вы скрыли год рождения в настройках приватности.\n"
                f"Поэтому придется использовать руки. Укажити возраст в формате: 'от <число> до <число>'",
            )
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return self.search_enter_age(user_id, age)

    def get_city(self, user_id):
        """
        Функция get_city принимает в качестве аргумента user_id и получает информацию о пользователе с помощью метода
        users.get из API ВКонтакте. Из полученной информации извлекается значение поля "city", представляющее город
        пользователя. Если значение поля "city" присутствует и не равно None, функция возвращает сообщение в формате
        "В городе <название города>.". Если значение поля "city" отсутствует или равно None, функция запрашивает у
        пользователя название города с помощью функции longpoll и вызывает метод database.getCities из API ВКонтакте
        для поиска города с введенным названием. Если город найден, функция возвращает сообщение в формате "В городе
        <название города>.". Если город не найден, функция запрашивает у пользователя повторно ввести название города
        или отвечает другим сообщением в зависимости от логики приложения. В конце функция возвращает строку с
        названием города.
        """

        global city_id, city_title
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer = event.text.lower()
                if answer == "да":
                    info = self.user_vk_api.users.get(user_id=user_id, fields="city")
                    city_id = info[0]["city"]["id"]
                    city_title = info[0]["city"]["title"]
                    return f"В городе {city_title}."
                else:
                    cities = self.user_vk_api.database.getCities(
                        country_id=1, q=answer.capitalize(), need_all=1, count=1000
                    )["items"]
                    for i in cities:
                        if i["title"] == answer.capitalize():
                            city_id = i["id"]
                            city_title = answer.capitalize()
                            return f"В городе {city_title}"

    def get_search_gender(self, user_id):
        """
        Функция get_search_gender используется для определения пола пользователя VK и отправки сообщения в
        зависимости от этого значения. Аргументы: user_id (int): идентификатор пользователя VK, для которого
        определяется пол. Возвращаемое значение: Если пол пользователя равен 1 (женский), то возвращается значение 2.
        Если пол пользователя равен 2 (мужской), то возвращается значение 1.
        """

        information = self.user_vk_api.users.get(user_id=user_id, fields="sex")
        user_gender = information[0]["sex"]
        if user_gender == 1:
            self.send_message(user_id, f"Ваш пол женский, ищем мужчину.")
            return 2
        elif user_gender == 2:
            self.send_message(user_id, f"Ваш пол мужской, ищем женщину.")
            return 1
        else:
            self.send_message(user_id, f"Я не смог определить ваш пол. Кто Вы?")

    def looking_for_persons(self, user_id):
        """
        Функция looking_for_persons используется для поиска пользователей ВКонтакте на основе указанных критериев.
        Аргументы:
        user_id (int): идентификатор пользователя ВКонтакте, для которого осуществляется поиск.
        Возвращаемое значение:
        None
        """

        global list_found_persons
        list_found_persons = []
        res = self.user_vk_api.users.search(
            sort=0,
            city=city_id,
            hometown=city_title,
            sex=self.get_search_gender(user_id),
            status=1,
            age_from=age_from,
            age_to=age_to,
            has_photo=1,
            can_write_private_message=1,
            count=1000,
            fields="can_write_private_message, " "city, " "domain, " "home_town, ",
        )
        number = 0
        for person in res["items"]:
            if not person["is_closed"]:
                if (
                    "city" in person
                    and person["city"]["id"] == city_id
                    and person["city"]["title"] == city_title
                ):
                    number += 1
                    id_vk = person["id"]
                    list_found_persons.append(id_vk)
        self.send_message(
            user_id, f'Я нашел {number} доступных анкет из {res["count"]}.'
        )
        return

    def photos_found_users(self, user_id):
        """
        Функция photos_found_users используется для поиска фотографий пользователей ВКонтакте.
        Аргументы:
        user_id (int): идентификатор пользователя ВКонтакте, для которого осуществляется поиск фотографий.
        Возвращаемое значение:
        attachments (list): список вложений (фотографий), найденных для указанного пользователя.
        Каждая фотография представлена в формате "photo{user_id}_{photo_id}".
        """

        global attachments
        attachments = []
        res = self.user_vk_api.photos.get(
            owner_id=user_id, album_id="profile", extended=1, count=30
        )
        dict_photos = {}
        for i in res["items"]:
            photo_id = str(i["id"])
            i_likes = i["likes"]
            if i_likes["count"]:
                likes = i_likes["count"]
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        photo_ids = []
        for i in list_of_ids:
            photo_ids.append(i[1])
        if photo_ids:
            try:
                attachments.append("photo{}_{}".format(user_id, photo_ids[0]))
                attachments.append("photo{}_{}".format(user_id, photo_ids[1]))
                attachments.append("photo{}_{}".format(user_id, photo_ids[2]))
                return attachments
            except IndexError:
                return
        else:
            return attachments

    def found_person_info(self, show_person_id):
        """
        Функция found_person_info используется для получения информации о конкретном пользователе ВКонтакте.
        Аргументы: show_person_id (int): идентификатор пользователя ВКонтакте, информацию о котором необходимо
        получить. Возвращаемое значение: str: строка с информацией о пользователе, в формате "Имя Фамилия, возраст,
        город, ссылка_на_профиль_вконтакте". Пример использования: info = found_person_info(1234567) print(info) #
        Выводит "Иван Иванов, 25 лет, Москва. vk.com/ivanov123".
        """

        global p_id, first_name, last_name, gender, u_age, city
        pattern = r"\d+"
        res = self.user_vk_api.users.get(
            user_ids=show_person_id,
            fields="about, "  # Поле «О себе»
            "activities, "  # Поле «Деятельность».
            "bdate, "  # Дата рождения. Если дата рождения скрыта, поле отсутствует в ответе.
            "status, "
            "sex, "  # Пол (для записи в БД)
            "can_write_private_message, "  # Информация о том, может ли текущий пользователь отправить личное
            # сообщение. Возможные значения: 1 — может; 0 — не может.
            "city, "  # Город из раздела контакты.
            "common_count, "  # Количество общих друзей.
            "contacts, "  # Информация о телефонных номерах пользователя.
            "domain, "  # Короткий адрес страницы.
            "home_town, "  # Родной города.
            "interests, "  # Поле «Интересы».
            "movies, "  # Поле «Любимые фильмы».
            "music, "  # Поле «Любимая музыка».
            "occupation",  # Информация о занятиях пользователя.
        )
        p_id = show_person_id
        first_name = res[0]["first_name"]
        last_name = res[0]["last_name"]
        age = self.get_person_age(res[0]["bdate"])
        u_age = re.findall(pattern, age)[0]
        vk_link = "vk.com/" + res[0]["domain"]
        city = ""
        try:
            if res[0]["city"]["title"] is not None:
                city = f'{res[0]["city"]["title"]}'
            else:
                city = f'{res[0]["home_town"]}'
        except KeyError:
            pass
        gender = res[0]["sex"]
        return f"{first_name} {last_name}, {age}, {city}. {vk_link}"

    def send_photo(self, user_id, message, attachments):
        """
        Функция send_photo используется для отправки фотографий пользователю в сообщении. Аргументы: user_id (int):
        идентификатор пользователя, которому необходимо отправить фотографии. message (str): текст сообщения,
        которое будет отправлено вместе с фотографиями. attachments (list): список вложений в виде ссылок или
        идентификаторов фотографий. Возвращаемое значение: None Пример использования: send_photo(1234567, "Привет,
        это фотографии с нашей поездки!", ["photo1234_5678", "photo9876_5432"]).
        """

        if attachments:
            try:
                self.group_vk_api.messages.send(
                    user_id=user_id,
                    message=message,
                    random_id=randrange(10**7),
                    attachment=",".join(attachments),
                )
            except TypeError:
                pass
        else:
            self.send_message(
                user_id,
                "У данного пользователя нет фотографий в альбоме 'Фото со страницы'.",
            )

    def get_person_from_db(self):
        """
        Функция get_person_from_db используется для получения уникального идентификатора персоны из базы данных.
        Аргументы: None Возвращаемое значение: unique_person_id (int): уникальный идентификатор персоны из базы
        данных. Алгоритм работы функции: 1. Инициализируется глобальная переменная unique_person_id, которая будет
        содержать уникальный идентификатор персоны из базы данных. 2. Инициализируется глобальная переменная
        found_persons, которая будет содержать количество найденных персон в базе данных. 3. Создается пустой список
        seen_person, который будет содержать все найденные персоны из базы данных. 4. Происходит поиск персон в базе
        данных с помощью метода search_users() класса data_managment_vk. Результаты поиска добавляются в список
        seen_person. 5. Проверяется, были ли найдены персоны в базе данных. Если не найдено, то выполняется
        следующее: 6. Пытается присвоить значение первого элемента списка list_found_persons переменной
        unique_person_id. 7. Возвращается значение unique_person_id. 8. Если возникает ошибка NameError (т.е.
        переменная list_found_persons не определена), то присваивается значение 0 переменной found_persons. 9.
        Возвращается значение found_persons. 10. Если найдены персоны в базе данных, то выполняется следующее: 11.
        Пытается выполнить цикл по элементам списка list_found_persons. 12. Если текущий идентификатор персоны
        (page_id) присутствует в списке seen_person, то ничего не происходит (pass). 13. Если текущий идентификатор
        персоны (page_id) не присутствует в списке seen_person, то присваивается значение page_id переменной
        unique_person_id. Возвращается значение unique_person_id. Если возникает ошибка NameError (т.е. переменная
        list_found_persons не определена), то присваивается значение 0 переменной found_persons. Возвращается
        значение found_persons.
        """

        global unique_person_id, found_persons
        seen_person = []
        for i in self.data_management_vk.search_users():
            seen_person.append(i)
        if not seen_person:
            try:
                unique_person_id = list_found_persons[0]
                return unique_person_id
            except NameError:
                found_persons = 0
                return found_persons
        else:
            try:
                for page_id in list_found_persons:
                    if page_id in seen_person:
                        pass
                    else:
                        unique_person_id = page_id
                        return unique_person_id
            except NameError:
                found_persons = 0
                return found_persons

    def show_found_person(self, user_id):
        """
        Функция show_found_person используется для отображения найденной персоны из базы данных пользователя.
        Аргументы: self (обязательный): объект класса, который вызывает функцию. user_id (обязательный): уникальный
        идентификатор пользователя, для которого будет отображаться найденная персона. Возвращаемое значение:
        отсутствует Алгоритм работы функции: Проверяется, есть ли найденная персона в базе данных для данного
        пользователя. Если нет, то выполняется следующее: 1. Отправляется пользователю сообщение о том,
        что все анкеты были просмотрены и будет выполнен новый поиск. Также происходит запрос на изменение критериев
        поиска (возраст, город). 2. Происходит прослушивание новых сообщений от пользователя. 3. При получении нового
        сообщения с заданным возрастом, вызываются функции для обработки возраста, поиска города и поиска персон. 4.
        Вызывается функция show_found_person для отображения найденной персоны. 5. Возвращение значения функции. Если
        найдена персона в базе данных, то выполняется следующее: 1. Отправляется пользователю сообщение с информацией
        о найденной персоне и выбором клавиатуры. 2. Отправляется пользователю фотография с максимальными лайками
        персоны. 3. Вызывается функция create_user класса data_managment_vk для создания нового пользователя в базе
        данных.
        """

        if self.get_person_from_db() is None:
            self.send_message(
                user_id,
                f"Все анекты ранее были просмотрены. Будет выполнен новый поиск. "
                f"Измените критерии поиска (возраст, город). "
                f"Введите возраст поиска, на пример от 21 года и до 35 лет, "
                f"в формате : 21-35 (или 21 конкретный возраст 21 год).  ",
            )
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    self.search_enter_age(user_id, age)
                    self.get_city(user_id)
                    self.looking_for_persons(user_id)
                    self.show_found_person(user_id)
                    return
        else:
            self.send_message(
                user_id,
                self.found_person_info(self.get_person_from_db()),
                Keyboard.key_set_4(),
            )
            self.send_photo(
                user_id,
                "Фото с максимальными лайками",
                self.photos_found_users(self.get_person_from_db()),
            )
            self.data_management_vk.create_user(
                p_id, user_id, first_name, last_name, gender, u_age, city
            )

    def add_to_favorites(
        self, user_id, first_name, last_name, u_age, city, attachments
    ):
        """
        Функция add_to_favorites используется для добавления пользователя в список избранных. Аргументы:
        self(обязательный): объект класса, который вызывает функцию. user_id (обязательный): уникальный идентификатор
        пользователя, которого нужно добавить в избранное. first_name (обязательный): имя пользователя,
        которого нужно добавить в избранное. last_name (обязательный): фамилия пользователя, которого нужно добавить
        в избранное. u_age (обязательный): возраст пользователя, которого нужно добавить в избранное.
        city(обязательный): город пользователя, которого нужно добавить в избранное. attachments (необязательный):
        ссылки на фотографии пользователя, которого нужно добавить в избранное. Возвращаемое значение: отсутствует
        Алгоритм работы функции: Выполняется поиск пользователей в базе данных. Проверяется, есть ли пользователь,
        которого нужно добавить в избранное, в списке уже избранных пользователей. Если пользователь еще не добавлен
        в избранное, то выполняется следующее: Добавляется информация о пользователе в избранные пользователи в базе
        данных. Если есть фотографии для добавления, то добавляются ссылки на фотографии в базу данных. Если
        пользователь уже был добавлен в избранное ранее, то отправляется сообщение пользователю о том,
        что этот пользователь уже сохранен в избранное.
        """

        liked_users_id = self.data_management_vk.search_users()
        all_liked_users_id = self.data_management_vk.search_liked_users_id()
        this_user = int(liked_users_id[-1])
        if this_user not in all_liked_users_id:
            self.data_management_vk.add_liked_user(
                this_user, user_id, first_name, last_name, u_age, city
            )
            self.send_message(
                user_id,
                f"Последняя анкета добавлена в Избранное.",
                Keyboard.key_set_4(),
            )
            if attachments and len(attachments) >= 3:
                photo_links = attachments[:3]
                self.data_management_vk.add_photos(this_user, *photo_links)
            else:
                self.send_message(
                    user_id, f"К сожалению данные фотографии сохранить не получилось."
                )
        else:
            self.send_message(
                user_id,
                f"Этот пользователь уже сохранен в Избранном.",
                Keyboard.key_set_4(),
            )

    def show_favorites(self, user_id):
        """
        Функция show_favorites используется для отображения списка избранных пользователей. Аргументы:
        self(обязательный): объект класса, который вызывает функцию. user_id (обязательный): уникальный идентификатор
        пользователя, для которого нужно отобразить список избранных. Возвращаемое значение: отсутствует Алгоритм
        работы функции: Выполняется поиск пользователей в базе данных, которые являются избранными. Для каждого
        пользователя в списке избранных пользователей выполняется следующее: Получаются данные о пользователе: имя,
        фамилия, возраст, город и ссылка на профиль ВКонтакте. Отправляется сообщение пользователю со сведениями о
        пользователе: имя, фамилия, возраст, город и ссылка на профиль ВКонтакте. Отправляются фотографии
        пользователя, если они есть.
        """

        list_users = self.data_management_vk.search_liked_users(user_id)
        count = 0
        while count < len(list_users):
            for el in list_users:
                f_first_name = el["first_name"]
                f_last_name = el["last_name"]
                f_age = el["age"]
                f_city = el["city"]
                f_vk_link = f"vk.com/id" + str(el["liked_users_id"])
                self.send_message(
                    user_id,
                    f"{f_first_name} {f_last_name}, {self.declination_of_years(f_age, till=False)}, "
                    f"город {f_city}, cсылка вк: {f_vk_link}",
                )
                if (
                    not el["photo_link_1"]
                    and not el["photo_link_2"]
                    and not el["photo_link_3"]
                ):
                    self.send_message(user_id, "У данного пользователя нет фото.")
                else:
                    self.send_photo(
                        user_id,
                        f"Сохраненные фото пользователя:",
                        attachments=[
                            el["photo_link_1"],
                            el["photo_link_2"],
                            el["photo_link_3"],
                        ],
                    )
                count += 1

    def bot_management(self):
        """
        Функция bot_management служит для управления поведением бота и обработки входящих сообщений от пользователей.
        Аргументы:
        self (обязательный): объект класса, который вызывает функцию.
        Алгоритм работы функции:
        Происходит прослушивание событий и получение нового входящего сообщения от пользователя.
        Если тип события - новое сообщение и оно адресовано боту:
        Извлекается текст сообщения и идентификатор пользователя.
        """

        for self.event in self.longpoll.listen():
            if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                request = self.event.text
                user_id = self.event.user_id
                if request == "Начать":
                    self.send_message(
                        user_id,
                        f"Привет {self.get_user_name(user_id)}!\nЯ помогу найти тебе пару.\nЖми 'Продолжить'",
                        Keyboard.key_set_1(),
                    )
                elif request == "Продолжить...":
                    self.send_message(
                        user_id,
                        f"\n'Поиск' - меню поиска пары.\n'БД' - меню создание/удаление базы.\n"
                        f"'Выход' - завершить работу.",
                        Keyboard.key_set_2(),
                    )
                elif request == "Поиск":
                    self.send_message(
                        user_id,
                        f"\n'Да' - будем искать в городе указанный в Вашем профиле.\n"
                        f"Или введите название города - будем искать в городе который Вы скажете.\n"
                        f"Например: Москва.",
                        Keyboard.key_set_3(),
                    )
                    datingbot.get_user_age(user_id)
                    datingbot.get_city(user_id)
                    datingbot.looking_for_persons(user_id)
                    datingbot.show_found_person(user_id)
                elif request == "Дальше":
                    self.send_message(user_id, f"Хорошо, ищем дальше ...")
                    datingbot.show_found_person(user_id)
                elif request == "Добавить в Избранное":
                    datingbot.add_to_favorites(
                        user_id, first_name, last_name, u_age, city, attachments
                    )
                elif request == "Избранное":
                    self.send_message(user_id, f"Вот все кто был добавлен в Избранное.")
                    datingbot.show_favorites(user_id)
                    self.send_message(
                        user_id,
                        f"Можете продолжить поиск нажав 'Дальше'.",
                        Keyboard.key_set_7(),
                    )
                elif request == "БД":
                    self.send_message(
                        user_id,
                        f"Инструкция:\n'Создать БД' - создание базы данных.\n"
                        f"'Очистить БД' - очистка базы данных\n'Выход' - завершить работу.",
                        Keyboard.key_set_6(),
                    )
                elif request == "Создать БД":
                    create_tables(self.data_management_vk.engine)
                    self.send_message(
                        user_id,
                        f"База данных создана, {datingbot.get_user_name(user_id)}!",
                        Keyboard.key_set_2(),
                    )
                elif request == "Очистить БД":
                    create_tables(self.data_management_vk.engine)
                    self.send_message(
                        user_id,
                        f'База данных очищена, {datingbot.get_user_name(user_id)}!\nНажмите "Продолжить...".',
                        Keyboard.key_set_1(),
                    )
                elif request == "Выход":
                    self.send_message(
                        user_id,
                        f"До свидания, {datingbot.get_user_name(user_id)}!",
                        Keyboard.key_set_5(),
                    )
                else:
                    self.send_message(
                        user_id,
                        f"{datingbot.get_user_name(user_id)}, что бы начать со мной работать нажмите 'Начать'.",
                        Keyboard.key_set_5(),
                    )


if __name__ == "__main__":
    create_tables(sqlalchemy.create_engine(get_tokens()["db_token"]))
    datingbot = DatingBot(
        get_tokens()["user_token"],
        get_tokens()["group_token"],
        get_tokens()["db_token"],
    )
    datingbot.bot_management()