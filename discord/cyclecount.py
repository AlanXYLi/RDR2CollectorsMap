COLLECTIONS = [
    "flower",
    "cards",
    "jewelry",
    "bottle",
    "egg",
    "arrow",
    "loom",
    "coin",
    "random"
]

CYCLE_COUNT = {
    "flower":6,
    "cards":6,
    "jewelry":6,
    "bottle":6,
    "egg":6,
    "arrow":6,
    "loom":6,
    "coin":6,
    "random":7
}

URL_BASE = "https://jeanropke.github.io/RDR2CollectorsMap/?cycles="

class Cycle:
    def __init__(self):
        self.currentCycle = {}
        self.stats={}
        for c in COLLECTIONS:
            self.currentCycle[c] = {}
            for i in range(CYCLE_COUNT[c]):
                self.currentCycle[c][str(i + 1)] = 0

    def __str__(self):
        self.check_stats()
        return str(self.stats["top_choices"])+str(self.stats["top_votes"])+str(self.stats["second_top_votes"])

    def update(self, response_map, user_level):
        for c, vote in response_map.items():
            self.currentCycle[c][vote] += user_level

    def check_stats(self):
        self.stats = {
            "top_choices": [],
            "top_votes": [],
            "second_top_votes": []
        }
        for c in COLLECTIONS:
            max_vote = ["0", 0]
            second_max_vote = ["0", 0]
            for cycle, count in self.currentCycle[c].items():
                if max_vote[1] < count:
                    second_max_vote = max_vote
                    max_vote = [cycle, count]
            self.stats["top_choices"].append(max_vote[0])
            self.stats["top_votes"].append(max_vote[1])
            self.stats["second_top_votes"].append(second_max_vote[1])

    def url(self):
        return URL_BASE + ",".join(self.stats["top_choices"])

    def verbose(self):
        result = self.url() + "\n"
        for i, c in enumerate(COLLECTIONS):
            if self.stats["top_votes"][i] == 0:
                result += c + " category needs your help, we currently have no reports for it. \n"
            elif self.stats["top_votes"][i] - self.stats["second_top_votes"][i] < 3:
                result += c + " category needs your verification, the top two votes are very close. \n"
        return result



