import numpy as np
import cv2
import config.settings as settings

def generate_heatmap(frame, objects):

    frame = cv2.resize(frame, (settings.FRAME_WIDTH, settings.FRAME_HEIGHT))

    # 🔥 RESET HEATMAP EVERY FRAME (NO MEMORY)
    heat = np.zeros((settings.FRAME_HEIGHT, settings.FRAME_WIDTH), dtype=np.float32)

    for (_, x, y, w, h) in objects:

        # STRICT FILTER AGAIN
        if w < 60 or h < 120:
            continue

        cx = int(x + w // 2)
        cy = int(y + h // 2)

        if 0 <= cx < settings.FRAME_WIDTH and 0 <= cy < settings.FRAME_HEIGHT:
            cv2.circle(heat, (cx, cy), 40, 1, -1)

    # Smooth
    heat = cv2.GaussianBlur(heat, (31, 31), 0)

    heat_norm = cv2.normalize(heat, None, 0, 255, cv2.NORM_MINMAX)
    heat_uint8 = heat_norm.astype(np.uint8)

    heatmap = cv2.applyColorMap(heat_uint8, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(frame, 0.75, heatmap, 0.25, 0)

    return overlay