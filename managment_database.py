import configparser

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from create_database import create_tables, Users, Photos, LikedUsers


class DataManagementVK:
    """
    Класс управления данными в БД.
    Создает пользователя.
    Добавляет фаворитов в таблицу Liked_users.
    Добавляет фотографии понравившихся пользователей в таблицу Photos
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        DSN = config["DEFAULT"]["DSN"]
        self.engine = sqlalchemy.create_engine(DSN)
        engine = sqlalchemy.create_engine(DSN)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_user(
        self, found_user_id, user_id, first_name, last_name, gender, age, city
    ):
        """
        Функция добавляет пользователя в таблицу Users
        :param user_id: идентификатор пользователя ВК
        :param first_name: имя пользователя
        :param last_name: фамилия пользователя
        :param gender: пол
        :param age: возраст
        :param city: город
        :return:
        """

        self.user = Users(
            found_user_id=found_user_id,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            age=age,
            city=city,
        )
        self.session.add(self.user)
        self.session.commit()

    def add_liked_user(self, liked_users_id, user_id, first_name, last_name, age, city):
        """
        Функция добавляет понравившуюся пару в таблицу
        :param liked_users_id: идентификатор понравившегося пользователя в ВК
        :param user_id: идентификатор пользователя, работающего с ботом
        :return:
        """

        self.liked_user = LikedUsers(
            liked_users_id=liked_users_id,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            city=city,
        )
        self.session.add(self.liked_user)
        self.session.commit()
        self.session.close()

    def add_photos(self, liked_users_id, photo_link_1, photo_link_2, photo_link_3):
        """
        Функция добавляет фотографии понравившегося пользователя в таблицу Photos
        :param photo_id:
        :param liked_users_id:
        :param photo_link:
        :param likes:
        :return:
        """

        self.photos = Photos(
            liked_users_id=liked_users_id,
            photo_link_1=photo_link_1,
            photo_link_2=photo_link_2,
            photo_link_3=photo_link_3,
        )
        self.session.add(self.photos)
        self.session.commit()
        self.session.close()

    def search_users(self):
        """
        Функция возвращает идентификаторы пользователей из таблицы users
        :return: id users
        """

        all_found_user_id = []
        for elem in self.session.query(Users.found_user_id).all():
            all_found_user_id.append(elem[0])
        return all_found_user_id

    def search_liked_users_id(self):
        """
        Функция возвращает идентификаторы пользователей из таблицы users
        :return: id users
        """

        all_found_liked_users_id = []
        for elem in self.session.query(LikedUsers.liked_users_id).all():
            all_found_liked_users_id.append(elem[0])
        return all_found_liked_users_id

    def search_liked_users(self, user_id):
        """
        Функция возвращает список словарей словарь понравившихся пользователей
        :return: liked_users_list
        """

        self.user_id = user_id
        liked_users_list = []
        for elem in (
            self.session.query(
                LikedUsers.liked_users_id,
                LikedUsers.first_name,
                LikedUsers.last_name,
                LikedUsers.city,
                LikedUsers.age,
                Photos.photo_link_1,
                Photos.photo_link_2,
                Photos.photo_link_3,
            )
            .join(Photos, LikedUsers.liked_users_id == Photos.liked_users_id)
            .filter(LikedUsers.user_id == self.user_id)
            .all()
        ):
            liked_users_dict = {
                "liked_users_id": elem[0],
                "first_name": elem[1],
                "last_name": elem[2],
                "city": elem[3],
                "age": elem[4],
                "photo_link_1": elem[5],
                "photo_link_2": elem[6],
                "photo_link_3": elem[7],
            }
            liked_users_list.append(liked_users_dict)
        return liked_users_list
