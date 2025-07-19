from app.controllers.datarecord import dataBase, MusicsDB, addMusics
from bottle import template, redirect, request, response, Bottle, static_file
import socketio
from json import dumps

class Application:

    def __init__(self):

        self.pages = {
            'create': self.create,
            'login': self.login,
            'menu': self.menu,
            'adicionarMusicas': self.adicionarMusicas,
            'remove': self.remove,
            'admin': self.admin,
            'conta': self.conta,
            'player': self.player
        }
        self.__musics = MusicsDB()

        self.edited = None
        self.removed = None
        self.created= None
        self.__alteticatedUser = None
        self.__permisionADM = True 
        self.__mensagem= None

        dataBase.load()

        # Initialize Bottle app
        self.app = Bottle()
        self.setup_routes()

        # Initialize Socket.IO server
        self.sio = socketio.Server(async_mode='eventlet')
        self.setup_websocket_events()
        
        # Create WSGI app
        self.wsgi_app = socketio.WSGIApp(self.sio, self.app)

    #pegar cookie
    def get_session_id(self):
        return request.get_cookie('session_id')
    
    #validar
    def existSessionIDUser(self):
        session_id = self.get_session_id()
        verificar, usuario = dataBase.verifyUserWithID(session_id)
        if verificar:
            self.__alteticatedUser = usuario
            print(self.__alteticatedUser)
            print(usuario)
            print(session_id)
            return True
        return False
    
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
        
        @self.app.route('/')
        @self.app.route('/login', method='GET')
        def login_getter():
            usuario = self.existSessionIDUser()
            if usuario:
                return self.render('menu', self.__alteticatedUser)
            return self.render('login')
        
        @self.app.route('/adicionarMusicas', method='GET')
        def adicionarMusicas_getter():
            usuario = self.existSessionIDUser()
            if usuario:
                return self.render('adicionarMusicas', self.__alteticatedUser)
            return self.render('login')
        
        @self.app.route('/remove', method='GET')
        def remove_getter():
            usuario = self.existSessionIDUser()
            if usuario:
                return self.render('remove', self.__alteticatedUser)
            return self.render('login')
        
        @self.app.route('/menu', method='GET')
        def menu_getter():
            usuario = self.existSessionIDUser()
            if usuario:
                print(usuario)
                return self.render('menu', self.__alteticatedUser)
            return self.render('login')

        @self.app.route('/permision', method='GET')
        def get_permision():
            return dumps(self.__permisionADM)

        @self.app.route('/conta', method='GET')
        def conta_getter():
            usuario = self.existSessionIDUser()
            if usuario:
                print(usuario)
                return self.render('conta', self.__alteticatedUser)
            return self.render('login')
        
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
                    self.update_account_list()
                    return dumps(dataBase.removeUser(file))
                
                case 'removeMusic':
                    for music in file:
                        self.__musics.removeMusic(music, "public")
                    return dumps(True)
            return
        
        @self.app.route('/music', method='GET')
        def music_getter():
            return self.render('musicPlay')


        @self.app.route('/music', method='POST')
        def music_play():
            paramet = request.json['paramet']
            musicName = request.json['data']
            response.content_type = 'application/json'

            return dumps(self.__musics.getMusicPath(musicName, paramet, self.__alteticatedUser))
        
        @self.app.route('/controllers/musicsfiles/<filename:path>', method="GET")
        def serve_music(filename):
            return static_file(filename, root='./app/controllers/db/musicsfiles')


        @self.app.route('/adicionarMusicas', method='POST')
        def adicionarMusicas_action():
            upload = request.files.get('file')
            title = upload.filename
            thumb = request.files.get('thumb-music')
            verify = addMusics(self.__alteticatedUser).verify(title)
            if verify:
                foto = dataBase.getProfileFoto(self.__alteticatedUser)
                return template('app/views/html/adicionarMusicas', username=self.__alteticatedUser, foto=foto, mensage='Essa música já existe.', mensagem2=None)
            else:
                typeStatus = request.forms.get('privado-check') == 'true'
                artista = request.forms.get('artista')
                musica = addMusics(self.__alteticatedUser).upMusic(upload,artista, title, thumb)
                mensage = addMusics(self.__alteticatedUser).salvarMusica(musica)
                mensagem2=None
                if typeStatus:
                    mensagem2 = addMusics(self.__alteticatedUser).publicMusic(musica,title)
                    foto = dataBase.getProfileFoto(self.__alteticatedUser)
                return template('app/views/html/adicionarMusicas', username=self.__alteticatedUser, foto=foto, mensage=mensage, mensagem2=mensagem2)

        @self.app.route('/login', method='POST')
        def login_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            username = username.lower()
            print('Usuário recebido:', username)
            print('Senha recebida:', password)

            verificar, session_id = dataBase.verificarLogin(username, password)
            print("verificaçao de login: ", verificar, "id: ", session_id)
            if verificar == False:
                print('Não existe')
                return self.render('login')
            else:
                response.set_cookie('session_id', session_id, path = '/')
                self.__alteticatedUser = username
                dataBase.connected(self.__alteticatedUser)
                self.update_conecteds_list()
                return self.render('menu')
            
        @self.app.route('/remove', method='POST')
        def remove_action():
            musicsToRemove = request.json
            response.content_type = 'application/json'
            for music in musicsToRemove:
                self.__musics.removeMusic(music, "private", self.__alteticatedUser)
            return self.__musics.getUserMusicString(self.__alteticatedUser)    
        
        @self.app.route('/create', method='POST')
        def create_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            username = username.lower()
            print('Usuário recebido:', username)
            print('Senha recebida:', password)
            
            dataBase.load()
            mensage = dataBase.newUser(username, password)
            self.update_account_list()
            return self.render('create', mensage)
        
        @self.app.route('/menu/player', method='POST')
        def playerMenuMusic():
            name = request.forms.get('name')
            artista, thumb, path = self.__musics.getMusic(name)
            return template('app/views/html/player', musica=name, artist=artista, thumb=thumb, path=path)
            
        @self.app.route('/conta', method='POST')
        def conta_action():
            username = self.__alteticatedUser
            verify = dataBase.deleteAccount(username)
            self.update_account_list()
            if verify:
                session_id = self.get_session_id
                if session_id:
                    dataBase.logoutUser(session_id)
                    response.delete_cookie('session_id')
                    return self.render('logout')
            return self.render('conta')
        
        @self.app.route('/conta/changePhoto/', method='POST')
        def changePhoto():
            foto = request.forms.get('photo')
            verify = dataBase().changeProfilePhoto(self.__alteticatedUser, foto)
            if verify:
                return self.render('conta')
            return self.render('conta')
        
        @self.app.route('/conta/changeUsername/', method='POST')
        def changeUsername():
            username = request.forms.get('usuario')
            verify = dataBase.verificarUser(username)
            if verify:
                self.__mensagem = 'Usuário já existe'
                return self.render('conta')
            teste = dataBase.changeUsername(self.__alteticatedUser, username)
            session_id = self.get_session_id()
            if session_id:
                dataBase.logoutUser(session_id)
                response.delete_cookie('session_id')
                self.__mensagem = None
            return self.render('login')

        @self.app.route('/logout', method='GET')
        def logout():
            session_id = self.get_session_id()
            if session_id:
                dataBase.logoutUser(session_id)
                response.delete_cookie('session_id')
                self.update_conecteds_list()
            return self.render('login')
        
        @self.app.route('/player', method='POST')
        def playerMenuMusic():
            music = request.forms.get('music_name')
            artista, thumb, path1 = self.__musics.getMusic(music, self.__alteticatedUser)
            path = '/controllers/musicsfiles/' + path1 
            return template('app/views/html/player', path=path, musica=music, artist=artista, thumb=thumb)
        
    # método controlador de acesso às páginas:
    def render(self, page, parameter=None):
        content = self.pages.get(page, self.login)
        if not parameter:
            return content()
        return content(parameter)

    # métodos controladores de páginas

    def login(self):
        return template('app/views/html/login')
    
    def create(self, text = None):
        print(text)
        return template('app/views/html/createUser', mensage = text)
    
    def adicionarMusicas(self, username=None):
        foto = dataBase.getProfileFoto(self.__alteticatedUser)
        return template('app/views/html/adicionarMusicas',foto=foto, mensage=None, username=self.__alteticatedUser, mensagem2=None)
    
    def player(self, username=None):
        return template('app/views/html/player', path=None, musica='Nome da música', artist='Nome do artista', thumb='/static/indisponivel.png')
    
    def remove(self,username=None):
        db = self.__musics.getUserMusic(self.__alteticatedUser)
        return template('app/views/html/remove', musicDb = db)
    
    def conta(self,username=None):
        foto = dataBase.getProfileFoto(self.__alteticatedUser)
        password = dataBase.getPassword(self.__alteticatedUser)
        allthumbs = dataBase.getAllthumb()
        return template('app/views/html/conta', mensagem=self.__mensagem, foto=foto, allthumbs=allthumbs, username= self.__alteticatedUser, password=password)

    def menu(self, username=None):
        allmusics = self.__musics.getAllMusics()
        userMusic = self.__musics.getUserMusic(self.__alteticatedUser)
        self.__permisionADM = dataBase.verPermisions(self.__alteticatedUser)
        print('permision', self.__permisionADM)
        foto = dataBase.getProfileFoto(self.__alteticatedUser)
        return template('app/views/html/menu', foto=foto, username = self.__alteticatedUser, allmusics = allmusics, userMusic = userMusic)

    def admin(self):
        if self.__permisionADM == True:
            allmusics = self.__musics.getAllMusics()
            users = dataBase.getUsers()
            return template(('app/views/html/admin'), musics = allmusics, users = users)
        else:
            return dumps("Usuario Não tem permisão")
        
    def setup_websocket_events(self):

        @self.sio.event
        async def connect(sid, environ):
            print(f'Client connected: {sid}')
            self.sio.emit('connected', {'data': 'Connected'}, room=sid)

        @self.sio.event
        async def disconnect(sid):
            print(f'Client disconnected: {sid}')

        @self.sio.event
        def conected_user_list(sid, data):
            self.sio.emit('conected_user_list', {'content': data})

        @self.sio.event
        def update_account_list(sid, data):
            self.sio.emit('update_account_list', {'content': data})

    def update_conecteds_list(self):
        print('Conectando Usuario...')
        conecteds = dataBase.getConnectedUsers()
        self.sio.emit('conected_user_list', conecteds)

    def update_account_list(self):
        print('Atualizando a lista de usuários cadastrados...')
        users = dataBase.getUsers()        
        self.sio.emit('update_account_list', users)
