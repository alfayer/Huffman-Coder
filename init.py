import logging
import uuid

from flask import Flask, g, request
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY

from route.debug import debug_bp
from route.oss import oss_bp
from route.welcome import welcome_bp
from route.monitor import monitor_bp


def create_app():
    app = Flask(__name__)
    #app.wsgi_app=make_wsgi_app(REGISTRY)
    # 载入配置
    app.config.from_pyfile('./config.py')

    logging.basicConfig(level=logging.INFO)
    with app.app_context():
        # 注册路由
        app.register_blueprint(welcome_bp)
        app.register_blueprint(monitor_bp)
        app.register_blueprint(oss_bp)
        app.register_blueprint(debug_bp)

    @app.before_request
    def before_request():
        # 从请求头中获取 request-id
        g.request_id = request.headers.get('x-fc-request-id', uuid.uuid4())

    @app.after_request
    def after_request(response):
        # 移除request-id
        g.request_id = ''
        return response
    


    return app
