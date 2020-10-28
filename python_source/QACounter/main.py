import argparse
from src.script.block_dim_counter import BlockDimCounter
from src.script.block_name_counter import BlockNameCounter
from src.script.mtext_counter import MTextCounter


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        type=str,
                        choices=["bnc", "mtc", "bdc"],
                        nargs='*',
                        help='Support counter tools are: '
                             '1. bnc (BlockNameCounter) - Counts names of a BlockReference and '
                             'tally\'s each unique names '
                             '2. mtc (MTextCounter) - Counts all the Mtext and tally each unique string value'
                             '3. bdc (BlockDimCounter) - Counts all the polylines inside the block and '
                             'tally each with width and height of the polyline')
    args = parser.parse_args()
    if args.s == "bnc":
        script = BlockNameCounter()
    elif args.s == "mtc":
        script = MTextCounter()
    elif args.s == "bdc":
        script = BlockDimCounter()
    else:
        print("Not supported.")
        script = None
    try:
        script.iter_input()
    except Exception:
        pass
