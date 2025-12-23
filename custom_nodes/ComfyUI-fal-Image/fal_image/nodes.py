import numpy as np
from .config import get_api_key, get_timeout_default, get_retries_default
from .fal_client import FalClient
from .io_image import image_from_response, image_to_data_uri
from . import schemas

class FalModelSelectImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'model': (list(schemas.MODEL_MAP.keys()), )
            }
        }
    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ('model_id',)
    FUNCTION = 'select'
    CATEGORY = 'fal.ai/Image'
    def select(self, model: str):
        mid = schemas.MODEL_MAP.get(model)
        return (mid,)

class FalText2Image:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'model_id': ('STRING',),
                'prompt': ('STRING',),
                'width': ('INT', {'default': 1024, 'min': 64, 'max': 2048}),
                'height': ('INT', {'default': 1024, 'min': 64, 'max': 2048}),
                'num_images': ('INT', {'default': 1, 'min': 1, 'max': 4}),
                'seed': ('INT', {'default': 0, 'min': 0}),
                'steps': ('INT', {'default': 28, 'min': 1, 'max': 100}),
                'guidance': ('FLOAT', {'default': 3.5, 'min': 0.0, 'max': 20.0}),
                'safety_mode': (['auto', 'enabled', 'disabled'], ),
                'timeout_sec': ('INT', {'default': get_timeout_default(), 'min': 10, 'max': 600}),
                'retries': ('INT', {'default': get_retries_default(), 'min': 0, 'max': 5}),
            },
            'optional': {
                'context_id': ('STRING',),
            }
        }
    RETURN_TYPES = ('IMAGE', 'STRING', 'STRING', 'STRING')
    RETURN_NAMES = ('image', 'image_url', 'context_id_out', 'safety_applied')
    FUNCTION = 'run'
    CATEGORY = 'fal.ai/Image'
    def run(self, model_id: str, prompt: str, width: int, height: int, num_images: int, seed: int, steps: int, guidance: float, safety_mode: str, timeout_sec: int, retries: int, context_id: str = None):
        key = get_api_key()
        if not key:
            raise RuntimeError('FAL_KEY fehlt. Bitte Environment setzen oder config.ini verwenden.')
        payload = {'prompt': prompt}
        payload['image_size'] = schemas.coerce_image_size(width, height)
        if seed:
            payload['seed'] = int(seed)
        payload['num_images'] = int(num_images)
        payload['guidance_scale'] = float(guidance)
        payload['num_inference_steps'] = int(steps)
        payload['output_format'] = 'png'
        sparams, applied = schemas.map_safety(safety_mode, model_id)
        payload.update(sparams)
        allow = schemas.TEXT2IMAGE_PAYLOAD_KEYS.get(model_id, set())
        payload = {k: v for k, v in payload.items() if k in allow or not allow}
        client = FalClient(key)
        try:
            res, req_id, st = client.run_with_polling(model_id, payload, timeout_sec, retries)
            arr, img_url = image_from_response(res)
            ctx = req_id
            print(f'[fal.ai] model_id={model_id} seed={res.get("seed")} safety_applied={applied} image_url={img_url or ""}')
            return (arr, img_url or '', ctx or '', applied)
        except Exception as e:
            if 'enable_safety_checker' in payload:
                p2 = dict(payload)
                p2.pop('enable_safety_checker', None)
                applied2 = 'forced_by_model'
                res, req_id, st = client.run_with_polling(model_id, p2, timeout_sec, retries)
                arr, img_url = image_from_response(res)
                print(f'[fal.ai] model_id={model_id} seed={res.get("seed")} safety_applied={applied2} image_url={img_url or ""}')
                return (arr, img_url or '', req_id or '', applied2)
            raise e

class FalImage2Image:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'model_id': ('STRING',),
                'prompt': ('STRING',),
                'init_image': ('IMAGE',),
                'strength': ('FLOAT', {'default': 0.75, 'min': 0.0, 'max': 1.0}),
                'seed': ('INT', {'default': 0, 'min': 0}),
                'steps': ('INT', {'default': 30, 'min': 1, 'max': 100}),
                'guidance': ('FLOAT', {'default': 3.5, 'min': 0.0, 'max': 20.0}),
                'safety_mode': (['auto', 'enabled', 'disabled'], ),
                'timeout_sec': ('INT', {'default': get_timeout_default(), 'min': 10, 'max': 600}),
                'retries': ('INT', {'default': get_retries_default(), 'min': 0, 'max': 5}),
            },
            'optional': {
                'context_id': ('STRING',),
            }
        }
    RETURN_TYPES = ('IMAGE', 'STRING', 'STRING')
    RETURN_NAMES = ('image', 'image_url', 'safety_applied')
    FUNCTION = 'run'
    CATEGORY = 'fal.ai/Image'
    def run(self, model_id: str, prompt: str, init_image: np.ndarray, strength: float, seed: int, steps: int, guidance: float, safety_mode: str, timeout_sec: int, retries: int, context_id: str = None):
        key = get_api_key()
        if not key:
            raise RuntimeError('FAL_KEY fehlt. Bitte Environment setzen oder config.ini verwenden.')
        data_uri = image_to_data_uri(init_image, fmt='PNG')
        payload = {'prompt': prompt, 'image_url': data_uri}
        if seed:
            payload['seed'] = int(seed)
        payload['guidance_scale'] = float(guidance)
        payload['num_inference_steps'] = int(steps)
        payload['output_format'] = 'png'
        sparams, applied = schemas.map_safety(safety_mode, model_id)
        payload.update(sparams)
        if strength is not None:
            payload['strength'] = float(strength)
        allow = schemas.IMAGE2IMAGE_PAYLOAD_KEYS.get(model_id, set())
        payload = {k: v for k, v in payload.items() if k in allow or not allow}
        client = FalClient(key)
        try:
            res, req_id, st = client.run_with_polling(model_id, payload, timeout_sec, retries)
            arr, img_url = image_from_response(res)
            print(f'[fal.ai] model_id={model_id} seed={res.get("seed")} safety_applied={applied} image_url={img_url or ""}')
            return (arr, img_url or '', applied)
        except Exception as e:
            if 'enable_safety_checker' in payload:
                p2 = dict(payload)
                p2.pop('enable_safety_checker', None)
                applied2 = 'forced_by_model'
                res, req_id, st = client.run_with_polling(model_id, p2, timeout_sec, retries)
                arr, img_url = image_from_response(res)
                print(f'[fal.ai] model_id={model_id} seed={res.get("seed")} safety_applied={applied2} image_url={img_url or ""}')
                return (arr, img_url or '', applied2)
            raise e

class FalContextStore:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'context_id_in': ('STRING',),
            }
        }
    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ('context_id',)
    FUNCTION = 'store'
    CATEGORY = 'fal.ai/Image'
    def store(self, context_id_in: str):
        return (context_id_in,)

NODE_CLASS_MAPPINGS = {
    'FALModelSelectImage': FalModelSelectImage,
    'FALText2Image': FalText2Image,
    'FALImage2Image': FalImage2Image,
    'FALContextStore': FalContextStore,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    'FALModelSelectImage': 'FAL Model Select (Image)',
    'FALText2Image': 'FAL Text2Image',
    'FALImage2Image': 'FAL Image2Image',
    'FALContextStore': 'FAL Context Store',
}

