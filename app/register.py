# path registration
from app.controllers.file_uploader import uploader
from app.controllers.data_management import data_mng
from app.controllers.data_preprocessing import data_prep

def register(app):
    app.register_blueprint(uploader, url_prefix="/")
    app.register_blueprint(data_mng, url_prefix="/")
    app.register_blueprint(data_prep, url_prefix="/")