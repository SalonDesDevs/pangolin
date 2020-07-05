import argparse
import logging

# cli options
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", action="count", help="increase verbosity", default=0
)
parser.add_argument(
    "-s", "--silent", action="count", help="decrease verbosity", default=0
)
parser.add_argument("--fps", action="store", type=int, default=60)
options = parser.parse_args()
verbosity = 10 * max(0, min(3 - options.verbose + options.silent, 5))

# logging configuration
stdout = logging.StreamHandler()
stdout.formatter = logging.Formatter(
    "{asctime} [{levelname}] <{name}:{funcName}> {message}", style="{"
)
logging.root.handlers.clear()
logging.root.addHandler(stdout)
logging.root.setLevel(verbosity)

from game import Game

game = Game(fps=options.fps)
game.start()
