from flask import Flask
from flask import request, flash, render_template, redirect, url_for, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from pypdftk import get_num_pages, dump_data_fields, fill_form
import json
#template_dir = os.path.abspath('templates')
#app = Flask(__name__, template_folder=template_dir)

UPLOAD_FOLDER = os.path.abspath('tmp')
ALLOWED_EXTENSIONS_PDF = {'pdf'}
ALLOWED_EXTENSIONS_DATA = {'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF


def allowed_file_data(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_DATA

def jsondump(pdffile):
    campos = dump_data_fields(pdffile)
    lista = {}
    for campo in campos:
        lista[campo['FieldName']] = ''
    return lista


@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/pdf', methods=['POST'])
def pdffill():
    pdffile = ''
    datafile = ''
    if request.method == 'POST':
        if 'pdffile' in request.files:
            file = request.files['pdffile']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                pdffile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(pdffile)

        if 'datafile' in request.files:
            file = request.files['datafile']
            if file and allowed_file_data(file.filename):
                filename = secure_filename(file.filename)
                datafile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], datafile))
        if pdffile != '' and datafile != '':
            datos = {}
            with open(datafile) as json_file:
                datos = json.load(json_file)
            outfile = pdffile+'x'
            fill_form(pdffile, datos, outfile)
            return send_file(outfile, attachment_filename='file.pdf')
        else:
            return jsonify(jsondump(pdffile))
    else:
        return "error"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
