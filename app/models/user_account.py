class user():
    def __init__(self, name, password = None, admin = False, connected = False):
        self.name = name
        self.password = password
        self.admin = admin
        self.connected = connected

    def toDic(self):
        userDic = {'name': self.name, 'password': self.password, 'admin': self.admin, 'connected': self.connected}
        return userDic
