# ComfyUI-fal-Image

ComfyUI Custom Node Pack für fal.ai Image-Endpoints (FLUX Dev/Pro/Schnell, Kontext inkl. Multi).

Installation
- Kopiere den Ordner `custom_nodes/ComfyUI-fal-Image/` in deinen ComfyUI `custom_nodes`-Pfad
- Installiere Abhängigkeiten: `pip install -r custom_nodes/ComfyUI-fal-Image/requirements.txt`
- Setze `FAL_KEY` als Environment-Variable (Windows PowerShell: `$env:FAL_KEY = "YOUR_KEY"`)
- Optional: `config.ini` anlegen (siehe `config.example.ini`)

Minimal-Workflow
- FAL Model Select → FAL Text2Image → Save Image

Unterstützte Endpoints und Parameter (Quelle fal.ai Doku)
- FLUX.1 [dev] Text-to-Image: `fal-ai/flux/dev` (Input u.a. `prompt`, `image_size`, `num_inference_steps`, `guidance_scale`, `num_images`, `seed`, `enable_safety_checker`) [https://fal.ai/models/fal-ai/flux/dev/api]
- FLUX.1 [schnell] Text-to-Image: `fal-ai/flux/schnell` (zusätzlich `acceleration`) [https://fal.ai/models/fal-ai/flux/schnell/api]
- FLUX.1 [pro] v1.1 / new Text-to-Image: `fal-ai/flux-pro/v1.1`, `fal-ai/flux-pro/new` (API-only `safety_tolerance`, optional `enable_safety_checker`) [https://fal.ai/models/fal-ai/flux-pro/v1.1/api] [https://fal.ai/models/fal-ai/flux-pro/new/api]
- FLUX.1 Kontext [pro] Image-to-Image: `fal-ai/flux-pro/kontext` (Input `prompt`, `image_url`, optional `guidance_scale`, `num_inference_steps`, `enable_safety_checker`, `output_format`, `aspect_ratio`) [https://fal.ai/models/fal-ai/flux-pro/kontext/api]
- FLUX.1 Kontext [dev] Image-to-Image: `fal-ai/flux-kontext/dev` [https://fal.ai/models/fal-ai/flux-kontext/dev/api]
- FLUX.1 Kontext [pro] Multi (experimentell): `fal-ai/flux-pro/kontext/multi` (Input `images: [{url, content_type}]`, `prompt`) [https://fal.ai/models/fal-ai/flux-pro/kontext/max/multi]

Hinweise
- Sicherheit: `safety_mode` (auto|enabled|disabled) wird auf die fal Felder gemappt. Bei Schemafehlern wird automatisch ohne Safety-Parameter erneut versucht.
- Async: Requests laufen über `https://queue.fal.run/`, der Node kapselt Polling bis `COMPLETED`.
- Image-IO: Response-URLs oder Base64 Data-URIs werden unterstützt und zu ComfyUI `IMAGE` konvertiert.

