import io
import base64
import numpy as np
import requests
from PIL import Image

def _to_numpy(img: Image.Image):
    arr = np.array(img.convert('RGB')).astype(np.float32) / 255.0
    return arr

def _from_data_uri(data_uri: str):
    if data_uri.startswith('data:'):
        header, b64 = data_uri.split(',', 1)
        data = base64.b64decode(b64)
        return Image.open(io.BytesIO(data))
    resp = requests.get(data_uri, timeout=30)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content))

def image_from_response(resp: dict):
    img_url = None
    if 'images' in resp and resp['images']:
        item = resp['images'][0]
        if 'url' in item and item['url']:
            img_url = item['url']
            pil = _from_data_uri(img_url)
            return _to_numpy(pil), img_url
        if 'data' in item and item['data']:
            pil = _from_data_uri(item['data'])
            return _to_numpy(pil), None
        if 'data_uri' in item and item['data_uri']:
            pil = _from_data_uri(item['data_uri'])
            return _to_numpy(pil), None
    if 'image' in resp and resp['image']:
        pil = _from_data_uri(resp['image'])
        return _to_numpy(pil), None
    raise RuntimeError('No image found in response')

def image_to_data_uri(image_np: np.ndarray, fmt: str = 'PNG'):
    pil = Image.fromarray((np.clip(image_np, 0.0, 1.0) * 255).astype(np.uint8))
    buf = io.BytesIO()
    pil.save(buf, format=fmt)
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    mime = 'image/png' if fmt.upper() == 'PNG' else 'image/jpeg'
    return f'data:{mime};base64,{b64}'

