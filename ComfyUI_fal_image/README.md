# ComfyUI-fal-Image

ComfyUI Custom Node Pack für fal.ai Image-Endpoints (FLUX Dev/Pro/Schnell, Kontext inkl. Multi).

Installation
- Kopiere den Ordner `ComfyUI_fal_image/` in den `custom_nodes`-Ordner deiner ComfyUI-Installation
- Installiere Abhängigkeiten: `pip install -r ComfyUI_fal_image/requirements.txt`
- Setze `FAL_KEY` als Environment-Variable (Windows PowerShell: `$env:FAL_KEY = "YOUR_KEY"`)
- Optional: `ComfyUI_fal_image/config.ini` anlegen (siehe `config.example.ini`)

Minimal-Workflow
- FAL Model Select → FAL Text2Image → Save Image
