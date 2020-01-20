import sched
import time
from datetime import timedelta, datetime
import settings


class Cycle:
    def __init__(self, cycle_votes=None):
        self.cycle_votes = {}
        self.stats = {}
        if cycle_votes:
            self.cycle_votes = cycle_votes
            self.update_stats()
        else:
            self.reset()

    def __str__(self):
        return str(self.cycle_votes)

    def seconds_to_next_reset(self):
        utc_now = datetime.utcnow()
        utc_tomorrow = (datetime.utcnow() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return utc_tomorrow.timestamp() - utc_now.timestamp()

    def reset(self):
        self.cycle_votes = {}
        for c in settings.COLLECTIONS:
            self.cycle_votes[c] = {}
            for i in range(settings.COLLECTIONS_CYCLE_COUNT[c]):
                self.cycle_votes[c][str(i + 1)] = 0
        self.update_stats()

    def reset_loop(self):
        s = sched.scheduler(time.time, time.sleep)

        def loop():
            self.reset()
            print("Cycle reset at ", datetime.fromtimestamp(time.time()))
            next_reset_time = time.time() + self.seconds_to_next_reset()
            print("Next cycle reset scheduled at ", datetime.fromtimestamp(next_reset_time))
            s.enterabs(next_reset_time, 1, loop)

        first_reset_time = time.time() + self.seconds_to_next_reset()
        print("First cycle reset scheduled at ", datetime.fromtimestamp(first_reset_time))
        s.enterabs(first_reset_time, 1, loop)

        s.run()

    def update(self, response_tuples, user_level):
        score = 0
        for c, vote in response_tuples:
            self.cycle_votes[c][vote] += user_level
            score += settings.COLLECTION_SCORES[c]
        self.update_stats()
        return score

    def update_stats(self):
        self.stats = {
            "time_updated": datetime.now(),
            "top_choices": [],
            "top_votes": [],
            "second_top_votes": []
        }
        for c in settings.COLLECTIONS:
            max_vote = ["0", 0]
            second_max_vote = ["0", 0]
            for cycle, count in self.cycle_votes[c].items():
                if max_vote[1] < count:
                    second_max_vote = max_vote
                    max_vote = [cycle, count]
            self.stats["top_choices"].append(max_vote[0])
            self.stats["top_votes"].append(max_vote[1])
            self.stats["second_top_votes"].append(second_max_vote[1])

    def verbose(self):
        result = settings.URL_BASE + ",".join(self.stats["top_choices"]) + "\n"
        needs_help = []
        needs_verification = []

        for i, c in enumerate(settings.COLLECTIONS):
            if self.stats["top_votes"][i] == 0:
                needs_help.append(c)
            elif self.stats["top_votes"][i] - self.stats["second_top_votes"][i] < 3:
                needs_verification.append(c)
        if needs_help:
            result += ",".join(needs_help) + settings.NEED_HELP_MSG
        if needs_verification:
            result += ",".join(needs_verification) + settings.NEED_VERIFICATION_MSG
        return result


if __name__ == "__main__":
    testCycle = Cycle()
    testCycle.reset_loop()
