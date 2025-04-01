from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from app import db, app  

with app.app_context():
    db.session.execute(text("DELETE FROM stroop_result;"))
    db.session.commit()
