import numpy as np
from PIL import Image
import cv2

def analyze_image(img: Image.Image):
    arr = np.array(img).astype(np.float32) / 255.0
    gray = cv2.cvtColor((arr*255).astype('uint8'), cv2.COLOR_RGB2GRAY).astype(np.float32)/255.0

    # brightness: mean luminance
    brightness = float(gray.mean())

    # darkness ratio: % pixels below 0.2
    darkness_ratio = float((gray < 0.2).mean())

    # noise score: simple high-frequency energy via Laplacian variance minus structure
    lap = cv2.Laplacian((gray*255).astype('uint8'), cv2.CV_16S, ksize=3)
    lap = np.abs(lap).astype(np.float32)
    hf_energy = float(lap.var())

    # normalize to 0..1 (heuristic)
    noise_score = float(min(1.0, hf_energy / 2000.0))

    return {
        "brightness": brightness,
        "darkness_ratio": darkness_ratio,
        "noise_score": noise_score
    }
