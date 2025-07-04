from app.controllers.datarecord import dataBase, MusicsDB
from bottle import template, redirect, request, response, Bottle, static_file
import socketio
from json import dumps

class Application:

    def __init__(self):

        self.pages = {
            'create': self.create,
            'login': self.login,
            'newUser': self.newUser,
            'menu': self.menu,
            'remove': self.remove,
            'logado': self.logado,
            'admin': self.admin
        }
        self.__musics = MusicsDB()

        self.edited = None
        self.removed = None
        self.created= None
        self.__alteticatedUser = None
        self.__permisionADM = True 

        # Initialize Bottle app
        self.app = Bottle()
        self.setup_routes()

        # Initialize Socket.IO server
        self.sio = socketio.Server(async_mode='eventlet')
        
        # Create WSGI app
        self.wsgi_app = socketio.WSGIApp(self.sio, self.app)


    # estabelecimento das rotas
    def setup_routes(self):
        @self.app.route('/static/<filepath:path>')  
        def serve_static(filepath):
            return static_file(filepath, root='./app/static')

        @self.app.route('/favicon.ico')
        def favicon():
            return static_file('favicon.ico', root='.app/static')

        @self.app.route('/create', method='GET')
        def create_getter():
            return self.render('create')
        
        
        @self.app.route('/create', method='POST')
        def create_action():
            username = request.forms.get('username')
            password = request.forms.get('password')

            print('Usuário recebido:', username)
            print('Senha recebida:', password)
            
            dataBase.load()
            mensage = dataBase.newUser(username, password)

            return self.render('create', mensage)

        @self.app.route('/')
        @self.app.route('/login', method='GET')
        def login_getter():
            return self.render('login')

        @self.app.route('/remove', method='GET')
        def remove_getter():
            return self.render('remove', self.__alteticatedUser)
        
        @self.app.route('/remove', method='POST')
        def remove_action():
            musicsToRemove = request.json
            response.content_type = 'application/json'

            for music in musicsToRemove:
                self.__musics.removeMusic(music, "private")
            return self.__musics.getUserMusicString(self.__alteticatedUser)    
            

        @self.app.route('/permision', method='GET')
        def get_permision():
            return dumps(self.__permisionADM)

        @self.app.route('/admin', method='GET')
        def admin_getter():
            return self.render('admin')
        
        @self.app.route('/admin', method='POST')
        def admin_action():
            act = request.json['paramet']
            file = request.json['data']
            
            response.content_type = 'application/json'

            match act:
                case 'setAdmin':
                    dataBase.setAdmin(file)
                    return dumps(True)
                
                case 'removeUser':
                    self.__musics.removeUser(file)
                    return dumps(dataBase.removeUser(file))
                
                case 'removeMusic':
                    for music in file:
                        self.__musics.removeMusic(music, "public")
                    return dumps(True)
            return
            
        
        @self.app.route('/login', method='POST')
        def login_action():
            username = request.forms.get('username')
            password = request.forms.get('password')

            print('Usuário recebido:', username)
            print('Senha recebida:', password)
            
            verificar = dataBase.verificarLogin(username, password)
            print(verificar)
            if verificar == False:
                print('Não existe')
                return self.render('login')
            else:
                print('Existe')
                self.__alteticatedUser = username
                return self.render('logado', username)
        
        @self.app.route('/menu', method='GET')
        def menu_getter():
            return self.render('menu')
        

    # método controlador de acesso às páginas:
    def render(self, page, parameter=None):
        content = self.pages.get(page, self.login)
        if not parameter:
            return content()
        return content(parameter)

    # métodos controladores de páginas


    def create(self, text = None):
        print(text)
        return template('app/views/html/createUser', mensage = text)
    
    def newUser(self, parameter = None):
        if not parameter:
            return template('app/views/html/teste')
        else:
            return template('app/views/html/teste', username = parameter)
        
    def login(self):
        return template('app/views/html/login')


    def logado(self, user):
        allmusics = self.__musics.getAllMusics()
        userMusic = self.__musics.getUserMusic(user)
        self.__permisionADM = dataBase.verPermisions(user)
        dataBase.connected(user)
        print('permision', self.__permisionADM)
        return template('app/views/html/menu', username = user, allmusics = allmusics, userMusic = userMusic)
    
    def remove(self,user):
        db = self.__musics.getUserMusic(user)
        return template('app/views/html/remove', musicDb = db)
    
    def menu(self):
        allmusics = self.__musics.getAllMusics()
        userMusic = self.__musics.getUserMusic(self.__alteticatedUser)
        return template('app/views/html/menu', username = self.__alteticatedUser, allmusics = allmusics, userMusic = userMusic)

    def admin(self):
        if self.__permisionADM == True:
            allmusics = self.__musics.getAllMusics()
            users = dataBase.getUsers()
            return template(('app/views/html/admin'), musics = allmusics, users = users)
        else:
            return dumps("Usuario Não tem permisão")