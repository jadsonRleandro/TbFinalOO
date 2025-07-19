class user():
    def __init__(self, name, password = None, admin = False, connected = False, foto='/static/assets/user.png'):
        self.name = name
        self.password = password
        self.admin = admin
        self.connected = connected
        self.foto = foto

    def toDic(self):
        userDic = {'name': self.name, 'password': self.password, 'admin': self.admin, 'connected': self.connected, 'foto': self.foto}
        return userDic
