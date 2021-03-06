import os
from flask import Flask, render_template

from chgallery.db import get_db_session
from chgallery.db.declarative import Image
from chgallery.middleware import PrefixMiddleware


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='sqlite:///{}'.format(os.path.join(app.instance_path, 'chgallery.sqlite')),
        UPLOAD_PATH=os.path.join(app.instance_path, 'uploads'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance config exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # create directory for uploaded file if doesn't exist
    try:
        os.makedirs(os.path.join(app.config['UPLOAD_PATH'], 'thumbs'))
        os.makedirs(os.path.join(app.config['UPLOAD_PATH'], 'previews'))
    except OSError:
        pass

    # In case that application is mounted outside of the server root,
    # e.g. /admin we can set this common prefix here for all url rules.
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config["ROOT_URL_PREFIX"])  # type: ignore

    # basic view for non-registered users
    @app.route('/')
    def index():
        images = get_db_session().query(Image).order_by(Image.id).all()
        return render_template('index.html', images=images)

    from chgallery.db import init_app
    init_app(app)

    from chgallery import auth
    app.register_blueprint(auth.bp)

    from chgallery import image
    app.register_blueprint(image.bp)

    return app
