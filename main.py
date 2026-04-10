import cv2
import config.settings as settings
from core.detector import detect_people
from core.tracker import track_people
from core.density_engine import compute_density
from core.risk_engine import compute_risk
from utils.visualizer import draw
from utils.heatmap import generate_heatmap
from utils.sound_alert import play_alert
from alerts.alert_manager import send_alert
from utils.location import get_location

print("System Starting...")

cap = cv2.VideoCapture(0)

alert_active = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect_people(frame)
    tracked = track_people(frame, detections)

    density = compute_density(tracked)

    # ✅ THIS DEFINES overcrowd
    risk_map, total_people, overcrowd, overcrowd_zones = compute_risk(density)

    frame = generate_heatmap(frame, tracked)

    # =========================
    # ALERT SYSTEM WITH LOCATION
    # =========================
    if overcrowd and not alert_active:

        lat, lng = get_location()

        if lat and lng:
            maps_link = f"https://www.google.com/maps?q={lat},{lng}"
        else:
            maps_link = "Location not available"

        # Zone info
        location_list = [f"Zone {z}" for z in overcrowd_zones]
        location_text = ", ".join(location_list)

        message = f"""
🚨 OVERCROWD ALERT 🚨
People Count: {total_people}

Unsafe Zones:
{location_text}

📍 Live Location:
{maps_link}
"""

        play_alert()
        send_alert(message)

        print("📍 Location:", maps_link)

        alert_active = True

    if not overcrowd:
        alert_active = False

    frame = draw(frame, tracked, risk_map, total_people, overcrowd, overcrowd_zones)

    cv2.imshow("Crowd Crush Management", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()