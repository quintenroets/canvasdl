import argparse
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--configure",
        default=False,
        const=True,
        help="Create new config file",
        action="store_const",
    )
    # don't parse arguments if invoked with pytest
    parser_args = ([],) if "pytest" in sys.modules else ()
    args = parser.parse_args(*parser_args)
    return args
