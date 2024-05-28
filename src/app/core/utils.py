from src.app.core.db.database import database


def get_user_by_email(username: str):
    for user in database:
        if user.email == username:
            return user
    return None
