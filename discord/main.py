# python 3.8, dependencies on top of vanilla python: pip install discord.py

import threading
import TOKENS

from score import Scores
from settings import *
from cycle import Cycle
from bot import PostOfficerClient

if __name__ == "__main__":
    cycle = Cycle()
    scoreboard = Scores()
    client = PostOfficerClient(cycle=cycle, score_obj=Scores)

    threads = [
        threading.Thread(target=cycle.reset_loop),
        threading.Thread(target=client.run, args=(TOKENS.token,)),
    ]

    for t in threads:
        t.start()

    while(1):
        pass