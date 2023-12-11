from flask import Flask
from flask_cors import CORS
from config.config import Config
from db.db_connect import init_db
from routes.route import main_blueprint

app = Flask(__name__)
CORS(app)
init_db(app)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
  app.run(debug=True, port=Config.PORT)