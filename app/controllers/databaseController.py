import json
from backend.models.userModel import user

class dataBase():
    __dataB = [{}]

    @classmethod
    def load(cls):
        with open("backend/db/Datas.json", "r") as file:
            cls.__dataB = json.load(file)

    @classmethod
    def save(cls):
        with open("backend/db/Datas.json", "w") as file:
            json.dump(cls.__dataB, file, indent=4)


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
            print("usario add")
        else:
            print('usuario ja existe')

