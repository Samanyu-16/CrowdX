def compute_risk(density):
    risk_map = {}
    total_people = 0

    overcrowd_zones = []

    for zone, count in density.items():
        total_people += count

        if count < 3:
            risk = "LOW"
        elif count < 6:
            risk = "MEDIUM"
        elif count < 10:
            risk = "HIGH"
        else:
            risk = "CRITICAL"

        # 🔥 Detect overcrowd zone
        if count >= 4:
            overcrowd_zones.append(zone)

        risk_map[zone] = (count, risk)

    overcrowd = total_people >= 4

    return risk_map, total_people, overcrowd, overcrowd_zones