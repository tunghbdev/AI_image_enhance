# AI Image Enhancement (Denoise + Low-Light)
This is a **ready-to-run FastAPI service** for *Denoising* and *Low-Light Enhancement* with:
- **DnCNN** (classic CNN denoiser; lightweight, fast)
- **Zero-DCE** (zero-reference low-light enhancement)

## Features
- `/enhance` endpoint: auto-detect noise level & low-light, then run the right pipeline.
- Tiling for very large images (to avoid VRAM spikes).
- Optional ONNX export & inference.
- Simple heuristics for noise/brightness detection (replace with your own later).

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (Optional) Download weights (see scripts/download_weights.sh)
# Then run API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
```

### Request
```bash
curl -X POST "http://localhost:8000/enhance?mode=auto"   -F "file=@/path/to/image.jpg"   --output out.png
```

## Weights
- **DnCNN**: place file at `weights/dncnn_color.pth` (or change path in `.env` or config).
- **Zero-DCE**: place file at `weights/zerodce.pth`.

**You can start without weights**: the service will fallback to *OpenCV fastNlMeansDenoisingColored* for denoise and a simple Retinex-like curve for low-light, so you can test the pipeline immediately. But for best results, add pretrained weights.

## Notes
- This repo is meant as a strong *starting point*. Swap DnCNN → **NAFNet/Restormer**, and Zero-DCE → **Zero-DCE++** when ready.
- Export models to ONNX/TensorRT for production latency.
