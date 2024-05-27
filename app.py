from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from scripts.pdf_generate import create_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        file = request.files['file']
        size = request.form.get('size', 'A4')
        puzzles_per_page = int(request.form.get('puzzles_per_page', 1))
        solutions_location = request.form.get('solutions_location', 'end')
        solutions_per_page = int(request.form.get('solutions_per_page', 1))
        font_size = int(request.form.get('font_size', 12))
        include_logo = 'include_logo' in request.form

        # Procesar archivo y generar sopa de letras
        words_list = parse_input_file(file)
        pdf = create_pdf(words_list, size, puzzles_per_page, solutions_location, solutions_per_page, font_size, include_logo)
        return send_file(pdf, as_attachment=True, download_name='sopa_de_letras.pdf')
    except Exception as e:
        return render_template('error.html', message=str(e))

def parse_input_file(file):
    words_list = []
    current_list = []
    for line in file.read().decode('utf-8').split('\n'):
        line = line.upper()
        if line.strip() == '':
            if current_list:
                words_list.append(current_list)
                current_list = []
        else:
            current_list.append(line.strip())
    if current_list:
        words_list.append(current_list)
    return words_list

if __name__ == '__main__':
    app.run(debug=True)

