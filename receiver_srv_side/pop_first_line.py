import argparse

from receiver_srv_tools import pop_first_line_from_file     # The receiver_srv_tools.py file should
                                                            # be in the same directory as this script

parser = argparse.ArgumentParser(description='This script gets the first line of a given file, removes it from the file and returns it.')

parser.add_argument('--target_file',        '-tf',  type=str,   required=True,                  help='Path to the target file')
parser.add_argument('--waiting_time_s',     '-wt',  type=float, required=False, default=1.0,    help='Time, in second, to wait before trying to grab again the target file if it was not found before (optional, the default value is 1.0)')
parser.add_argument('--max_grab_trials',    '-gt',  type=int,   required=False, default=10,     help='Maximum number of trials to grab the target file before raising an exception (optional, the default value is 10)')

args = parser.parse_args()

pop_first_line_from_file(   args.target_file,
                            args.waiting_time_s, 
                            args.max_grab_trials)