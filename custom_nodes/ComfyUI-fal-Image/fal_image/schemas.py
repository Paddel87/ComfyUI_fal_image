# Endpunktliste und Parameter basierend auf fal.ai Doku (siehe README Links)

IMAGE_SIZE_ENUMS = {
    'square_hd', 'square', 'portrait_4_3', 'portrait_16_9', 'landscape_4_3', 'landscape_16_9'
}

MODEL_MAP = {
    'flux-dev': 'fal-ai/flux/dev',
    'flux-schnell': 'fal-ai/flux/schnell',
    'flux-pro-v1.1': 'fal-ai/flux-pro/v1.1',
    'flux-pro-new': 'fal-ai/flux-pro/new',
    'flux-kontext-pro': 'fal-ai/flux-pro/kontext',
    'flux-kontext-pro-multi': 'fal-ai/flux-pro/kontext/multi',
    'flux-kontext-dev': 'fal-ai/flux-kontext/dev',
    'flux-schnell-redux': 'fal-ai/flux/schnell/redux',
}

TEXT2IMAGE_PAYLOAD_KEYS = {
    'fal-ai/flux/dev': {
        'prompt', 'image_size', 'num_inference_steps', 'seed', 'guidance_scale', 'num_images', 'sync_mode', 'output_format', 'enable_safety_checker', 'acceleration'
    },
    'fal-ai/flux/schnell': {
        'prompt', 'image_size', 'num_inference_steps', 'seed', 'guidance_scale', 'num_images', 'sync_mode', 'output_format', 'enable_safety_checker', 'acceleration'
    },
    'fal-ai/flux-pro/v1.1': {
        'prompt', 'image_size', 'seed', 'num_images', 'sync_mode', 'output_format', 'enable_safety_checker', 'safety_tolerance', 'enhance_prompt'
    },
    'fal-ai/flux-pro/new': {
        'prompt', 'image_size', 'num_inference_steps', 'seed', 'guidance_scale', 'num_images', 'sync_mode', 'output_format', 'enable_safety_checker', 'safety_tolerance', 'enhance_prompt'
    },
}

IMAGE2IMAGE_PAYLOAD_KEYS = {
    'fal-ai/flux-pro/kontext': {
        'prompt', 'image_url', 'seed', 'guidance_scale', 'num_inference_steps', 'sync_mode', 'num_images', 'output_format', 'enable_safety_checker', 'safety_tolerance', 'aspect_ratio', 'enhance_prompt'
    },
    'fal-ai/flux-kontext/dev': {
        'prompt', 'image_url', 'seed', 'guidance_scale', 'num_inference_steps', 'sync_mode', 'num_images'
    },
    'fal-ai/flux-pro/kontext/multi': {
        'prompt', 'images', 'seed', 'guidance_scale', 'num_inference_steps', 'sync_mode', 'num_images', 'output_format', 'enable_safety_checker', 'safety_tolerance'
    },
    'fal-ai/flux/schnell/redux': {
        'image_url', 'num_inference_steps', 'image_size', 'seed', 'sync_mode', 'num_images', 'output_format', 'enable_safety_checker', 'acceleration'
    },
}

def coerce_image_size(width: int, height: int):
    return {'width': int(width), 'height': int(height)}

def map_safety(mode: str, model_id: str):
    mode = (mode or 'auto').lower()
    params = {}
    applied = 'auto'
    if mode == 'enabled':
        params['enable_safety_checker'] = True
        applied = 'enabled'
    elif mode == 'disabled':
        params['enable_safety_checker'] = False
        applied = 'disabled'
    else:
        applied = 'auto'
    if 'flux-pro' in model_id:
        pass
    return params, applied

