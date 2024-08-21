from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import PyPDF2
import docx
import json


load_dotenv()

app = Flask(__name__)
CORS(app)


#GEt the environement variable
app.config['DEBUG']=os.environ.get('FLASK_DEBUG')

def pdf_to_json(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_text = {}

    for page_num, page in enumerate(pdf_reader.pages):
        pdf_text[f"page_{page_num + 1}"] = page.extract_text()

    return pdf_text

def docx_to_json(docx_file):
    doc = docx.Document(docx_file)
    doc_text = {}

    for i, para in enumerate(doc.paragraphs):
        doc_text[f"paragraph_{i + 1}"] = para.text

    return doc_text

def txt_to_json(txt_file):
    txt_text = {}

    for i, line in enumerate(txt_file.readlines()):
        txt_text[f"line_{i + 1}"] = line.strip()

    return txt_text

@app.route('/convert', methods=['POST'])
def convert_file_to_json():
    print(request.files)  # Log les fichiers reçus

    if 'file' not in request.files:
        if 'flie' in request.files:
            file = request.files['flie']
        else:
            return jsonify({"error": "No file provided or incorrect key used"}), 400
    else:
        file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_extension = file.filename.split('.')[-1].lower()

    try:
        if file_extension == 'pdf':
            file_json = pdf_to_json(file)
        elif file_extension == 'docx':
            file_json = docx_to_json(file)
        elif file_extension == 'txt':
            file_json = txt_to_json(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        return jsonify(file_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
