import os
import json

import numpy as np
from PIL import Image
import cv2.dnn as dnn  # type: ignore

THIS_FILE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(THIS_FILE_DIR, 'resnet101_dogs.onnx')
LABEL_TO_BREED_PATH = os.path.join(THIS_FILE_DIR, 'label_to_dirname.json')

PROBABILITY_THRESHOLD = 0.01

IMAGE_INPUT_SIZE = (256, 256)

classifier = dnn.readNetFromONNX(MODEL_PATH)
classifier.setPreferableBackend(dnn.DNN_BACKEND_CUDA)
classifier.setPreferableTarget(dnn.DNN_TARGET_CUDA)
layer_names = classifier.getLayerNames()

# Get unconnected layers
classifier_output = []
for unconnected_layer in classifier.getUnconnectedOutLayers():
    if isinstance(unconnected_layer, list):
        unconnected_layer = unconnected_layer[0]
    classifier_output.append(layer_names[unconnected_layer - 1])

with open(LABEL_TO_BREED_PATH, 'r') as f:
    label_to_breed = json.load(f)


def classify_dog(file_stream):
    # Convertir el stream de bytes a un array NumPy usando PIL
    pil_image = Image.open(file_stream)
    # Asegúrate de que la imagen esté en modo RGB
    pil_image = pil_image.convert('RGB')

    image = np.array(pil_image)

    # normalice la imagen
    scale = 0.00392
    mean = (0.485, 0.456, 0.406)
    std = (0.229, 0.224, 0.225)

    image = image.astype(np.float32) / 255.0
    image = ((image - mean) / std).astype(np.float32)

    blob = dnn.blobFromImage(image, 1, IMAGE_INPUT_SIZE,
                             (0, 0, 0), True, crop=False)

    classifier.setInput(blob)
    outputs = classifier.forward(classifier_output)[0][0]

    # Convierta las salidas en una lista estándar
    outputs = outputs.tolist()

    # Asigna los labels a las predicciones
    out = list(zip(label_to_breed, outputs))

    # Elimina las menores al umbral
    out = filter(lambda x: x[1] > PROBABILITY_THRESHOLD, out)

    # Deja solo el top 5, en caso de que haya más de 5
    out = sorted(out, key=lambda x: x[1], reverse=True)[:5]

    return out
