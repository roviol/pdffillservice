from flask import Flask
from flask import request, flash, render_template, redirect, url_for, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from pypdftk import get_num_pages, dump_data_fields, fill_form
import json
from docxtpl import DocxTemplate
from xlstpl.writer import BookWriter

#template_dir = os.path.abspath('templates')
#app = Flask(__name__, template_folder=template_dir)

UPLOAD_FOLDER = os.path.abspath('tmp')
ALLOWED_EXTENSIONS_PDF = {'pdf'}
ALLOWED_EXTENSIONS_DOCX = {'docx'}
ALLOWED_EXTENSIONS_XLS = {'xls'}
ALLOWED_EXTENSIONS_DATA = {'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF

def allowed_file_docx(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_DOCX


def allowed_file_xls(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_XLS


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
                file.save(datafile)
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


@app.route('/docx', methods=['POST'])
def docxfill():
    docxfile = ''
    datafile = ''
    if request.method == 'POST':
        if 'docxfile' in request.files:
            file = request.files['docxfile']
            if file and allowed_file_docx(file.filename):
                filename = secure_filename(file.filename)
                docxfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(docxfile)

        if 'datafile' in request.files:
            file = request.files['datafile']
            if file and allowed_file_data(file.filename):
                filename = secure_filename(file.filename)
                datafile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(datafile)
        if docxfile != '' and datafile != '':
            datos = {}
            with open(datafile) as json_file:
                datos = json.load(json_file)
            outfile = docxfile+'x'
            tpl = DocxTemplate(docxfile)
            tpl.render(datos)
            tpl.save(outfile)
            return send_file(outfile, attachment_filename='file.docx')
        else:
            return jsonify({})
    else:
        return "error"


@app.route('/xls', methods=['POST'])
def xlsfill():
    xlsfile = ''
    datafile = ''
    if request.method == 'POST':
        if 'xlsfile' in request.files:
            file = request.files['xlsfile']
            if file and allowed_file_xls(file.filename):
                filename = secure_filename(file.filename)
                xlsfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(xlsfile)

        if 'datafile' in request.files:
            file = request.files['datafile']
            if file and allowed_file_data(file.filename):
                filename = secure_filename(file.filename)
                datafile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(datafile)
        if xlsfile != '' and datafile != '':
            datos = {}
            with open(datafile) as json_file:
                datos = json.load(json_file)
            outfile = xlsfile+'x'
            tpl = BookWriter(xlsfile)
            #tpl.render(datos)
            tpl.render_book(payloads=[datos])
            #tpl.render_sheet(person_info2, 'form2', 1)
            tpl.save(outfile)
            return send_file(outfile, attachment_filename='file.xls')
        else:
            return jsonify({})
    else:
        return "error"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
