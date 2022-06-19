from loguru import logger


class ScoreUpdater:
    def __init__(self, coach_cli):
        self.coach_cli = coach_cli
        self.old_score = dict()

    def on_upd(self, data):
        try:
            if len(data[0]) > 1:
                logger.info("Ignore snapshot because it's not event")
                return
            if len(data[0]) == 0:
                logger.info("Ignore empty because it's not event")
                return

            new_score = self.parse_score(data)

            if new_score != self.old_score:
                logger.info(f"New score {new_score}")
                self.coach_cli.send_point(new_score)
                self.old_score = new_score

        except Exception as e:
            logger.exception(f"Unexpected error {e} on data {data}")

    @staticmethod
    def parse_score(data):
        event = data[0][0]
        new_score = dict()
        for param in event["params"]:
            if param["key"] == "4":
                # points
                new_score["player1_points"], new_score["player2_points"] = param[
                    "value"
                ].split(
                    ":"
                )  # need inverse?

            elif param["key"] == "5":
                # sets
                new_score["player1_sets"], new_score["player2_sets"] = param[
                    "value"
                ].split(
                    ":"
                )  # need inverse?
        return new_score
