class UserAccount():

    def __init__(self, username, password):
        self.username= username
        self.password= password

    def isAdmin(self):
        return False

class user():
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def toDic(self):
        userDic = {'name': self.name, 'password': self.password}
        return userDic

class SuperAccount(UserAccount):

    def __init__(self, username, password, permissions):

        super().__init__(username, password)
        self.permissions= permissions
        if not permissions:
            self.permissions= ['user']

    def isAdmin(self):
        return True
