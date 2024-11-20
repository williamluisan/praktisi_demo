import json

class Data:
    def get_users_data():
        with open('data/users.json', 'r') as file:
                users = json.load(file)
        return users