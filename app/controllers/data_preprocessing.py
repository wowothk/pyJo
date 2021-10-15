from flask import render_template, request, Blueprint, redirect, url_for
from app.models import Data, Relation
from app.extensions import db
from app.lib.preprocessing import *
from app.lib.uploader import save_df
from app.lib.helper import *
import os

STORE_FOLDER = os.getcwd() + "/data_store/"

data_prep = Blueprint('data_prep', __name__)

@data_prep.route("/rename", methods=["POST"])
def rename():
    id = request.args.get("id")
    col = request.form.get("col")
    repl = request.form.get("repl")
    
    origin = Data.query.filter_by(id=id).first()
    name = origin.name
    
    if origin.temp_pathfile != '':
        df = reader(origin.temp_pathfile)
    else:
        df = reader(origin.pathfile)

    df = rename_col(df,col,repl)

    filename = str(origin.pathfile).split("/")[-1]
    save_to_datastore(df, STORE_FOLDER + "/temp/" + filename)
    origin.temp_pathfile = STORE_FOLDER + "/temp/" + filename
    db.session.commit()
    return redirect(url_for("data_mng.prep", id=id))
    

@data_prep.route("/delete_col", methods=["POST"])
def delete():
    id = request.args.get("id")
    col = request.form.get("col")

    origin = Data.query.filter_by(id=id).first()
    name = origin.name

    df = reader(origin.temp_pathfile)
    df = del_column(df, col)
    
    filename = str(origin.pathfile).split("/")[-1]
    save_to_datastore(df, STORE_FOLDER + "/temp/" + filename)
    origin.temp_pathfile = STORE_FOLDER + "/temp/" + filename
    db.session.commit()
    return redirect(url_for("data_mng.prep", id=id))

@data_prep.route("/select_col", methods=["POST"])
def select():
    id = request.args.get("id")
    cols = request.form.getlist("cols")

    origin = Data.query.filter_by(id=id).first()
    name = origin.name

    if origin.temp_pathfile != '':
        df = reader(origin.temp_pathfile)
    else:
        df = reader(origin.pathfile)

    df = select_column(df, cols)
    filename = str(origin.pathfile).split("/")[-1]
    save_to_datastore(df, STORE_FOLDER + "/temp/" + filename)
    origin.temp_pathfile = STORE_FOLDER + "/temp/" + filename
    db.session.commit()
    return redirect(url_for("data_mng.prep", id=id))

@data_prep.route("/num_filter", methods=["POST"])
def num_filter():
    id = request.args.get("id")
    col = request.form.get("col")
    max = request.form.get("max")
    min = request.form.get("min")

    max = float(max) if max!='' else None
    min = float(min) if min!='' else None

    origin = Data.query.filter_by(id=id).first()
    name = origin.name
    if origin.temp_pathfile != '':
        df = reader(origin.temp_pathfile)
    else:
        df = reader(origin.pathfile)

    df = filter(df, col, max, min)
    filename = str(origin.pathfile).split("/")[-1]
    save_to_datastore(df, STORE_FOLDER + "/temp/" + filename)
    origin.temp_pathfile = STORE_FOLDER + "/temp/" + filename
    db.session.commit()
    return redirect(url_for("data_mng.prep", id=id))


@data_prep.route("/str_filter", methods=["POST"])
def str_filter():
    id = request.args.get("id")
    col = request.form.get("col")
    pat = request.form.get("pat")
    method = request.form.get("method")

    origin = Data.query.filter_by(id=id).first()
    name = origin.name

    if origin.temp_pathfile != '':
        df = reader(origin.temp_pathfile)
    else:
        df = reader(origin.pathfile)
    df = filter_str(df, col, pat, method)

    filename = str(origin.pathfile).split("/")[-1]
    save_to_datastore(df, STORE_FOLDER + "/temp/" + filename)
    origin.temp_pathfile = STORE_FOLDER + "/temp/" + filename
    db.session.commit()
    return redirect(url_for("data_mng.prep", id=id))
    


@data_prep.route("/str_replace", methods=["POST"])
def str_replace():
    id = request.args.get("id")
    col = request.form.get("col")
    pat = request.form.get("pat")
    repl = request.form.get("repl")

    origin = Data.query.filter_by(id=id).first()
    name = origin.name

    if origin.temp_pathfile != '':
        df = reader(origin.temp_pathfile)
    else:
        df = reader(origin.pathfile)
    df = replace_str(df, col, pat, repl)

    filename = str(origin.pathfile).split("/")[-1]
    save_to_datastore(df, STORE_FOLDER + "/temp/" + filename)
    origin.temp_pathfile = STORE_FOLDER + "/temp/" + filename
    db.session.commit()
    return redirect(url_for("data_mng.prep", id=id))


@data_prep.route("/integration", methods=["GET", "POST"])
def integration():
    if request.method == "GET":
        fields, tables=list_relation(Data)
        info = Relation.query.all()
        return render_template("integration.html", fields=fields, 
            tables=tables, data=info)
    else:
        source = request.form.get("source")
        source_id = request.form.get("source_id")
        target = request.form.get("target")
        target_id = request.form.get("target_id")
        method = request.form.get("method")

        dt1 = Data.query.filter_by(id=source).first()
        dt2 = Data.query.filter_by(id=target).first()
        
        src_tbl = reader(dt1.pathfile)
        trg_tbl = reader(dt2.pathfile)

        df = join(src_tbl, source_id, trg_tbl, target_id, method)
        pathfile = save_df(df)

        rel = Relation(
            pathfile=pathfile,
            sourcetbl_id=dt1.id, 
            sourcetbl_name=dt1.name,
            source_key_id=source_id,
            targettbl_id=dt2.id,
            targettbl_name=dt2.name,
            target_key_id=target_id
        )

        db.session.add(rel)
        db.session.commit()

        ndata = Data(
            name=dt1.name+"_"+dt2.name+"_"+str(method),
            pathfile=pathfile,
            temp_pathfile="",
            status="dataset",
            relation_id=rel.id
        )
        db.session.add(ndata)
        db.session.commit()

        fields, tables=list_relation(Data)
        info = Relation.query.all()
        return render_template("integration.html", fields=fields, 
            tables=tables, data=info)