#Настройка приложения Flask и базы данных

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, ValidationError
import pymysql
import os
import mysql.connector
from mysql.connector import connect
# from config import DB_CONFIG
# , Config
from mysql.connector import Error
import warnings
import sqlite3
# from config import Config
#connection = mysql.connector.connect(**DB_CONFIG)

app = Flask(__name__)
# загружаем конфиг из config.py
# app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://liza:f26nqZaDyZFEc5R+@localhost:3306/climbing_club'
db = SQLAlchemy(app)

# связываем приложение и экземпляр SQLAlchemy для работы с базой данных
# db.init_app(app)

connection = pymysql.connect(
    host='localhost',
    user='liza',
    password='f26nqZaDyZFEc5R+',
    database='climbing_club'
)

# connection.close()

warnings.filterwarnings("ignore", category=DeprecationWarning)

# connection = sqlite3.connect('climbing_club.db')
# cursor = connection.cursor()

# Создание таблицы "mountains"
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS mountains (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     height INTEGER NOT NULL,
#     location TEXT
# );
# ''')

# Вставка тестовых данных
# cursor.executemany('''
# INSERT INTO mountains (name, height, location)
# VALUES (?, ?, ?)
# ''', [
#     ('Everest', 8848, 'Nepal/China'),
#     ('K2', 8611, 'Pakistan/China'),
#     ('Kangchenjunga', 8586, 'Nepal/India')
# ])

# Сохранение изменений и закрытие соединения
# connection.commit()
# connection.close()

# print("База данных успешно создана и наполнена тестовыми данными!")

# Список таблиц в базе данных
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
# print("Таблицы:", tables)

# Функция для получения данных из базы
def get_data_from_db():
    # connection = sqlite3.connect('climbing_club.db')
    # connection.open()
    cursor = connection.cursor()
    # cursor.execute("SELECT name FROM climbers")
    cursor.execute("SELECT name FROM mountains")
    # cursor.execute("SELECT name FROM expeditions")
    rows = cursor.fetchall()
    # connection.close()
    return [row[0] for row in rows]

# Главная страница
@app.route('/')
def index():
    data = get_data_from_db()
    return render_template('index.html', data=data)

# Пример API-эндпоинта
@app.route('/api/data', methods=['GET'])
def api_data():
    data = get_data_from_db()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'climbing_club'
# }

# try:
#     connection = mysql.connector.connect(**DB_CONFIG)
#     print("Успешное подключение")
# except mysql.connector.Error as err:
#     print(f"Ошибка подключения: {err}")
# finally:
#     if connection.is_connected():
#         connection.close()
#         print("Соединение закрыто")

# try:
#     connection = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='climbing_club'
#     )
#     if connection.is_connected():
#         print("Успешное подключение к базе данных")
# except Error as e:
#     print(f"Ошибка подключения: {e}")
# finally:
#     if connection.is_connected():
#         connection.close()
#         print("Соединение закрыто")

# # Настройки подключения
# connection = mysql.connector.connect(
#     host="localhost",            # Адрес сервера MySQL (обычно localhost)
#     user="root",                 # Ваш MySQL пользователь
#     password="",       # Пароль от пользователя MySQL
#     database="climbing_club"     # Имя вашей базы данных
# )

# connection = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="climbing_club"
# )
# print("Подключение успешно")

# # Проверка подключения
# if connection.is_connected():
#     print("Подключение к базе данных прошло успешно")
# else:
#     print("Ошибка подключения")

# try:
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="climbing_club"
#     )
#     print("Подключение успешно")
# except mysql.connector.Error as err:
#     print(f"Ошибка: {err}")

# with open('db.sql', 'r') as f:
#     cursor = connection.cursor()
#     cursor.execute(f.read(), multi=True)

#Модели для базы данных

class Mountain(db.Model):
    __tablename__ = 'mountains'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(100), nullable=False)

class Climber(db.Model):
    __tablename__ = 'climbers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)

class Expedition(db.Model):
    __tablename__ = 'expeditions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mountain_id = db.Column(db.Integer, db.ForeignKey('mountains.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

class Participation(db.Model):
    __tablename__ = 'participation'
    climber_id = db.Column(db.Integer, db.ForeignKey('climbers.id'), primary_key=True)
    expedition_id = db.Column(db.Integer, db.ForeignKey('expeditions.id'), primary_key=True)

#Настройка схем валидации с помощью marshmallow

class MountainSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    height = fields.Integer(required=True, validate=lambda n: n > 0)
    country = fields.String(required=True, validate=validate.Length(min=1))

class ClimberSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    address = fields.String(load_default=None)

class ExpeditionSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    mountain_id = fields.Integer(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(load_default=None)

#Обработчик для добавления новой вершины с валидацией
    
@app.route('/mountains', methods=['POST'])
def add_mountain():
    try:
        data = request.json
        schema = MountainSchema()
        validated_data = schema.load(data)  # Валидация данных

        new_mountain = Mountain(
            name=validated_data['name'],
            height=validated_data['height'],
            country=validated_data['country']
        )
        db.session.add(new_mountain)
        db.session.commit()
        return jsonify({'message': 'Mountain added successfully!'}), 201

    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
#Обработчик для добавления нового альпиниста в группу с валидацией

@app.route('/expeditions/<int:expedition_id>/climbers', methods=['POST'])
def add_climber_to_expedition(expedition_id):
    try:
        expedition = Expedition.query.get(expedition_id)
        if not expedition:
            return jsonify({'message': 'Expedition not found'}), 404

        data = request.json
        schema = ClimberSchema()
        validated_data = schema.load(data)

        climber = Climber.query.filter_by(name=validated_data['name']).first()
        if not climber:
            climber = Climber(
                name=validated_data['name'],
                address=validated_data.get('address')
            )
            db.session.add(climber)
            db.session.flush() # Получаем ID нового альпиниста

        participation = Participation(climber_id=climber.id, expedition_id=expedition_id)
        db.session.add(participation)
        db.session.commit()
        return jsonify({'message': 'Climber added to expedition successfully!'}), 201

        # Валидация и добавление альпиниста
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

#Обработка ошибок, таких как отсутствие вершины или восхождения
#добавим проверки и использование специальных обработчиков для возврата корректных HTTP-ответов
#Пример обработчика для изменения данных о вершине

@app.route('/mountains/<int:mountain_id>', methods=['PUT'])
def update_mountain(mountain_id):
    try:
        mountain = Mountain.query.get(mountain_id)
        if not mountain:
            return jsonify({'message': 'Mountain not found'}), 404

        expeditions = Expedition.query.filter_by(mountain_id=mountain_id).count()
        if expeditions > 0:
            return jsonify({'message': 'Cannot update, expeditions exist for this mountain'}), 400

        data = request.json
        schema = MountainSchema(partial=True)
        validated_data = schema.load(data)

        mountain.name = validated_data.get('name', mountain.name)
        mountain.height = validated_data.get('height', mountain.height)
        mountain.country = validated_data.get('country', mountain.country)

        db.session.commit()
        return jsonify({'message': 'Mountain updated successfully!'})

    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
#Унифицированная обработка 404 (Not Found)
#Можно добавить общий обработчик для случаев, когда гора, восхождение или альпинист не найдены
    
# @app.errorhandler(404)
# def not_found_error(error):
#     return jsonify({'message': 'Resource not found'}), 404

#Пример ошибки 400 (Bad Request) для некорректных данных
#Валидация данных через marshmallow автоматически выбрасывает ошибки, которые можно обработать    

# @app.errorhandler(ValidationError)
# def handle_validation_error(error):
#     return jsonify({'errors': error.messages}), 400


# CRUD для таблицы Mountains
#Получение списка альпинистов за определенный период

@app.route('/climbers', methods=['GET'])
def get_climbers_by_date():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    climbers = db.session.query(Climber).join(Participation).join(Expedition).filter(
        Expedition.start_date >= start_date,
        Expedition.end_date <= end_date
    ).distinct().all()
    
    return jsonify([{'id': climber.id, 'name': climber.name} for climber in climbers])

#Показать список групп, осуществлявших восхождение на определенную гору в хронологическом порядке

@app.route('/mountains/<int:mountain_id>/expeditions', methods=['GET'])
def get_expeditions_by_mountain(mountain_id):
    expeditions = Expedition.query.filter_by(mountain_id=mountain_id).order_by(Expedition.start_date).all()
    return jsonify([{
        'id': expedition.id,
        'name': expedition.name,
        'start_date': expedition.start_date,
        'end_date': expedition.end_date
    } for expedition in expeditions])


#Показать информацию о количестве восхождений каждого альпиниста на каждую гору

@app.route('/climbers/<int:climber_id>/expeditions', methods=['GET'])
def get_climber_expeditions_count(climber_id):
    results = db.session.query(
        Mountain.name,
        db.func.count(Expedition.id).label('expeditions_count')
    ).join(Expedition).join(Participation).filter(
        Participation.climber_id == climber_id
    ).group_by(Mountain.name).all()

    return jsonify([{
        'mountain_name': result.name,
        'expeditions_count': result.expeditions_count
    } for result in results])

#Показать список восхождений (групп), которые осуществлялись в указанный пользователем период времени

@app.route('/expeditions', methods=['GET'])
def get_expeditions_by_period():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    expeditions = Expedition.query.filter(
        Expedition.start_date >= start_date,
        Expedition.end_date <= end_date
    ).all()

    return jsonify([{
        'id': expedition.id,
        'name': expedition.name,
        'start_date': expedition.start_date,
        'end_date': expedition.end_date
    } for expedition in expeditions])

#Добавление новой группы (восхождения)

@app.route('/expeditions', methods=['POST'])
def add_expedition():
    data = request.json
    new_expedition = Expedition(
        name=data['name'],
        mountain_id=data['mountain_id'],
        start_date=data['start_date'],
        end_date=data.get('end_date')
    )
    db.session.add(new_expedition)
    db.session.commit()
    return jsonify({'message': 'Expedition added successfully!'}), 201

#Показать количество альпинистов, побывавших на каждой горе

@app.route('/mountains/climber_count', methods=['GET'])
def get_climber_count_per_mountain():
    results = db.session.query(
        Mountain.name,
        db.func.count(db.distinct(Participation.climber_id)).label('climber_count')
    ).join(Expedition).join(Participation).group_by(Mountain.name).all()

    return jsonify([{
        'mountain_name': result.name,
        'climber_count': result.climber_count
    } for result in results])

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

#
#
#


# SQL для создания таблиц
# CREATE_DB_SQL = """
# CREATE TABLE IF NOT EXISTS mountains (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     height INT NOT NULL CHECK (height > 0),
#     country VARCHAR(255) NOT NULL
# );

# CREATE TABLE IF NOT EXISTS expeditions (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     mountain_id INT NOT NULL,
#     start_date DATE NOT NULL,
#     end_date DATE,
#     FOREIGN KEY (mountain_id) REFERENCES mountains(id) ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS climbers (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     address VARCHAR(255)
# );

# CREATE TABLE IF NOT EXISTS participations (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     expedition_id INT NOT NULL,
#     climber_id INT NOT NULL,
#     FOREIGN KEY (expedition_id) REFERENCES expeditions(id) ON DELETE CASCADE,
#     FOREIGN KEY (climber_id) REFERENCES climbers(id) ON DELETE CASCADE,
#     UNIQUE(expedition_id, climber_id)
# );
# """

# Подключение и выполнение SQL
# def setup_database():
#     conn = connect(
#         host='localhost',
#         user='your_username',
#         password='your_password',
#         database='db'
#     )
#     cursor = conn.cursor()
#     for statement in CREATE_DB_SQL.split(';'):
#         if statement.strip():
#             cursor.execute(statement)
#     conn.commit()
#     cursor.close()
#     conn.close()

# if __name__ == "__main__":
#     setup_database()
