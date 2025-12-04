# src/xai/attention_rollout.py

import torch
import torch.nn.functional as F


def attention_rollout(model, img_tensor):
    """
    Compute attention rollout for HuggingFace ViT models.
    """

    # Prepare batch
    img = img_tensor.unsqueeze(0)

    # Ensure attention outputs are returned
    model.set_attn_implementation("eager")

    # Run forward pass with attention extraction
    outputs = model(img, output_attentions=True)

    if outputs.attentions is None:
        raise RuntimeError("ViT did not return attentions. Check model.set_attn_implementation('eager').")

    attentions = outputs.attentions  # list of (batch, heads, tokens, tokens)

    # Average over heads
    attn_maps = [a.mean(dim=1) for a in attentions]  # now (batch, tokens, tokens)

    # Start with identity matrix
    joint_attn = torch.eye(attn_maps[0].size(-1)).to(img.device)

    # Multiply attention matrices layer by layer
    for attn in attn_maps:
        attn = attn[0]  # remove batch dim
        attn = attn + torch.eye(attn.size(0), device=attn.device)  # add skip connection
        attn = attn / attn.sum(dim=-1, keepdim=True)  # normalize
        joint_attn = attn @ joint_attn

    # Patch token attention
    rollout = joint_attn[0, 1:]  # remove CLS token

    # Reshape to (14×14)
    num_patches = int((rollout.size(0)) ** 0.5)
    heatmap = rollout.reshape(num_patches, num_patches).detach().cpu().numpy()

    # Upsample to 224×224
    heatmap = F.interpolate(
        torch.tensor(heatmap).unsqueeze(0).unsqueeze(0),
        size=(224, 224),
        mode="bilinear",
        align_corners=False
    ).squeeze().numpy()

    return heatmap
