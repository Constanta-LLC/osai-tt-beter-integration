class ScoreUpdater:
    def __init__(self):
        self.old_score = dict()

    def on_upd(self, data):
        try:
            if len(data[0]) > 1:
                print("Ignore snapshot because it's not event", data)
                return
            if len(data[0]) == 0:
                print("Ignore empty because it's not event", data)
                return
            event = data[0][0]
            new_score = dict()
            for param in event["params"]:
                if param["key"] == "4":
                    # points
                    first, second = param["value"].split(":")  # need inverse?
                    new_score["points"] = {"first": first, "second": second}
                elif param["key"] == "5":
                    # sets
                    first, second = param["value"].split(":")  # need inverse?
                    new_score["sets"] = {"first": first, "second": second}

            if new_score != self.old_score:
                print("New score", new_score)
                self.old_score = new_score

        except Exception as e:
            print(e, data)
