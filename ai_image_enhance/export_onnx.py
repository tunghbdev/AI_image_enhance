# Export models to ONNX (optional)
import os, torch
from app.enhancers.denoise_dncnn import DnCNN
from app.enhancers.lowlight_zerodce import EnhanceNet

os.makedirs("onnx", exist_ok=True)

# DnCNN
dncnn = DnCNN().eval()
x = torch.randn(1,3,256,256)
torch.onnx.export(dncnn, x, "onnx/dncnn.onnx", opset_version=17, input_names=["input"], output_names=["output"], dynamic_axes={"input":{2:"h",3:"w"},"output":{2:"h",3:"w"}})
print("Saved onnx/dncnn.onnx")

# Zero-DCE
z = EnhanceNet().eval()
torch.onnx.export(z, x, "onnx/zerodce.onnx", opset_version=17, input_names=["input"], output_names=["rmaps"], dynamic_axes={"input":{2:"h",3:"w"},"rmaps":{2:"h",3:"w"}})
print("Saved onnx/zerodce.onnx")
