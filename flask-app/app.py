from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import colorSelection as CS
import pandas as pd
import pathlib
import os

app = Flask(__name__)
CORS(app)

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
app.config['UPLOAD_FOLDER'] = DOWNLOADS_FOLDER
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files and 'image2' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']
    file2 = request.files['image2']

    if file.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected file'})

    file_path1 = os.path.join(pathlib.Path(__file__).parent.resolve(), file.filename)
    file.save(file_path1)

    file_path2 = os.path.join(pathlib.Path(__file__).parent.resolve(), file2.filename)
    file2.save(file_path2)

    print(f"Parent: {pathlib.Path(__file__).parent.resolve()}")

    print(f"You're about to experience Color comparation between {file_path1} and {file_path2}")

    img1 = CS.ColorSelector(file_path1)
    rgb,hsv,lab,resulting_image = img1.obtainColors()
    whereto = pathlib.Path(__file__).parent.resolve().parent.resolve()
    # Imagen de los colores de la primera imagen
    plt.switch_backend('Agg') 
    plt.figure()
    plt.imshow(list(resulting_image))
    plt.axis('off')
    plt.savefig(f"{str(whereto)}/front/src/images/resultado_preliminar_colores.png")
    

    aComparar = img1.loadImage2Compare(file_path2)
    comparaciones = img1.compare_with_new_image(rgb)
    resultados = pd.DataFrame(comparaciones)
    comp = img1.visualize_comparison(comparaciones)

    plt.switch_backend('Agg') 
    plt.figure()
    plt.imshow(comp)
    plt.axis('off')
    plt.savefig(f"{str(whereto)}/front/src/images/resultado_comparacion_colores.png")

    return jsonify({'message': 'Image uploaded successfully', 'file_path': file_path1, 'file_path': file_path2})

@app.route('/analisis', methods=['GET'])
def fetch_image():
    print("AAAAAAAAAAAAAAAAAAAAA")
    return "Hemlo"

if __name__ == '__main__':
    app.run(debug=True)