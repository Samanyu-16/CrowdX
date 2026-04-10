import cv2
import config.settings as settings

def draw(frame, objects, risk_map, total_people, overcrowd, overcrowd_zones):

    # =========================
    # Grid size
    # =========================
    zone_w = settings.FRAME_WIDTH // settings.COLS
    zone_h = settings.FRAME_HEIGHT // settings.ROWS

    # =========================
    # Draw bounding boxes
    # =========================
    for (track_id, x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{track_id}", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # =========================
    # Draw grid lines
    # =========================
    for i in range(1, settings.COLS):
        cv2.line(frame, (i * zone_w, 0), (i * zone_w, settings.FRAME_HEIGHT), (255, 0, 0), 2)

    for j in range(1, settings.ROWS):
        cv2.line(frame, (0, j * zone_h), (settings.FRAME_WIDTH, j * zone_h), (255, 0, 0), 2)

    # =========================
    # Draw zone SAFE / UNSAFE
    # =========================
    for zone, (count, risk) in risk_map.items():

        row, col = zone

        x = col * zone_w + 10
        y = row * zone_h + 30

        # 🔥 YOUR SAFE / UNSAFE LOGIC
        if zone in overcrowd_zones:
            text = f"UNSAFE ({zone})"
            color = (0, 0, 255)  # Red
        else:
            text = f"SAFE ({zone})"
            color = (0, 255, 0)  # Green

        cv2.putText(frame, text, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # =========================
    # Top panel UI
    # =========================
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (settings.FRAME_WIDTH, 90), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

    # People count
    cv2.putText(frame, f"People: {total_people}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Global SAFE / UNSAFE
    if overcrowd:
        cv2.putText(frame, "UNSAFE ZONE 🚨", (300, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        cv2.putText(frame, "SAFE ZONE ✅", (300, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # =========================
    # Highlight overcrowd zones
    # =========================
    for zone in overcrowd_zones:
        row, col = zone

        x1 = col * zone_w
        y1 = row * zone_h
        x2 = x1 + zone_w
        y2 = y1 + zone_h

        # Red transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)
        frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)

    return frame