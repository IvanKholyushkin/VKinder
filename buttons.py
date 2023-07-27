from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    """
    Класс Keyboard используется для создания наборов кнопок
    """

    def __init__(self):
        self.key_set_1 = self.key_set_1()
        self.key_set_2 = self.key_set_2()
        self.key_set_3 = self.key_set_3()
        self.key_set_4 = self.key_set_4()
        self.key_set_5 = self.key_set_5()
        self.key_set_6 = self.key_set_6()

    @staticmethod
    def key_set_1():
        """
        Функция возвращает 1ый набор кнопок
        :return:
        """

        key_set_1 = VkKeyboard(one_time=True)
        key_set_1.add_button("Продолжить...", VkKeyboardColor.PRIMARY)
        key_set_1.add_line()
        key_set_1.add_button("Выход", VkKeyboardColor.PRIMARY)
        return key_set_1

    @staticmethod
    def key_set_2():
        """
        Функция возвращает 2ой набор кнопок
        :return:
        """

        key_set_2 = VkKeyboard(one_time=True)
        key_set_2.add_button("Поиск", VkKeyboardColor.PRIMARY)
        key_set_2.add_button("БД", VkKeyboardColor.PRIMARY)
        key_set_2.add_line()
        key_set_2.add_button("Выход", VkKeyboardColor.PRIMARY)
        return key_set_2

    @staticmethod
    def key_set_3():
        """
        Функция возвращает 3ий набор кнопок
        :return:
        """

        key_set_3 = VkKeyboard(one_time=True)
        key_set_3.add_button("Да", VkKeyboardColor.PRIMARY)
        key_set_3.add_line()
        key_set_3.add_button("Выход", VkKeyboardColor.PRIMARY)
        return key_set_3

    @staticmethod
    def key_set_4():
        """
        Функция возвращает 4ый набор кнопок
        :return:
        """

        key_set_4 = VkKeyboard(one_time=True)
        key_set_4.add_button("Дальше", VkKeyboardColor.PRIMARY)
        key_set_4.add_line()
        key_set_4.add_button("Добавить в Избранное", VkKeyboardColor.PRIMARY)
        key_set_4.add_line()
        key_set_4.add_button("Избранное", VkKeyboardColor.PRIMARY)
        key_set_4.add_line()
        key_set_4.add_button("Выход", VkKeyboardColor.PRIMARY)
        return key_set_4

    @staticmethod
    def key_set_5():
        """
        Функция возвращает 5ый набор кнопок
        :return:
        """

        key_set_5 = VkKeyboard(one_time=True)
        key_set_5.add_button("Начать", VkKeyboardColor.PRIMARY)
        return key_set_5

    @staticmethod
    def key_set_6():
        """
        Функция возвращает 6ой набор кнопок
        :return:
        """

        key_set_6 = VkKeyboard(one_time=True)
        key_set_6.add_button("Создать БД", VkKeyboardColor.PRIMARY)
        key_set_6.add_button("Очистить БД", VkKeyboardColor.PRIMARY)
        key_set_6.add_line()
        key_set_6.add_button("Выход", VkKeyboardColor.PRIMARY)
        return key_set_6

    @staticmethod
    def key_set_7():
        """
        Функция возвращает 7ой набор кнопок
        :return:
        """

        key_set_7 = VkKeyboard(one_time=True)
        key_set_7.add_button("Дальше", VkKeyboardColor.PRIMARY)
        key_set_7.add_line()
        key_set_7.add_button("Выход", VkKeyboardColor.PRIMARY)
        return key_set_7
