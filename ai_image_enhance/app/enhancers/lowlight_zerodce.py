import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from .utils import clip01

# Minimal Zero-DCE network (8 curve estimation layers)
class EnhanceNet(nn.Module):
    def __init__(self, channels=32):
        super().__init__()
        self.e1 = nn.Conv2d(3, channels, 3, 1, 1)
        self.e2 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.e3 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.e4 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.e5 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.e6 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.e7 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.e8 = nn.Conv2d(channels, 24, 3, 1, 1)  # 8 curve maps * 3 channels

        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x1 = self.relu(self.e1(x))
        x2 = self.relu(self.e2(x1))
        x3 = self.relu(self.e3(x2))
        x4 = self.relu(self.e4(x3))
        x5 = self.relu(self.e5(x4))
        x6 = self.relu(self.e6(x5))
        x7 = self.relu(self.e7(x6))
        x8 = self.e8(x7)
        return x8

def curve_enhance(x, r):
    # x: [B,3,H,W], r: [B,24,H,W] -> apply 8 iterative curves
    r = torch.split(r, 3, dim=1)  # 8 tensors [B,3,H,W]
    x_enh = x
    for i in range(8):
        x_enh = x_enh + r[i] * (x_enh * (1 - x_enh))
    return x_enh

class ZeroDCEEnhancer:
    def __init__(self, weights_path=None, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.net = EnhanceNet().to(self.device)
        self.ok = False
        if weights_path and os.path.exists(weights_path):
            try:
                ckpt = torch.load(weights_path, map_location=self.device)
                if isinstance(ckpt, dict) and 'state_dict' in ckpt:
                    self.net.load_state_dict(ckpt['state_dict'])
                else:
                    self.net.load_state_dict(ckpt)
                self.ok = True
                self.net.eval()
            except Exception as e:
                print("Zero-DCE load failed, fallback to simple curve:", e)

    @torch.no_grad()
    def enhance(self, x):
        if self.ok:
            x = x.to(self.device)
            r = self.net(x)
            y = curve_enhance(x, r).cpu()
            return y
        else:
            # Simple fallback gamma/retinex-like curve
            y = torch.clamp(x, 0, 1)
            gamma = 0.7  # brighten
            y = y ** gamma
            return y
