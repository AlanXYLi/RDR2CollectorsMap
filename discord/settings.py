COLLECTIONS = [
    "flower",
    "card",
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
    "card":6,
    "jewelry":6,
    "bottle":6,
    "egg":6,
    "arrow":6,
    "loom":6,
    "coin":6,
    "random":7
}

COLLECTION_SCORES = {
    "flower":1,
    "card":1,
    "jewelry":1,
    "bottle":1,
    "egg":1,
    "arrow":1,
    "loom":1,
    "coin":1,
    "random":2
}


URL_BASE = "https://jeanropke.github.io/RDR2CollectorsMap/?cycles="

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