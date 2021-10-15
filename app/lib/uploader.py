from werkzeug.utils import secure_filename
import os
import datetime
import hashlib

ALLOWED_EXTENSIONS = ['csv', 'xls', 'xlsx']
STORE_FOLDER = os.getcwd() + "/data_store/"
MAX_FILE_SIZE = 2000
MIME_TYPES = ['multipart/form-data']

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_size(file):
    chunk = 10 #chunk size to read per loop iteration; 10 bytes
    data = None
    size = 0
	#keep reading until out of data
    while data != b'':
        data = file.read(chunk)
        size += len(data)
		#return false if the total size of data parsed so far exceeds MAX_FILE_SIZE
        if size > MAX_FILE_SIZE:
            return False
    return True

def get_secured_filename(filename):
    return str(secure_filename(filename))

def allowed_mimetypes(mimetype):
    return mimetype in MIME_TYPES

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def uploads(f):
    if f and allowed_extension(f.filename):
        fileorigin = f.filename.rsplit('.',1)
        fileext = fileorigin[1].lower()
        encfiles = hashlib.md5(get_secured_filename(f.filename).encode('utf-8')).hexdigest()
        pathfile = STORE_FOLDER+"raw/" + encfiles + "." + fileext
        f.save(pathfile)
        return {
            "status": "ok",
            "pathfile": pathfile
        }
    else:
        return {"status": "error"}

def save_df(df):
    filename = str(datetime.datetime.now()) + "_dataset"
    encfiles = hashlib.md5(get_secured_filename(filename).encode("utf-8")).hexdigest()
    pathfile = STORE_FOLDER+"dataset/" + encfiles + ".csv" 
    df.to_csv(pathfile, index=False)
    return pathfile