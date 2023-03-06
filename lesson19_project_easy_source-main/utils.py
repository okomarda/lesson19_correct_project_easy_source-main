import jwt
from flask import request, abort
from models import User

algo = 'HS256'
secret = 'Ada1941++'


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, secret, algorithms=[algo])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return {"Error": "Отсутствует авторизация"}, 401

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            user = jwt.decode (token, secret, algorithms=[algo])
            role = user.get("role")
            if role != "admin":
                return {"Error": "Пользователь не имеет прав на совершение операции"}, 400
        except Exception as e:
            print ("JWT Decode Exception", e)
            abort (401)
        return func (*args, **kwargs)

    return wrapper





