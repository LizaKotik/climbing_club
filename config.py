# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'ваш_пароль',
#     'database': 'climbing_club'
# }

#файл config.py для хранения конфигураций приложения
# import os

# class Config:
    # SECRET_KEY используется для безопасной подписи файла cookie сеанса
    # SECRET_KEY = os.environ.get('SECRET_KEY') or '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

    # SQLALCHEMY_DATABASE_URI - это строка для соединения с базой данных
    # (для локального тестирования можно использовать файл books.db - база sqlite)
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///books.db'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://liza:f26nqZaDyZFEc5R+@localhost:3306/book_store'

    # отключаем у Flask-SQLAlchemy отслеживание изменений объектов и выдачу сигналов, нам это не нужно
    # SQLALCHEMY_TRACK_MODIFICATIONS = False