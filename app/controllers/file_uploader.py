from flask import url_for, Blueprint, request, redirect
from app.lib.uploader import uploads
from app.models import Data
from app.extensions import db

uploader = Blueprint('uploader', __name__)

@uploader.route("/upload", methods=["POST"])
def upload():
    f = request.files['file']
    name = request.form.get("name")
    upload_data = uploads(f)
    if upload_data["status"] == "ok":
        newdata = Data(
            name=name,
            pathfile=upload_data["pathfile"],
            temp_pathfile='',
            status="raw"
        )
        db.session.add(newdata)
        db.session.commit()
        return redirect(url_for('data_mng.index'))