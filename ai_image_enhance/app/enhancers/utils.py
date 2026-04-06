import numpy as np
import torch

def to_tensor_image(arr: np.ndarray) -> torch.Tensor:
    # [H,W,3] uint8 -> [1,3,H,W] float32 0..1
    x = torch.from_numpy(arr).float() / 255.0
    x = x.permute(2,0,1).unsqueeze(0).contiguous()
    return x

def from_tensor_image(x: torch.Tensor) -> np.ndarray:
    # [1,3,H,W] -> [H,W,3] uint8
    x = x.squeeze(0).clamp(0,1).permute(1,2,0).cpu().numpy()
    x = (x * 255.0 + 0.5).astype(np.uint8)
    return x

def clip01(x: torch.Tensor) -> torch.Tensor:
    return torch.clamp(x, 0.0, 1.0)
