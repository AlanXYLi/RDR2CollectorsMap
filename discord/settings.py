from datetime import timedelta, datetime

COLLECTION_SETTINGS = {  # category: (cycle_count, score)
    "flower": (6, 1),
    "card": (6, 1),
    "jewelry": (6, 1),
    "bottle": (6, 1),
    "egg": (6, 1),
    "arrow": (6, 1),
    "loom": (6, 1),
    "coin": (6, 1),
    "random": (6, 1),
}

COLLECTIONS = list(COLLECTION_SETTINGS.keys())
COLLECTIONS_CYCLE_COUNT = {k: v[0] for k, v in COLLECTION_SETTINGS.items()}
COLLECTION_SCORES = {k: v[1] for k, v in COLLECTION_SETTINGS.items()}

REPO_UPDATE_EVENTS = [timedelta(seconds=5)]  # first update soon after cycle reset to reset away old data
for i in range(1, 10):
    REPO_UPDATE_EVENTS.append(timedelta(minutes=i))  # every minute during first 10
for i in range(10, 60, 10):
    REPO_UPDATE_EVENTS.append(timedelta(minutes=i))  # every 10 minutes during first hour
for i in range(60, 60 * 24, 30):
    REPO_UPDATE_EVENTS.append(timedelta(minutes=i))  # every 30 minutes afterwards
REPO_UPDATE_EVENTS.append(timedelta(days=1) - timedelta(minutes=5))  # final update of the day

ADMIN_UPDATE_QUOTA = 999
DAILY_UPDATE_QUOTA = 20

URL_BASE = "https://AlanXYLi.github.io/RDR2CollectorsMap/?cycles="

HELP_MSG = "Valid collection names are: " + ", ".join(COLLECTIONS) + "\n"\
           "To report all of today's cycle in the order listed above: $cycle 1,2,3,4,5,6,5,4,3 \n"\
            "\t You can enter either a partial list or complete list, $cycle 1,2,3 will only update first three. \n"\
           "To report some of today's cycle: $cycle name,name,...name num,num,...num \n" \
            "\t Example 1: $cycle loom 3 will report heirloom is on cycle 3 \n" \
            "\t Example 2: $cycle flower,loom,egg 3,2,1 will report flower on cycle 3, loom on  2 and egg on 1 \n"\
           "To get a link of the map with today's newest reported cycle list: $maplink \n"\
           "To get your rep: $rep \n" \
            "\t You earn 1 rep for each collection contribution, and 2 reps for random category contributio\n"\
            "\t The higher your rep, the more weight your report has\n"\


ERR_MSG = "Wrong format. Type $help for supported commands."

NEED_HELP_MSG = " categories need your help, we currently have no reports for them."

NEED_VERIFICATION_MSG = " categories need your verification, the top two votes of them are very close."

UPDATED_MSG = "Cycle updated! {} rep added. \n"

REP_MSG = "'s rep is: "

if __name__ == "__main__":
    pass
