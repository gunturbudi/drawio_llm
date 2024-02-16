
from flask_login import current_user
from models import db, LogAction
from datetime import datetime


def save_action(action):
    username = current_user.username
    timestamp = datetime.now()
    new_action = LogAction(username=username, action=action, timestamp=timestamp)
    db.session.add(new_action)
    db.session.commit()
    