from typing import Dict, List

from app.services import user_service, result_service, game_service


def register_admin(username: str, email: str, password: str):
    return user_service.create_user(username, email, password, role="admin")


def login_admin(username: str, password: str):
    return user_service.authenticate(username, password)


def dashboard_stats() -> Dict[str, int]:
    return {
        "users": len(user_service.list_users()),
        "games": len(game_service.list_games()),
        "results": len(result_service.list_results()),
    }

