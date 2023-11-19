from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    image_name = image.filename

    # LOGICA DE PROCESAMIENTO DE IMAGEN VA AQUÍ

    return jsonify({'processedImage': image_name})

if __name__ == '__main__':
    app.run(debug=True)
