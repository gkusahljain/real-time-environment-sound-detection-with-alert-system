from twilio.rest import Client
from datetime import datetime
from config import CRITICAL_SOUNDS

# Twilio config
ACCOUNT_SID = "AC2107daf468717391e8e3a9003ace74a3"
AUTH_TOKEN = "9e0bf1129ba70d1f8c0cdb01ffaa86d6"
FROM_NUMBER = "+13519007501"
TO_NUMBER = "+917338065007"   # emergency contact

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def generate_alerts(results):
    alerts = []

    for item in results:
        label = item["label"]
        score = item["score"]

        if label in CRITICAL_SOUNDS and score >= CRITICAL_SOUNDS[label]:
            msg = f"🚨 ALERT!\n{label}\nConfidence: {round(score*100,1)}%\nTime: {datetime.now()}"

            # Send SMS
            client.messages.create(
                body=msg,
                from_=FROM_NUMBER,
                to=TO_NUMBER
            )

            alerts.append({
                "type": label,
                "confidence": score,
                "message": msg
            })

    return alerts
