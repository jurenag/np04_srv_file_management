import argparse
from srv_004_tools import monitor_directory     # The srv_004_tools.py file should
                                                # be in the same directory as this script

parser = argparse.ArgumentParser(description='Monitoring-script information')

parser.add_argument('--refresh_time_s',             '-rt',  type=float, required=False, default=5.0,    help='Refresh time in seconds (optional, the default value is 5.0)')
parser.add_argument('--path_to_target_directory',   '-td',  type=str,   required=True,                  help='Path to the directory to monitor. For a proper integration with the receiver side script, this path must be absolute.')
parser.add_argument('--path_to_log_file',           '-lf',  type=str,   required=True,                  help='Path to the log file where to append the results of the monitoring')
parser.add_argument('--waiting_time_s',             '-wt',  type=float, required=False, default=1.0,    help='Time, in second, to wait before trying to grab again the log file if it was not found before (optional, the default value is 1.0)')
parser.add_argument('--max_grab_trials',            '-gt',  type=int,   required=False, default=10,     help='Maximum number of trials to grab the log file before raising an exception (optional, the default value is 10)')

args = parser.parse_args()

monitor_directory( args.refresh_time_s, 
                   args.path_to_target_directory, 
                   args.path_to_log_file, 
                   args.waiting_time_s, 
                   args.max_grab_trials)