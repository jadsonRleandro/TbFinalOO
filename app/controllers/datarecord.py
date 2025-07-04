from app.models.user_account import user
from app.models.musics import music
import json

# ------------------------------------------------------------------------------

class dataBase():
    __dataB = [{}]

    @classmethod
    def load(cls):
        with open("app/controllers/db/users.json", "r") as file:
            cls.__dataB = json.load(file)

    @classmethod
    def save(cls):
        with open("app/controllers/db/users.json", "w") as file:
            json.dump(cls.__dataB, file, indent=4)

    @classmethod
    def getUsers(cls):
        return cls.__dataB


    @classmethod
    def verindataB(cls,us):
        for i in cls.__dataB:
            if us.name == i.get('name'):
                return i
        
        return False
    
    @classmethod
    def saveInDataBase(cls, us):
        ver = cls.verindataB(us)

        if ver != False:
            for i in range(len(cls.__dataB)):
                if us.name == cls.__dataB[i]['name']:
                    cls.__dataB[i] = us.toDic()

        else:
            cls.__dataB.append(us.toDic())
        
        cls.save()
    
    @classmethod
    def newUser(cls, name, password):
        us = user(name, password)
        ver = cls.verindataB(us)
        if ver == False:
            cls.saveInDataBase(us)
            return "Usuario Adicionado"
        else:
            return "Usuario Ja Existe"

    @classmethod
    def verificarLogin(cls, user, password):
        with open("app/controllers/db/users.json", "r") as file:
            cls.__dataB = json.load(file)
        for loginGet in cls.__dataB:
            print(f"Comparando entrada: {user}/{password} com {loginGet.get('name')}/{loginGet.get('password')}")
            if user == loginGet.get('name') and password == loginGet.get('password'):
                return True
        return False
    
    @classmethod
    def verPermisions(cls, us):        
        verInDb = cls.verindataB(user(us))
        if verInDb != False:    
            return verInDb['admin']
        return False
    
    @classmethod
    def setAdmin(cls, us):
        verInDb = cls.verindataB(user(us))
        if verInDb != False:
            verInDb['admin'] = True
            cls.saveInDataBase(user(verInDb['name'], verInDb['password'], verInDb['admin']))
        return False

    @classmethod
    def removeUser(cls, us):
        index = 0
        for i in cls.__dataB:
            if us == i.get('name'):
                cls.__dataB.pop(index)
                cls.save()
                return True
            index += 1       
        return False

    @classmethod
    def connected(cls,us):
        ver = cls.verindataB(user(us))
        if ver != False:
            ver['connected'] = True
            return

# ------------------------------------------------------------------------------

class MusicsDB:
    def __init__(self):
        self.__allMusics = []
        self.__userMUsics = []
        
        self.load()

    def getAllMusics(self):
        return self.__allMusics
    
    def getUserMusic(self, us):
        for music in self.__userMUsics:
            if music['user'] == us:
                return music['musics']
        
        return ""
    
    def getUserMusicString(self, us):
        return json.dumps(self.getUserMusic(us))

    def getPublicMusicString(self):
        return json.dumps(self.getAllMusics())

    def load(self):
        with open("app/controllers/db/allMusics.json", "r") as file:
            self.__allMusics = json.load(file)
        
        with open("app/controllers/db/userMusics.json", "r") as file:
            self.__userMUsics = json.load(file)

    def save(self):
            with open("app/controllers/db/userMusics.json", "w") as file:
                    json.dump(self.__userMUsics, file, indent=4)
            
            with open("app/controllers/db/allMusics.json", "w") as file:
                    json.dump(self.__allMusics, file, indent=4)

    def removeMusic(self, musicName, paramet):
        match paramet:
            case "public":
                musicToRemove = self.verindataB(music(musicName), self.__allMusics)
                data = self.__allMusics
        
            case "private":
                musicToRemove = self.verindataB(music(musicName), self.__userMUsics[0]['musics'])
                data = self.__userMUsics[0]['musics']

        if musicToRemove != False:
            print(data)
            data.pop(musicToRemove['index'])
            self.save()

    def verindataB(self,music, db):
        indexElement = 0
        for i in db:
            if music.name == i.get('name'):
                print(i)
                print(indexElement)
                return {'element': i, 'index': indexElement} 
            indexElement += 1
        
        return False
    
    def removeUser(self, us):
        index = 0
        for i in self.__userMUsics:
            if i['user'] == us:
                self.__userMUsics.pop(index)
                self.save()
                return True
            index += 1       
        return False
        