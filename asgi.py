from asgiref.wsgi import WsgiToAsgi
from app import app

# Wrap the Flask WSGI app so it can run under ASGI servers like Uvicorn
asgi_app = WsgiToAsgi(app)
