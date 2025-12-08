from flask import Blueprint, request, jsonify
from pywebpush import webpush, WebPushException
import json
import os

notifications_bp = Blueprint('notifications', __name__)

VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")

@notifications_bp.route("/subscribe", methods=["POST"])
def subscribe():
    subscription = request.json.get("subscription")
    user_id = request.json.get("user_id")

    # sauvegarde dans MongoDB
    db.users.update_one(
        {"_id": user_id},
        {"$set": {"push_subscription": subscription}}
    )

    return jsonify({"ok": True})
