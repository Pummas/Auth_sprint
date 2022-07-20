from core.config import app
from v1.routes import routes


app.register_blueprint(routes)


def main(flask_app):
    flask_app.run(debug=True, host='0.0.0.0', port=5001)


if __name__ == '__main__':
    main(app)
