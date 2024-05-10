from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla

db = SQLAlchemy()  # Create a database object

# Define models
fsqla.FsModels.set_db_info(db)
