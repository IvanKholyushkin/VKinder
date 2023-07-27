## О проекте VKinder.

Проект в рамках курсовой работы от [Нетология](https://netology.ru/)

**VKinder** - это бот знакомств в ВК. 

*Что он делает?*<br>
Используя данные с вашей странички в ВК (пол, возраст, город) бот подбирает пару и отправляет сообщение с инфомрацией о ней и 3 самые популярные ее фотографии. Популярность определяется по количеству лайков. Информация о пользователях записывается в БД. База данных построена с использованием библиотеки ORM sqlalchemy.

1. Вы можете очистить и создать новую БД.
2. Вы можете сохранить понравившеюся анкету в Избранное. (отдельная таблица в БД)
3. Вы можете просмотреть все раннее добвленные анкеты в Избранном. 
4. Данная информация записывается в БД.

**Кнопки и команды бота:**
 - "Начать" - по этой команде бот начнет работу.
 - "Продолжить" - по этой команде бот перейдет к поиску.
 - "Дальше" - по этой команде бот покажет следующую анкету.
 - "Да" - по этой команде вы подтвердите поиск в Вашем городе. (ввести вручную если город не указан в вк). 
 - "Добавить в избранное" - по этой команде бот добавит в Избранное.
 - "Избранное" - по этой команде бот покажет всех кто был добавлен в Избранное.
 - "БД" - по этой команде бот перейдет в меню БД.
 - "Очистить БД" - по этой команде бот очистит БД.
 - "Создать БД" - - по этой команде бот созадст БД.
 - "Выход" - по этой команде бот завершит свою работы.

**Файлы проекта:** 
 - requirements.txt - все используему библиотеки для бота.
 - buttons.py - класс с кнопками.
 - VKinder_DB_scheme.drawio.png - схема БД.
 - config.ini - файл содержащий токены и строку подключения DNS. 
 - config.py - модуль создающий схему БД (используется в модуде managment_database).
 - create_datebase.py - класс который создает и удаляет БД.
 - main.py - класс запросов API и взаимодейсвие с пользователем. **(Запускать этот модуль.)**
 - managment_datebase.py - модуль предназначен для наполнения БД и извлечения данных
 - README.md - описание проекта VKinder.

**Для использования проекта необходимо:**
ВК токен для группы со всеми доступными разрешениями. (user_vk)<br>
Пользовательский токен для standalone приложений. (group_vk)<br>
Создать БД в консоли командой createdb -U postgres <название схемы>><br>
Токены и строку подключения DNS необходимо будет внести в файл .ini Модуль config.py поулчает из него данные для авторизации.<br>
Если после запуска кода сразу нажать "Добавить в Избранное" - будет ошибка т.к. еще не найден пользователь.<br>