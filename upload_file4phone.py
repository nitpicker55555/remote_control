from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = r"C:\Users\Morning\Desktop"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
        return 'Files uploaded successfully'

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)