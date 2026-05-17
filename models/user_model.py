from database.mongodb import users_collection

class UserModel:

    @staticmethod
    def create_user(user):

        return users_collection.insert_one(user)

    @staticmethod
    def find_by_username(username):

        return users_collection.find_one({
            "username": username
        })