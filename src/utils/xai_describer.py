# src/utils/xai_describer.py

import numpy as np

def describe_xai(heatmap: np.ndarray) -> str:
    h, w = heatmap.shape
    cy, cx = np.unravel_index(np.argmax(heatmap), heatmap.shape)

    if cx < w/3:
        lat = "hémisphère gauche"
    elif cx > 2*w/3:
        lat = "hémisphère droit"
    else:
        lat = "zone centrale"

    if cy < h/2:
        vert = "régions supérieures (pariétales/frontales)"
    else:
        vert = "régions inférieures (temporales/hippocampiques)"

    return f"La zone la plus activée du XAI se situe dans {lat}, correspondant aux {vert}."
