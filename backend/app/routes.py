import time
from model.model_utils import classify_dog
from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)


@main.route('/api/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    start_time = time.time()

    file = request.files['file']

    # Convertir el FileStorage a un stream de bytes
    file_stream = file.stream

    # Llamar a la función classify_dog
    results = classify_dog(file_stream)
    total_time = time.time() - start_time

    print(f'Tiempo total: {total_time} segundos, resultados: {results}')

    return jsonify(results)
