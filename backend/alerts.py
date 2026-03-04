CRITICAL_SOUNDS = ["Gunshot", "Fire alarm", "Scream", "Explosion"]

def check_alerts(results):
    alerts = []
    for r in results:
        if r["label"] in CRITICAL_SOUNDS and r["score"] > 0.7:
            alerts.append(r)
    return alerts
