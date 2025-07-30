# Simply-ocr 1.0.0

[By Jeroben Guzmán ](https://github.com/jeroguzman)

<br>

For text extraction from images on a simple way / Para extraer texto de imagenes de forma sencilla

<br>

## 💡 Prerequisites

   [Python 3](https://www.python.org/downloads/release/python-3111/)

<br>

## 🚀 Features

- Preprocesamiento avanzado: binarización, eliminación de ruido, ajuste de contraste, redimensionado, selección de región (ROI).
- Soporte multilenguaje y detección de idiomas instalados.
- Extracción de texto estructurado (texto y bounding boxes).
- Guardado de texto extraído a archivo.
- Visualización de la imagen preprocesada para debugging.

<br>

## 📦 Instalación de dependencias

Asegúrate de tener instalados:
- opencv-python
- scikit-image
- pytesseract
- matplotlib

Puedes instalar todo con:

```
pip install opencv-python scikit-image pytesseract matplotlib
```

<br>

## 📚 Ejemplos

```python
from simply_ocr import (
    read_image_en, read_image_es, read_image_multi_lang, get_available_languages,
    save_text_to_file, show_preprocessed_image, read_image
)

# Extraer texto en inglés o español
read_image_en('test.jpg')
read_image_es('test.jpg')

# Extraer texto en varios idiomas y obtener datos estructurados
result = read_image_multi_lang('test.jpg', ['eng', 'spa'], return_data='dict')
print(result['text'])

# Extraer texto de una región específica y mostrar la imagen preprocesada
roi = (100, 200, 300, 100)  # x, y, w, h
texto = read_image('test.jpg', lang='eng', preprocess_opts={'roi': roi, 'binarize': True, 'remove_noise': True})
show_preprocessed_image('test.jpg', preprocess_opts={'roi': roi})

# Guardar el texto extraído en un archivo
if texto:
    save_text_to_file(texto, 'salida.txt')

# Consultar los idiomas disponibles en tu instalación de Tesseract
print(get_available_languages())
```

<br>

## 🧩 Casos de uso

### 1. Digitalización de documentos escaneados
Extrae texto de facturas, recibos, contratos o cualquier documento escaneado para su almacenamiento o análisis automatizado.

```python
texto = read_image('factura.png', lang='spa')
print(texto)
```

### 2. Procesamiento de imágenes de cámaras o móviles
Ideal para extraer texto de fotos tomadas con el móvil, por ejemplo, carteles, pizarras o notas manuscritas.

```python
texto = read_image('foto_pizarra.jpg', lang='spa', preprocess_opts={'binarize': True, 'remove_noise': True})
```

### 3. Extracción de texto multilingüe
Cuando una imagen contiene texto en varios idiomas (por ejemplo, etiquetas de productos internacionales).

```python
result = read_image_multi_lang('etiqueta.jpg', ['eng', 'spa'], return_data='dict')
print(result['text'])
```

### 4. OCR en regiones específicas (ROI)
Extrae texto solo de una parte de la imagen, útil para formularios o layouts fijos.

```python
roi = (50, 100, 200, 50)  # x, y, w, h
texto = read_image('formulario.png', lang='spa', preprocess_opts={'roi': roi})
```

### 5. Automatización de flujos de trabajo
Guarda automáticamente el texto extraído para su posterior procesamiento o integración con otros sistemas.

```python
texto = read_image('ticket.jpg', lang='spa')
if texto:
    save_text_to_file(texto, 'ticket.txt')
```

### 6. Visualización y ajuste de preprocesamiento
Ajusta parámetros y visualiza el resultado para mejorar la precisión del OCR.

```python
show_preprocessed_image('documento.jpg', preprocess_opts={'contrast': 1.5, 'binarize': True})
```

<br>

## 📝 Notas
- Puedes personalizar el preprocesamiento usando el parámetro `preprocess_opts` en las funciones.
- Para usar la visualización, asegúrate de tener `matplotlib` instalado.
- El OCR funciona mejor con imágenes nítidas y bien contrastadas.