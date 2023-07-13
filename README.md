[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=637CF7&width=435&lines=Hi!!+Welcome+my+name+is+Gabriel+%E3%83%84;I'm+a+Full+stack+Developer+;From+Argentina+%F0%9F%A7%89)](https://git.io/typing-svg)

### Contactos
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-%230077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabriel-calcagni-659907260) [![Instagram](https://img.shields.io/badge/-Instagram-%23E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/calcagni_gabriel26/?ishid=ZDdkNTZiNTM%3D) 
##
![Version](https://img.shields.io/badge/Version-1.0-blue.svg)
![License](https://img.shields.io/badge/License-GNU%20GPL--3.0-blue.svg)

# Background-Remover

Este es un proyecto hecho con Python para tratar de quitar el fondo de una imagen.

El objetivo principal de este proyecto es brindar una herramienta fácil de usar y eficiente para eliminar fondos no deseados en imágenes. Se espera que sea útil para tareas como edición de fotografías, creación de imágenes con fondo transparente para diseño gráfico, entre otros.

## Estado del Proyecto

El proyecto se encuentra en etapa de desarrollo activo. Se está trabajando en mejorar la precisión y eficiencia del algoritmo de eliminación de fondos. Se agradece cualquier contribución, sugerencia o reporte de errores.

## Instalación

Para utilizar este proyecto, sigue estos pasos:

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias ejecutando el comando `pip install -r requirements.txt`.
3. Ejecuta el script principal para utilizar la herramienta.

## Ejemplos de Uso

Aquí hay un ejemplo básico de cómo utilizar el proyecto:

1- Puedes descargar el zip y ejecutar el archivo `bg-remover.py` en Windows y probar con imágenes no mayores a 1920*1080.

2- Recuerda que este es un proyecto en construcción y contiene errores.

3- Puedes copiar éste código y empezar a afinar el algoritmo. Estarías contribuyendo a la causa! 👀

```python
from flask import Flask, request, jsonify
import cv2
import numpy as np
from mrcnn import utils
from mrcnn import model as modellib

app = Flask(__name__)

# Configuración del modelo
class InferenceConfig(Config):
    NAME = "inference_config"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 2  # Fondo y objeto de interés
    # Resto de parámetros de configuración

# Directorio de los pesos pre-entrenados del modelo Mask R-CNN
WEIGHTS_PATH = "path/to/pretrained/weights.h5"

# Cargar la configuración y los pesos del modelo
config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", config=config, model_dir="")
model.load_weights(WEIGHTS_PATH, by_name=True)

# Función para eliminar el fondo de una imagen
def remove_background(image_path):
    image = cv2.imread(image_path)
    results = model.detect([image], verbose=0)
    r = results[0]
    # Crear una máscara binaria para el fondo
    background_mask = np.where(r['masks'][:,:,0], 0, 255).astype(np.uint8)
    # Aplicar la máscara al fondo de la imagen
    image = cv2.bitwise_and(image, image, mask=background_mask)
    return image

# Ruta para manejar la solicitud POST de eliminación de fondo
@app.route('/eliminar_fondo', methods=['POST'])
def eliminar_fondo():
    # Verificar si se envió una imagen
    if 'image' not in request.files:
        return jsonify({'result': 'error', 'message': 'No se envió ninguna imagen'})
    # Recibir la imagen enviada por el cliente
    image = request.files['image']
    # Guardar la imagen en disco
    image_path = 'temp_image.jpg'
    image.save(image_path)
    try:
        # Procesar la imagen y eliminar el fondo utilizando tu código de eliminación de fondo
        processed_image = remove_background(image_path)
        # Eliminar la imagen temporal
        os.remove(image_path)
        # Devolver la imagen procesada como una respuesta JSON
        _, processed_image_data = cv2.imencode('.jpg', processed_image)
        processed_image_base64 = base64.b64encode(processed_image_data).decode('utf-8')
        return jsonify({'result': 'success', 'image': processed_image_base64})
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run()

