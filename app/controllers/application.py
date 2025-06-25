from app.controllers.datarecord import UserRecord, MessageRecord, dataBase, MusicsDB
from bottle import template, redirect, request, response, Bottle, static_file
import socketio


class Application:

    def __init__(self):

        self.pages = {
            'create': self.create,
            'login': self.login,
            'newUser': self.newUser,
            'menu': self.menu,
            'remove': self.remove,
            'logado': self.logado
        }
        self.__users = UserRecord()
        self.__messages = MessageRecord()
        self.__musics = MusicsDB()

        self.edited = None
        self.removed = None
        self.created= None
        self.__alteticatedUser = None

        # Initialize Bottle app
        self.app = Bottle()
        self.setup_routes()

        # Initialize Socket.IO server
        self.sio = socketio.Server(async_mode='eventlet')
        self.setup_websocket_events()

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

        @self.app.route('/login', method='POST')
        def login_action():
            username = request.forms.get('username')
            return self.render('newUser', username)
        
        @self.app.route('/remove', method='GET')
        def remove_getter():
            __userName = "teste"
            return self.render('remove', __userName)
        
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
        def remove_getter():
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
        
    def login(self, text = None):
        return template('app/views/html/login', username = text)


    def logado(self, user):
        allmusics = self.__musics.getAllMusics()
        userMusic = self.__musics.getUserMusic(user)
        return template('app/views/html/menu', username = user, allmusics = allmusics, userMusic = userMusic)
    
    def remove(self,user):
        db = self.__musics.getUserMusic(user)
        return template('app/views/html/remove', musicDb = db)
    
    def menu(self):
        allmusics = self.__musics.getAllMusics()
        userMusic = self.__musics.getUserMusic(self.__alteticatedUser)
        return template('app/views/html/menu', username = self.__alteticatedUser, allmusics = allmusics, userMusic = userMusic)


    # Websocket:
    def setup_websocket_events(self):

        @self.sio.event
        async def connect(sid, environ):
            print(f'Client connected: {sid}')
            self.sio.emit('connected', {'data': 'Connected'}, room=sid)

        @self.sio.event
        async def disconnect(sid):
            print(f'Client disconnected: {sid}')

        # recebimento de solicitação de cliente para atualização das mensagens
        @self.sio.event
        def message(sid, data):
            objdata = self.newMessage(data)
            self.sio.emit('message', {'content': objdata.content, 'username': objdata.username})

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_users_event(sid, data):
            self.sio.emit('update_users_event', {'content': data})

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_account_event(sid, data):
            self.sio.emit('update_account_event', {'content': data})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários LOGAR ou DESLOGAR
    # este método vai forçar esta atualização em todos os CHATS ativos. Este
    # método é chamado sempre que a rota ''
    def update_users_list(self):
        print('Atualizando a lista de usuários conectados...')
        users = self.__users.getAuthenticatedUsers()
        users_list = [{'username': user.username} for user in users.values()]
        self.sio.emit('update_users_event', {'users': users_list})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários se removerem
    # este método vai comunicar todos os Administradores ativos.
    def update_account_list(self):
        print('Atualizando a lista de usuários cadastrados...')
        users = self.__users.getUserAccounts()
        users_list = [{'username': user.username} for user in users]
        self.sio.emit('update_account_event', {'accounts': users_list})
