from app.controllers.application import Application


# Inicialize a aplicação
app = Application()


# executa a aplicação
if __name__ == '__main__':

    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app.wsgi_app)
