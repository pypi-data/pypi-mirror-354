import cv2
from skimage import io
from pytesseract import pytesseract, Output
from typing import Optional, List, Tuple, Dict, Any, Union
import numpy as np
import os

def preprocess_image(
    image_path: str,
    grayscale: bool = True,
    binarize: bool = True,
    threshold: int = 120,
    remove_noise: bool = False,
    contrast: Optional[float] = None,
    resize: Optional[Tuple[int, int]] = None,
    roi: Optional[Tuple[int, int, int, int]] = None,
) -> np.ndarray:

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No se encontró la imagen: {image_path}")
    img = io.imread(image_path)
    if grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if contrast:
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=0)
    if binarize:
        img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    if remove_noise:
        img = cv2.medianBlur(img, 3)
    if resize:
        img = cv2.resize(img, resize, interpolation=cv2.INTER_AREA)
    if roi:
        x, y, w, h = roi
        img = img[y:y+h, x:x+w]
    return img

def read_image(
    image_path: str,
    lang: str = 'eng',
    threshold: int = 120,
    print_text: bool = False,
    preprocess_opts: Optional[Dict[str, Any]] = None,
    return_data: str = 'text',
    tesseract_config: str = '',
) -> Union[str, Dict[str, Any], None]:

    try:
        opts = preprocess_opts or {}
        opts.setdefault('threshold', threshold)
        img = preprocess_image(image_path, **opts)
        if return_data == 'dict' or return_data == 'both':
            data = pytesseract.image_to_data(img, lang=lang, config=tesseract_config, output_type=Output.DICT)
            text = ' '.join([w for w in data['text'] if w.strip()])
            result = {'text': text, 'data': data}
            if print_text:
                print(text)
            return result if return_data == 'dict' else {'text': text, 'data': data}
        else:
            text = pytesseract.image_to_string(img, lang=lang, config=tesseract_config)
            if print_text:
                print(text)
            return text
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None

def read_image_en(image_path: str, **kwargs) -> Optional[str]:
    return read_image(image_path, lang='eng', **kwargs)

def read_image_es(image_path: str, **kwargs) -> Optional[str]:
    return read_image(image_path, lang='spa', **kwargs)

def get_available_languages() -> List[str]:
    try:
        from pytesseract import get_languages
        return get_languages(config='')
    except Exception as e:
        print(f"No se pudieron obtener los idiomas: {e}")
        return []

def read_image_multi_lang(image_path: str, langs: List[str], **kwargs) -> Optional[str]:
    lang_str = '+'.join(langs)
    return read_image(image_path, lang=lang_str, **kwargs)

def save_text_to_file(text: str, output_path: str) -> None:
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def show_preprocessed_image(image_path: str, preprocess_opts: Optional[Dict[str, Any]] = None) -> None:
    import matplotlib.pyplot as plt
    img = preprocess_image(image_path, **(preprocess_opts or {}))
    plt.imshow(img, cmap='gray')
    plt.title('Imagen preprocesada')
    plt.axis('off')
    plt.show()

