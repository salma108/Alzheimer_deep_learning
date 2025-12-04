# src/xai/gradcam.py

import torch
import torch.nn.functional as F

# ----------------------------------------------------------
# UNIVERSAL, SAFE, FORWARD-HOOK GRADCAM (NO BACKWARD NEEDED)
# ----------------------------------------------------------

def generate_gradcam(model, img_tensor, target_layer):
    model.eval()

    activations = {}

    # Capture output of target layer
    def hook_fn(module, inp, out):
        activations["value"] = out

    hook = target_layer.register_forward_hook(hook_fn)

    # Forward pass
    with torch.no_grad():
        output = model(img_tensor.unsqueeze(0))

    hook.remove()

    # Extract feature maps
    fmap = activations["value"].squeeze(0)  # shape: C,H,W

    # Simple CAM: mean across channels
    cam = fmap.mean(dim=0)  # (H,W)

    # Normalize
    cam = cam - cam.min()
    cam = cam / (cam.max() + 1e-8)

    return cam.cpu().numpy()
