from loguru import logger

from models import Event


class ScoreUpdater:
    def __init__(self, coach_cli):
        self.coach_cli = coach_cli
        self.old_score_and_first_match_serve = dict()

    async def on_upd(self, data):
        try:
            logger.info(data)
            score_and_first_match_serve = self.parse_score_and_first_match_serve(data)

            if score_and_first_match_serve != self.old_score_and_first_match_serve:
                logger.info(
                    f"New score_and_first_match_serve={score_and_first_match_serve}"
                )

                await self.coach_cli.send_point(score_and_first_match_serve)
                self.old_score_and_first_match_serve = score_and_first_match_serve

        except Exception as e:
            logger.exception(f"Unexpected error {e} on data {data}")

    @staticmethod
    def parse_score_and_first_match_serve(msg):
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

        score_and_first_match_serve = dict()
        if reverse_score:
            (
                score_and_first_match_serve["player2_points"],
                score_and_first_match_serve["player1_points"],
            ) = _set.score.as_tuple()
            (
                score_and_first_match_serve["player2_sets"],
                score_and_first_match_serve["player1_sets"],
            ) = _match.score.as_tuple()
        else:
            (
                score_and_first_match_serve["player1_points"],
                score_and_first_match_serve["player2_points"],
            ) = _set.score.as_tuple()
            (
                score_and_first_match_serve["player1_sets"],
                score_and_first_match_serve["player2_sets"],
            ) = _match.score.as_tuple()

        if _set.score.as_tuple() == (0, 0) and _match.score.as_tuple() == (0, 0):
            left_player_first_serve = ScoreUpdater.parse_first_serve(
                _match, _set, reverse_score
            )
            if left_player_first_serve:
                score_and_first_match_serve["side"] = "left"
                score_and_first_match_serve["team"] = 1
            else:
                score_and_first_match_serve["side"] = "right"
                score_and_first_match_serve["team"] = 2
        return score_and_first_match_serve

    @staticmethod
    def parse_first_serve(_match, _set, reverse_score):
        beter_first_player_is_active = _set.active_player_id == _match.player1.id
        logger.info(
            f"beter_first_player_is_active={beter_first_player_is_active}, reverse_score={reverse_score}"
        )
        left_player_first_serve = (
            beter_first_player_is_active is True
            and reverse_score is False
            or beter_first_player_is_active is False
            and reverse_score is True
        )
        logger.info(f"left_player_first_serve={left_player_first_serve}")
        return left_player_first_serve
