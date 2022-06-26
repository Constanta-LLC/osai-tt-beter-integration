from loguru import logger

from models import Event


class ScoreUpdater:
    def __init__(self, coach_cli):
        self.coach_cli = coach_cli
        self.old_score = dict()

    async def on_upd(self, data):
        try:
            logger.info(data)
            new_score = self.parse_score(data)

            if new_score != self.old_score:
                logger.info(f"New score {new_score}")

                await self.coach_cli.send_point(new_score)
                self.old_score = new_score

        except Exception as e:
            logger.exception(f"Unexpected error {e} on data {data}")

    @staticmethod
    def parse_score(msg):
        event = Event.parse_raw(msg)
        _set = event.data.set
        _match = event.data.match
        players_sides_need_swap_by_rules = (
            _set.number in {2, 4}
            or _set.number == 5
            and max(_set.score.as_tuple()) >= 5
        )

        # in beter playground player1 staying right in frame by default that we need reverse scores
        # but players can inverse position on start match
        if players_sides_need_swap_by_rules == bool(_set.reverse_position):
            reverse_score = True
        else:
            reverse_score = False

        score = dict()
        if reverse_score:
            score["player2_points"], score["player1_points"] = _set.score.as_tuple()
            score["player2_sets"], score["player1_sets"] = _match.score.as_tuple()
        else:
            score["player1_points"], score["player2_points"] = _set.score.as_tuple()
            score["player1_sets"], score["player2_sets"] = _match.score.as_tuple()
        return score
