from utils.zone_mapper import get_zone

def compute_density(objects):
    zones = {}

    for (track_id, x, y, w, h) in objects:
        cx = x + w//2
        cy = y + h//2

        zone = get_zone(cx, cy)

        if zone not in zones:
            zones[zone] = 0

        zones[zone] += 1

    return zones