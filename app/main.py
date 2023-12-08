from flask import Flask, jsonify
from config.config import Config
from db.db_connect import db, init_db
from routes.route import main_blueprint

app = Flask(__name__)
init_db(app)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
  app.run(debug=True, port=Config.PORT)