-- Создание таблицы "Горы"
CREATE TABLE mountains (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    height INTEGER NOT NULL CHECK (height > 0),
    country TEXT NOT NULL
);

-- Создание таблицы "Восхождения/Группы"
CREATE TABLE expeditions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    mountain_id INTEGER NOT NULL REFERENCES mountains(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE
);

-- Создание таблицы "Альпинисты"
CREATE TABLE climbers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT
);

-- Создание таблицы "Участие в восхождении"
CREATE TABLE participations (
    id SERIAL PRIMARY KEY,
    expedition_id INTEGER NOT NULL REFERENCES expeditions(id) ON DELETE CASCADE,
    climber_id INTEGER NOT NULL REFERENCES climbers(id) ON DELETE CASCADE,
    UNIQUE(expedition_id, climber_id) -- Один альпинист может участвовать в одном восхождении только один раз
);

-- Добавление гор
INSERT INTO mountains (name, height, country) VALUES
('Everest', 8848, 'Nepal'),
('Mont Blanc', 4810, 'France'),
('Elbrus', 5642, 'Russia');

-- Добавление восхождений
INSERT INTO expeditions (name, mountain_id, start_date, end_date) VALUES
('Everest 2023 Spring', 1, '2023-04-01', '2023-05-15'),
('Elbrus Challenge 2023', 3, '2023-06-10', '2023-06-20');

-- Добавление альпинистов
INSERT INTO climbers (name, address) VALUES
('John Doe', '123 Alpine St, Denver, USA'),
('Jane Smith', '45 Summit Rd, London, UK'),
('Ivan Ivanov', 'ул. Гора, 1, Москва, Россия');

-- Добавление участия
INSERT INTO participations (expedition_id, climber_id) VALUES
(1, 1),
(1, 2),
(2, 3);