import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton

# Variables globales
ruta_imagen = None
imagen_cargada = None

# Función para cargar la imagen al hacer clic en el botón "Cargar imagen"
def cargar_imagen():
    global ruta_imagen, imagen_cargada
    ruta_imagen, _ = QFileDialog.getOpenFileName(options=QFileDialog.Options())  # Ventana de diálogo para seleccionar un archivo
    imagen_cargada = QtGui.QPixmap(ruta_imagen)  # Cargar la imagen seleccionada
    etiqueta_imagen.setPixmap(imagen_cargada.scaledToHeight(1080, QtCore.Qt.SmoothTransformation))

# Función para descargar la imagen con el fondo removido al hacer clic en el botón "Descargar imagen"
def descargar_imagen():
    global ruta_imagen, imagen_cargada
    if ruta_imagen is None:
        return  # No se ha cargado ninguna imagen previamente
    
    # Cargar la imagen utilizando OpenCV
    imagen_cv = cv2.imread(ruta_imagen)

    # Convertir la imagen de BGR a RGB
    imagen_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)

    # Redimensionar la imagen si es necesario
    max_size = (1920, 1080)  # Tamaño máximo permitido (1080p)
    imagen_rgb = cv2.resize(imagen_rgb, max_size)

    # Crear una máscara inicial para la segmentación
    mascara = np.zeros(imagen_rgb.shape[:2], np.uint8)

    # Detectar contornos en la imagen
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar el contorno más grande (supuesto objeto principal)
    contorno_objeto = max(contornos, key=cv2.contourArea)

    # Obtener el rectángulo delimitador del contorno
    x, y, w, h = cv2.boundingRect(contorno_objeto)

    # Ajustar la región de interés alrededor del objeto
    rect = (x, y, x + w, y + h)

    # Aplicar el algoritmo GrabCut para remover el fondo
    cv2.grabCut(imagen_rgb, mascara, rect, None, None, 5, cv2.GC_INIT_WITH_RECT)

    # Crear una máscara binaria donde los píxeles con valores 0 y 2 son considerados fondo, y los píxeles con valores 1 y 3 son considerados primer plano
    mascara_binaria = np.where((mascara == 2) | (mascara == 0), 0, 1).astype('uint8')

    # Aplicar la máscara al objeto principal en la imagen original
    imagen_final = imagen_rgb * mascara_binaria[:, :, np.newaxis]

    # Convertir la imagen final a formato PIL y corregir el perfil de color
    imagen_final_pil = Image.fromarray(imagen_final)
    imagen_final_pil = imagen_final_pil.convert("RGB")

    # Guardar la imagen con el fondo removido
    ruta_guardado, _ = QFileDialog.getSaveFileName(None, "Guardar imagen", "", "JPEG Files (*.jpg);;PNG Files (*.png)")  # Ventana de diálogo para guardar la imagen
    imagen_final_pil.save(ruta_guardado)
    print("Imagen guardada con éxito (fondo removido)")

# Crear la aplicación y la ventana principal
app = QtWidgets.QApplication([])
app.setStyle('Fusion')  # Establecer el estilo de la aplicación como Fusion

# Crear una paleta de colores personalizada para los botones
paleta = QtGui.QPalette()
paleta.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
paleta.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))

# Establecer la paleta de colores personalizada para los botones
app.setPalette(paleta)

# Establecer estilos CSS para los botones y la ventana principal
estilos = """
    QMainWindow {
        background-color: #333;
    }

    QPushButton {
        background-color: #555;
        color: #FFF;
        padding: 8px 16px;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #888;
    }

    QLabel {
        background-color: #000;
        border: 1px solid #FFF;
    }
"""

# Crear la ventana principal
ventana = QtWidgets.QMainWindow()
ventana.setStyleSheet(estilos)

# Crear el botón "Cargar imagen"
boton_cargar = QPushButton("Cargar imagen", ventana)
boton_cargar.clicked.connect(cargar_imagen)
boton_cargar.setGeometry(QtCore.QRect(10, 10, 150, 30))

# Crear el botón "Descargar imagen"
boton_descargar = QPushButton("Descargar imagen", ventana)
boton_descargar.clicked.connect(descargar_imagen)
boton_descargar.setGeometry(QtCore.QRect(10, 50, 150, 30))

# Crear una etiqueta para mostrar la imagen
etiqueta_imagen = QLabel(ventana)
etiqueta_imagen.setGeometry(QtCore.QRect(180, 10, 1024, 720))

# Mostrar la ventana principal
ventana.show()
app.exec()
