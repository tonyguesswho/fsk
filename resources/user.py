from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type =str,
    required=True,
    help="This field is required"
    )
    parser.add_argument('password',
    type =str,
    required=True,
    help="This field is required"
    )


    def post(self):
        data =  UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {
            "message":"user exists"
        }
        user = UserModel(**data)
        user.save_to_db()

        return {
            "message":"user created successfully"
        }


