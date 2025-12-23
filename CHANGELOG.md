# Changelog

## v0.1.0 – 2025-12-23
Initial public release – fully tested & verified.

### ✨ Added
- **Full FLUX model support**: Dev, Pro v1.1, Pro New, Schnell, Kontext variants  
- **Queue polling client**: non-blocking requests with configurable timeout (10-600 s) & retry logic  
- **Safety controls**: per-request enable/disable + tolerance (0-6) with automatic fallback  
- **Context continuity**: store & reuse request-ids for multi-step Kontext workflows  
- **Native ComfyUI I/O**: transparent URL ↔ numpy array conversion (HWC, 0-1 range)  
- **Configuration**: ENV variable or INI file for API key & defaults  
- **Comprehensive logging**: model_id, seed, safety_applied plus request metadata  
- **Minimal workflow**: ready-made JSON for Kontext → Variants → Img2Img pipeline  

### ✅ Verified
- Context-ID reuse – maintains identity across runs  
- Img2Img low-strength (0.2-0.4) – preserves core features  
- Safety configuration – server-side enforcement handled gracefully  
- Logging – model_id, seed, safety_applied tracked per request  

### 📦 Assets
- `workflows/minimal_kontext_img2img.json` – drag-and-drop ComfyUI workflow  
- `tests/demo_flux.py` – standalone API test script
- `example_workflows/` – ready-to-use workflow templates
- `LICENSE` – MIT license