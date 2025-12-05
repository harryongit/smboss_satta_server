from typing import List, Dict, Any

from app.models.result import Result
from app.core.time_utils import utc_now_iso


_results: List[Result] = []
_id_seq = 1


def _next_id() -> int:
    global _id_seq
    value = _id_seq
    _id_seq += 1
    return value


def upload_result(game_id: int, payload: Dict[str, Any]) -> Result:
    result = Result(id=_next_id(), game_id=game_id, data=payload)
    _results.append(result)
    return result


def list_results() -> List[Result]:
    return list(_results)


def list_results_for_game(game_id: int) -> List[Result]:
    return [r for r in _results if r.game_id == game_id]


def live_results() -> List[Dict[str, Any]]:
    return [
        {"game_id": r.game_id, "data": r.data, "timestamp": utc_now_iso()}
        for r in _results[-5:]
    ]

