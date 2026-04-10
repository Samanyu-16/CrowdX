from deep_sort_realtime.deepsort_tracker import DeepSort

tracker = DeepSort(max_age=10)

def track_people(frame, detections):
    tracks = tracker.update_tracks(detections, frame=frame)

    objects = []

    for track in tracks:
        if not track.is_confirmed():
            continue

        # 🔥 REMOVE OLD / GHOST TRACKS
        if track.time_since_update > 0:
            continue

        x1, y1, x2, y2 = map(int, track.to_ltrb())
        w = x2 - x1
        h = y2 - y1

        # 🔥 STRICT SIZE FILTER
        if w < 60 or h < 120:
            continue

        track_id = track.track_id
        objects.append((track_id, x1, y1, w, h))

    return objects