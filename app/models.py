from app.extensions import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    pathfile = db.Column(db.String(256), nullable=False)
    temp_pathfile = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(16))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    relation_id = db.Column(db.Integer)


class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    pathfile = db.Column(db.String(256), nullable=False)
    sourcetbl_id = db.Column(db.Integer, nullable=False)
    sourcetbl_name = db.Column(db.String(128), nullable=False)
    source_key_id = db.Column(db.String(64), nullable=False)
    targettbl_id = db.Column(db.Integer, nullable=False)
    targettbl_name = db.Column(db.String(128), nullable=False)
    target_key_id = db.Column(db.String(64), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())