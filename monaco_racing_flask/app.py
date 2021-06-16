from flask import Flask, redirect
from flasgger import Swagger
from playhouse.flask_utils import FlaskDB
from .config import config_by_name

db_wrapper = FlaskDB()


def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    swag = Swagger(app)
    db_wrapper.init_app(app)

    from .api.v1.resources import api_bp as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    @app.route('/')
    def redirect_to_apidocs():
        return redirect("/apidocs", code=302)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
