from flask import request
from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        username = request.args.get ('username')
        udg = User.query
        if username:
            udg = udg.filter (User.username == username)

        users = udg.all()
        return users_schema.dump(users), 200



    def post(self):
        req_json = request.json
        ent = User(**req_json)

        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/users/{ent.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        b = db.session.query(User).get(uid)
        u_d = UserSchema().dump(b)
        return u_d, 200

    def put(self, uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")
        db.session.add(user)
        db.session.commit()
        return "", 204

    def delete(self, uid):
        user = db.session.query(User).get(uid)

        db.session.delete(user)
        db.session.commit()
        return "", 204