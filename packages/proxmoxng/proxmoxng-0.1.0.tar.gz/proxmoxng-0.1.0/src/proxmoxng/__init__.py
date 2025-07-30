from flask import Flask
from flask_cors import CORS
from proxmoxer import ProxmoxAPI
from flask_sqlalchemy import SQLAlchemy
import os
import tomllib

proxmox = None

if not os.path.exists("/etc/proxmoxng/middleware/config.toml"):
    raise Exception("Config file not found")

with open("/etc/proxmoxng/middleware/config.toml", "rb") as f:
    config = tomllib.load(f)


db_uri = config["database"]["uri"]

db = SQLAlchemy()

from .models.vms import VM

app = Flask(__name__)
CORS(app)  


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_uri

db.init_app(app)

with app.app_context():
    if not os.path.exists(db_uri):
        db.create_all()

print("Database created")
from .flaskapi import main as main_blueprint
print("Registering main blueprint")
app.register_blueprint(main_blueprint)


app.run(host='0.0.0.0', ssl_context=(config["cert"]['cert'], config["cert"]['key']))