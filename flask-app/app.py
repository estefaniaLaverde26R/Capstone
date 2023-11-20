from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
app.config['UPLOAD_FOLDER'] = DOWNLOADS_FOLDER
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST','GET'])
def upload_image():
    if 'image' not in request.files and 'image2' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']
    file2 = request.files['image2']

    if file.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected file'})

    file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path1)
    file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
    file2.save(file_path2)

    return jsonify({'message': 'Image uploaded successfully', 'file_path': file_path1, 'file_path': file_path2})



if __name__ == '__main__':
    app.run(debug=True)