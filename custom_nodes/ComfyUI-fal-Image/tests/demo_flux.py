import os
import sys
import json
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(PKG_DIR))

from fal_image.fal_client import FalClient  # type: ignore
from fal_image.schemas import coerce_image_size  # type: ignore

def run_flux_dev():
    key = os.environ.get('FAL_KEY')
    if not key:
        raise SystemExit('FAL_KEY is not set')
    client = FalClient(key)
    model_id = 'fal-ai/flux/dev'
    payload = {
        'prompt': 'photo of a friendly robot drinking coffee in a cozy cafe, cinematic lighting',
        'image_size': coerce_image_size(768, 512),
        'num_inference_steps': 24,
        'guidance_scale': 3.5,
        'num_images': 1,
        'output_format': 'png',
        'enable_safety_checker': True,
    }
    res, req_id, st = client.run_with_polling(model_id, payload, timeout_sec=60, retries=2)
    print(json.dumps({
        'request_id': req_id,
        'seed': res.get('seed'),
        'image_url': (res.get('images') or [{}])[0].get('url'),
        'status': st.get('status'),
        }, indent=2))

if __name__ == '__main__':
    run_flux_dev()
