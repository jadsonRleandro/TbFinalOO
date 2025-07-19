import os
from app.models.user_account import user
from app.models.musics import music
import json
import uuid
# ------------------------------------------------------------------------------

class dataBase():
    __dataB = [{}]
    __user_autenticado = {}
    __thumbProfile = []

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
    def getConnectedUsers(cls):
        conecteds = []
        for user in cls.__dataB:
            if user['connected'] == True:
                conecteds.append({'name': user['name'], 'permision': user['admin']})
        return conecteds

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
                session_id = str(uuid.uuid4())
                cls.__user_autenticado[session_id] = user
                print(cls.__user_autenticado)   
                return True, session_id
        return False, None
    
    @classmethod
    def getUserByID(cls,session_id):
        return cls.__user_autenticado[session_id]
    
    @classmethod
    def verifyUserWithID(cls,session_id):
        if session_id in cls.__user_autenticado:
            return True, cls.__user_autenticado[session_id]
        return False, None
    
    @classmethod
    def logoutUser(cls,session_id):
        if session_id in cls.__user_autenticado:
            cls.disconnectUser(cls.__user_autenticado[session_id])
            del cls.__user_autenticado[session_id]
    
    
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
            cls.save()
            return
        
    @classmethod
    def disconnectUser(cls, us):
        ver = cls.verindataB(user(us))
        if ver != False:
            ver['connected'] = False
            cls.save()
            return
        
    @classmethod
    def getProfileFoto(cls, us):
        with open('app/controllers/db/users.json', 'r') as file:
            getFoto = json.load(file)
        for user in getFoto:
            if user['name'] == us:
                return user['foto']
        return None
    
    @classmethod
    def getPassword(cls, user):
        with open('app/controllers/db/users.json', 'r') as file:
            getPasswordUser = json.load(file)
        for i in getPasswordUser:
            if i['name'] == user:
                return i['password']
        return None
    
    @classmethod
    def verificarUser(cls, user):
        with open('app/controllers/db/users.json','r') as file:
            vUser = json.load(file)
        for i in vUser:
            if i['name'] == user:
                return True
        return False
    
    @classmethod
    def changeUsername(cls, us, newUser):
        with open('app/controllers/db/users.json', 'r') as file:
            changeUser = json.load(file)
        for user in changeUser:
            if user['name'] == us:
                userAntigo = user['name']
                user['name'] = newUser
                cls.changeUserMusics(newUser, userAntigo)
                with open('app/controllers/db/users.json', 'w') as file:
                    json.dump(changeUser, file,indent=4,ensure_ascii=False)
                return newUser
        return 'Não foi possivel.'
    
    @classmethod
    def changeUserMusics(cls, newUser, userAntigo):
        with open('app/controllers/db/userMusics.json', 'r') as file:
            changeUser = json.load(file)
        for music in changeUser:
            if music['user'] == userAntigo:
                music['user'] = newUser
                with open('app/controllers/db/userMusics.json', 'w') as file:
                    json.dump(changeUser, file, indent=4, ensure_ascii=False)
                return
        return
    
    @classmethod
    def deleteAccount(cls, user):
        with open('app/controllers/db/users.json', 'r') as file:
            deleteUser = json.load(file)
        for i in deleteUser:
            if i['name'] == user:
                deleteUser.remove(i)
                with open('app/controllers/db/users.json', 'w') as file:
                    json.dump(deleteUser, file, indent=4, ensure_ascii=False)
                cls.deleteAccountUserMusics(user)
                return True
        return False
    
    @classmethod
    def getAllthumb(cls):
        with open('app/controllers/db/photoProfile.json','r') as file:
            cls.__thumbProfile = json.load(file)
        return cls.__thumbProfile
    
    @classmethod
    def deleteAccountUserMusics(cls, user):
        with open('app/controllers/db/userMusics.json', 'r') as file:
            deleteUserMusics = json.load(file)
        for i in deleteUserMusics:
            if i['user'] == user:
                deleteUserMusics.remove(i)
                with open('app/controllers/db/userMusics.json', 'w') as file:
                    json.dump(deleteUserMusics, file, indent=4, ensure_ascii=False)
                break
    
    @classmethod
    def changeProfilePhoto(cls, user, newPhoto):
        with open('app/controllers/db/users.json', 'r') as file:
            changePhoto = json.load(file)
        for i in changePhoto:
            if i['name'] == user:
                i['foto'] = newPhoto
                with open('app/controllers/db/users.json', 'w') as file:
                    json.dump(changePhoto, file, indent=4, ensure_ascii=False)
                return True
        return False
    

# ------------------------------------------------------------------------------

class MusicsDB:
    def __init__(self):
        self.__allMusics = []
        self.__userMUsics = []
        
        self.load()

    def getAllMusics(self):
        with open('app/controllers/db/allMusics.json','r') as file:
            self.__allMusics = json.load(file)
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



    def removeFilePath(self, ms):
        musicPath = os.path.join("app", "controllers", "db",'musicsfiles', ms)
        if os.path.exists(musicPath):
            os.remove(musicPath)

    def removeMusic(self, musicName, paramet, username = None):
        ms = music(musicName)
        match paramet:
            case "public":
                musicToRemove = self.verindataB(ms, self.__allMusics)
                data = self.__allMusics
        
            case "private":
                data = self.getUserMusic(username)
                musicToRemove = self.verindataB(ms, data)
                

        if musicToRemove != False:
            data.pop(musicToRemove['index'])
            if paramet == "private":
                self.uptadeUserDb(username, data)
            musicPath = musicToRemove['element']['path']
            if self.verUsersMusics(musicPath) and self.verPublicMusics(musicPath):
                self.removeFilePath(musicPath)
            self.save()
    
    def verPublicMusics(self,musicPath):
        for music in self.__allMusics:
            if music['path'] == musicPath:
                return False
        
        return True

    def uptadeUserDb(self, username, newDb):
        for i in self.__userMUsics:
            if i['user'] == username:
                i['musics'] = newDb
                self.save()

    def verUsersMusics(self, musicPath):
        print("todos os usuarios",self.__userMUsics)
        for user in self.__userMUsics:
            db = self.getUserMusic(user['user'])
            print("banco de dados", db)
            for music in db:
                if music['path'] == musicPath:
                    return False
        
        return True

    def getMusicPath(self,musicName, paramet, user):
        match paramet:  
            case "Privado":
                db = self.getUserMusic(user)
                for music in db:
                    if music['name'] == musicName:
                        return music['path']
        
            case "Publico":
                for music in self.__allMusics:
                    if music['name'] == musicName:
                        return music['path']
        
    def getMusic(self,name, user):
            for userGet in self.__userMUsics:
                if userGet['user'] == user:
                    for music in userGet['musics']:
                        if music['name'] == name:
                            artista = music['artist']
                            thumb = music['thumb']
                            path = music['path']
                            return artista,thumb,path
            for music in self.__allMusics:
                if music['name'] == name:
                    artista = music['artist']
                    thumb = music['thumb']
                    path = music['path']
                    return artista,thumb,path

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

class addMusics():
    def __init__(self, username):
        self.username = username

    def publicMusic(self, musica, title):
        with open('app/controllers/db/allMusics.json', 'r') as file:
            allMusics = json.load(file)
        for i in range(len(allMusics)):
            if allMusics[i]['name'] == title:
                return 'Música já existe!'
        allMusics.append(musica)
        with open('app/controllers/db/allMusics.json','w') as file:
            json.dump(allMusics, file, indent=4,ensure_ascii=False)
        return 'Música foi publicada!.'
        
    
    def verify(self, title):
        with open('app/controllers/db/userMusics.json', 'r') as file:
            userMusics = json.load(file)
        for i in range(len(userMusics)):
            if userMusics[i]['user'] == self.username:
                for j in range(len(userMusics[i]['musics'])):
                    if userMusics[i]['musics'][j]['path'] == title:
                        return True #TEM DOIS TRUE, DEIXAR APENAS ESSE !!!!!!
        return False

    def upMusic(self, musica, artista, title, thumb):
        if musica:
            savepaththumb = 'app/static/assets/thumb/'
            savepath = 'app/controllers/db/musicsfiles/'
            thumb.save(savepaththumb, overwrite=True)
            musica.save(savepath, overwrite=True)
            titleTratado = self.formatarString(title)
            thumblink = 'static/assets/thumb/' + thumb.filename
            teste = {'name': titleTratado, 'artist': artista, 'path': title, 'thumb': thumblink}
            return teste
        return 'Música não encontrada:'
    
    def formatarString(self, title):
        title = title.replace('-', ' ')
        title = title.replace('.mp3', '')
        return title
            
    def salvarMusica(self, musica):
        with open('app/controllers/db/userMusics.json', 'r') as file:
            userMusics = json.load(file)
        for i in range(len(userMusics)):
            if userMusics[i]['user'] == self.username:
                userMusics[i]['musics'].append(musica)
                with open('app/controllers/db/userMusics.json', 'w') as file:
                    json.dump(userMusics, file, indent=4, ensure_ascii=False)
                break
        else:
            teste = {'user': self.username , 'musics': [musica]}
            userMusics.append(teste)
            with open('app/controllers/db/userMusics.json', 'w') as file:
                json.dump(userMusics, file, indent=4, ensure_ascii=False)
        return 'Musica foi salvada!.'