from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel
import io, os
from PIL import Image
import numpy as np
from dotenv import load_dotenv

from .enhancers.autodetect import analyze_image
from .enhancers.denoise_dncnn import DnCNNDenoiser
from .enhancers.lowlight_zerodce import ZeroDCEEnhancer
from .enhancers.utils import to_tensor_image, from_tensor_image, clip01

load_dotenv()

app = FastAPI(title="AI Image Enhancement (Denoise + Low-Light)")

# Instantiate enhancers (lazy-load weights if present)
dncnn = DnCNNDenoiser(weights_path=os.getenv("DNCCN_WEIGHTS", "weights/dncnn_color.pth"))
zerodce = ZeroDCEEnhancer(weights_path=os.getenv("ZERODCE_WEIGHTS", "weights/zerodce.pth"))

class Analysis(BaseModel):
    brightness: float
    darkness_ratio: float
    noise_score: float

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/analyze", response_model=Analysis)
async def analyze(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    a = analyze_image(img)
    return Analysis(**a)

@app.post("/enhance")
async def enhance(file: UploadFile = File(...), mode: str = Query("auto", enum=["auto", "denoise", "lowlight"])):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    arr = np.array(img)

    metrics = analyze_image(img)

    # Decide pipeline
    run_denoise = (mode == "denoise") or (mode == "auto" and metrics["noise_score"] > 0.2)
    run_lowlight = (mode == "lowlight") or (mode == "auto" and (metrics["brightness"] < 0.35 or metrics["darkness_ratio"] > 0.4))

    x = to_tensor_image(arr)

    if run_lowlight:
        x = zerodce.enhance(x)

    if run_denoise:
        x = dncnn.denoise(x)

    y = from_tensor_image(clip01(x))
    out = Image.fromarray(y)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")
