import json
from datetime import datetime



class User:
    def __init__(self, username, user_id, is_admin=False, created_at=None):
        self.username = username
        self.user_id = user_id
        self.is_admin = False if not is_admin else True
        self.created_at = datetime.now() if not created_at else datetime.strptime(created_at, '%d.%m.%Y %H:%M:%S')

    def __str__(self):
        return f'{self.username} - {self.user_id}'

    def __repr__(self):
        return self.__str__()

    def serialized(self):
        return {
            'username': self.username,
            'user_id': self.user_id,
            'is_admin': self.is_admin,
            'created_at': self.created_at.strftime('%d.%m.%Y %H:%M:%S'),
        }


class DB_User:
    def __init__(self):
        self.users: list = self.__get()

    def add_user(self, user):
        if user.user_id not in self.users_id:
            self.users.append(user)
            self.users_id.append(user.user_id)
            self.__save()

    def __save(self):
        with open(r'D:\LA\TGBOT_Stepanova\app\data_user.json', 'w') as file:
            users = [user.serialized() for user in self.users]
            json.dump(users, file)


    def __get(self) -> list:
        with open(r'D:\LA\TGBOT_Stepanova\app\data_user.json', 'r') as file:
            return json.load(file)


    def __str__(self):
        return str(self.users)

db_user = DB_User()