import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import cv2
from .utils import clip01

class DnCNN(nn.Module):
    def __init__(self, depth=17, n_channels=64, image_channels=3, use_bnorm=True):
        super(DnCNN, self).__init__()
        kernel_size = 3
        padding = 1
        layers = []
        layers.append(nn.Conv2d(in_channels=image_channels, out_channels=n_channels, kernel_size=kernel_size, padding=padding, bias=True))
        layers.append(nn.ReLU(inplace=True))
        for _ in range(depth-2):
            layers.append(nn.Conv2d(n_channels, n_channels, kernel_size, padding=padding, bias=False))
            if use_bnorm:
                layers.append(nn.BatchNorm2d(n_channels))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Conv2d(in_channels=n_channels, out_channels=image_channels, kernel_size=kernel_size, padding=padding, bias=False))
        self.dncnn = nn.Sequential(*layers)

    def forward(self, x):
        noise = self.dncnn(x)
        return x - noise

class DnCNNDenoiser:
    def __init__(self, weights_path=None, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DnCNN().to(self.device)
        self.ok = False
        if weights_path and os.path.exists(weights_path):
            try:
                ckpt = torch.load(weights_path, map_location=self.device)
                if isinstance(ckpt, dict) and 'state_dict' in ckpt:
                    self.model.load_state_dict(ckpt['state_dict'])
                else:
                    self.model.load_state_dict(ckpt)
                self.ok = True
                self.model.eval()
            except Exception as e:
                print("DnCNN load failed, fallback to OpenCV:", e)

    @torch.no_grad()
    def denoise(self, x):
        if self.ok:
            self.model.eval()
            x = x.to(self.device)
            y = self.model(x)
            return y.cpu()
        else:
            # Fallback: OpenCV NLM (works on CPU, non-AI but decent baseline)
            x_np = (x.squeeze(0).permute(1,2,0).cpu().numpy()*255).astype(np.uint8)
            y_np = cv2.fastNlMeansDenoisingColored(x_np, None, 5, 5, 7, 21)
            y = torch.from_numpy(y_np.astype(np.float32)/255.0).permute(2,0,1).unsqueeze(0)
            return y
