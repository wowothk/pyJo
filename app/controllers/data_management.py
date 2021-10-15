from flask import request, Blueprint
from flask import render_template, url_for, redirect
from app.models import Data, Relation
from app.extensions import db
from app.lib.helper import *
import os

STORE_FOLDER = os.getcwd() + "/data_store/"

data_mng = Blueprint('data_mng', __name__)

@data_mng.route('/', methods=['GET'])
def index():
    data = Data.query.all()
    return render_template("index.html", 
            list_info=data, head=None, 
            values=None, pagename="rawData")

@data_mng.route('show', methods=['GET'])
def show():
    id = request.args.get('id')
    origin = Data.query.filter_by(id=id).first()
    name = origin.name
    path = origin.pathfile
    df = reader(path)
    head, values = table_return(df)
    status = origin.status
    return render_template("show.html", 
                head=head, values=values, 
                name=name, id=id, status=status)

@data_mng.route('prep', methods=['GET'])
def prep():
    id = request.args.get('id')
    origin = Data.query.filter_by(id=id).first()
    name = origin.name
    path = origin.temp_pathfile
    df = reader(path)
    head, values = table_return(df)
    status = origin.status
    return render_template("show.html", 
                head=head, values=values, 
                name=name, id=id, status=status)

@data_mng.route('delete', methods=["POST"])
def delete():
    id = request.args.get('id')
    data = Data.query.filter_by(id=id).first()
    path = data.pathfile

    if data.relation_id:
        rel = Relation.query.filter_by(
                    id=data.relation_id).first()
        db.session.delete(rel)
        db.session.commit()

    db.session.delete(data)
    db.session.commit()

    os.remove(path)
    return redirect(url_for('data_mng.index'))

@data_mng.route("dataset", methods=["GET"])
def dataset():
    data = Data.query.filter_by(status="dataset").all()
    return render_template("index.html", list_info=data,
            pagename="dataset")

@data_mng.route("save_dataset", methods=["POST"])
def save_dataset():
    id = request.args.get("id")
    data = Data.query.filter_by(id=id).first()

    if data.temp_pathfile != '':
        df = reader(data.temp_pathfile)
    else:
        df = reader(data.pathfile)

    filename = str(data.pathfile).split("/")[-1]
    data.status = "dataset"
    save_to_datastore(df, STORE_FOLDER + "dataset/" + filename)
    data.temp_pathfile = ""
    data.pathfile = STORE_FOLDER + "dataset/" + filename
    db.session.commit()

    os.remove(STORE_FOLDER+ "raw/" + filename)
    try:
        os.remove(STORE_FOLDER+ "temp/" + filename)
    except:
        pass
    return redirect(url_for("data_mng.dataset"))

@data_mng.route("save_raw", methods=["POST"])
def save_raw():
    id = request.args.get("id")
    data = Data.query.filter_by(id=id).first()

    if data.temp_pathfile != '':
        df = reader(data.temp_pathfile)
    else:
        df = reader(data.pathfile)

    filename = str(data.pathfile).split("/")[-1]
    save_to_datastore(df, STORE_FOLDER + "raw/" + filename)
    data.temp_pathfile = ""
    data.pathfile = STORE_FOLDER + "raw/" + filename
    db.session.commit()
    os.remove(STORE_FOLDER+ "temp/" + filename)
    return redirect(url_for("data_mng.index"))

@data_mng.route("delete_merge", methods=["POST"])
def delete_merge():
    id = request.args.get("id")
    rel = Relation.query.filter_by(id=id).first()

    db.session.delete(rel)
    db.session.commit()

    data = Data.query.filter_by(relation_id=id).first()
    path = data.pathfile

    db.session.delete(data)
    db.session.commit()

    os.remove(path)
    return redirect(url_for("data_prep.integration"))

@data_mng.route("show_integrate", methods=["GET"])
def show_integrate():
    rel_id = request.args.get("id")
    data = Data.query.filter_by(relation_id=rel_id).first()
    path = data.pathfile
    df = reader(path)
    head, values = table_return(df)
    status = data.status
    return render_template("show.html", 
                head=head, values=values, 
                name=data.name, id=id, status=status)