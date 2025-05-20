import json
import os
import sys
import pathlib
import sqlite3
from flask import Flask, request, jsonify, Response, g

def make_db():
    return sqlite3.connect(os.path.dirname(os.path.abspath(sys.argv[0])) + os.sep + "crud.db")

# Формируем коннект к БД (если БД не существует, то она будет создана рядом со скриптом)
db = sqlite3.connect(os.path.dirname(os.path.abspath(sys.argv[0])) + os.sep + "crud.db")
cursor = db.cursor()

# Создаем структуру
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users
    (
        user_name TEXT PRIMARY KEY NOT NULL UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    );
''')
db.commit()


# Функция, формирующая ошибку
def make_response(code, message = str()):
    r = Response()
    r.status = code
    r.mimetype = "application/json"
    r.data = json.dumps({"code": code, "message": message})
    return r


app = Flask(__name__)


@app.route('/user', methods=['POST'])
def user_create():

    # Парсим запрос
    params = json.loads(request.data)

    # Проверяем поля
    if "user_name" not in params:
        return make_response(400, "Field 'user_name' does not exist")

    if "first_name" not in params:
        return make_response(400, "Field 'first_name' does not exist")

    if "last_name" not in params:
        return make_response(400, "Field 'last_name' does not exist")

    if "email" not in params:
        return make_response(400, "Field 'email' does not exist")

    if "phone" not in params:
        return make_response(400, "Field 'phone' does not exist")

    # Вытаскиваем значения полей
    user_name = params["user_name"]
    first_name = params["first_name"]
    last_name = params["last_name"]
    email = params["email"]
    phone = params["phone"]

    # Формируем запрос на вставку
    sql = f'''
        INSERT INTO users(user_name, first_name, last_name, email, phone)
        VALUES('{user_name}', '{first_name}', '{last_name}', '{email}', '{phone}') 
    '''

    # Добавляем пользователя
    try:
        db = make_db()
        db.cursor().execute(sql)
        db.commit()
    except Exception as e:
        return make_response(400, str(e))

    # И отдаём 200 при успехе
    return make_response(200, "OK")

@app.route('/user', methods=['GET'])
def user_get():

    # Парсим запрос
    params = json.loads(request.data)

    # Проверяем поля
    if "user_name" not in params:
        return make_response(400, "Field 'user_name' does not exist")

    # Вытаскиваем имя пользователя
    user_name = params["user_name"]

    # Формируем запрос на выборку
    sql = f'SELECT * FROM users WHERE user_name = \'{user_name}\''

    # Вытаскиваем пользователя
    try:
        db = make_db()
        cur = db.cursor()
        cur.execute(sql)

        row = cur.fetchone()
        if row is None:
            return make_response(404, "Not found")

        # Формируем объект
        user = {}
        user['user_name'] = user_name
        user['first_name'] = row[1]
        user['last_name'] = row[2]
        user['email'] = row[3]
        user['phone'] = row[4]

        # И отдаём его клиенту
        return Response(status=200, mimetype="application/json", response=json.dumps(user))

    except Exception as e:
        return make_response(400, str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
