import io
import pytest
import requests
from PIL import Image

BASE_URL = "http://localhost:8000"

def _img_buf(w=50, h=50, color=(128,128,128)):
    """Tạo 1 ảnh nhỏ RGB để test"""
    img = Image.new("RGB", (w, h), color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_analyze_endpoint():
    files = {"file": ("test.jpg", _img_buf(), "image/jpeg")}
    r = requests.post(f"{BASE_URL}/analyze", files=files)
    assert r.status_code == 200
    data = r.json()
    for k in ("brightness", "darkness_ratio", "noise_score"):
        assert k in data

@pytest.mark.parametrize("mode", ["auto", "denoise", "lowlight"])
def test_enhance_endpoint(mode):
    files = {"file": ("test.jpg", _img_buf(), "image/jpeg")}
    r = requests.post(f"{BASE_URL}/enhance?mode={mode}", files=files)
    assert r.status_code == 200
    assert r.headers.get("content-type") in ("image/png", "application/octet-stream")
