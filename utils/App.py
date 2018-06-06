
from flask import Flask

from utils.settings import TEMPLATE_DIR, STATIC_DIR

from App.user_views import user_blueprint
from App.house_views import house_blueprint
from App.order_views import order_blueprint

from utils.functions import init_ext


def create_app(config):

    app = Flask(__name__,
                template_folder=TEMPLATE_DIR,
                static_folder=STATIC_DIR)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    app.config.from_object(config)

    init_ext(app)

    return app

