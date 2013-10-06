from flask import Flask, request
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

user = {}
users = {}


# /users
class Users(Resource):
    def get(self, user_id):
        #return {user_id: users[user_id]}
        return {user_id: 'profil'}

    def post(self, user_id):
        if user_id is not None:
            return {user_id: "404"}
        else:
            return {user_id: "Welcome X"}

    def put(self, user_id):
        return {user_id: "updated"}

    def delete(self, user_id):
        return {user_id: "disabled function for instance"}

api.add_resource(Users, '/users/<int:user_id>')


# /users/login
class UsersLogin(Resource):
    # Authentificate users
    def get(self):
        return {"Authentification failed"}

api.add_resource(UsersLogin, '/users/<int:user_id>')


# /users/nearest
class UsersNearest(Resource):
    # Find users
    def get(self):
        return {"No one found there."}

api.add_resource(UsersNearest, '/users/nearest/<int:user_id>')


# /tags
class Tags(Resource):
    # Add tags
    def post(self):
        return {"May, the 4th be with you"}

api.add_resource(Tags, '/tags/')


# /geoposition
class Geoposition(Resource):
    # Update position
    def post(self):
        return {"Why are you moving so fast ?!"}

api.add_resource(Geoposition, '/geoposition/')

if __name__ == '__main__':
    app.run(debug=True)
