import sched
import time
from datetime import timedelta, datetime
import os

from cycle import Cycle
import settings


class RepoUpdater:
    def __init__(self, cycle: Cycle, update_cmd_file="update_script"):
        self.update_cmd_file = update_cmd_file
        self.last_top_choices = None
        self.cycle = cycle

    def seconds_to_next_update(self):
        utc_now = datetime.utcnow()
        utc_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        now_delta = utc_now - utc_today
        for event in settings.REPO_UPDATE_EVENTS:
            if event + utc_today > utc_now:
                return (event - now_delta).total_seconds()
        return None

    def update(self):
        if self.cycle_changed():
            print("Cycle changed, Updating")
            self.write_cycle()
            with open(self.update_cmd_file) as fd:
                cmd = fd.read()
            cmd = cmd.format(datetime.utcnow())
            return os.system(cmd)

    def write_cycle(self):
        pass
        #TODO: write cycle data in correct file

    def cycle_changed(self):
        if str(self.cycle.stats["top_choices"]) != self.last_top_choices:
            self.last_top_choices = str(self.cycle.stats["top_choices"])
            return True
        return True

    def update_loop(self):
        s = sched.scheduler(time.time, time.sleep)

        def loop():
            self.update()
            print("Repo updated at ", datetime.fromtimestamp(time.time()))
            next_update_time = time.time() + self.seconds_to_next_update()
            print("Next repo update scheduled at ", datetime.fromtimestamp(next_update_time))
            s.enterabs(next_update_time, 1, loop)

        first_update_time = time.time() + self.seconds_to_next_update()
        print("Next repo update scheduled at ", datetime.fromtimestamp(first_update_time))
        s.enterabs(first_update_time, 1, loop)

        s.run()


if __name__ == "__main__":
    testUpdate = RepoUpdater(Cycle())
    testUpdate.update_loop()

