import os
import math
import time
from typing import Tuple, List

def get_file_names(input_folder_path : str) -> List[str]:

    """
    Gets an string, which should the path
    to a folder, and returns a list which contains
    the names of all the files in the folder.

    Parameters
    ----------
    input_folder_path : str
    
    Returns
    -------
    output : List[str]
    """

    if not os.path.isdir(input_folder_path):

        raise Exception(f"In function get_file_names(): {input_folder_path} is not a valid directory")
    
    output = []
    for filename in os.listdir(input_folder_path):
        if os.path.isfile(os.path.join(input_folder_path, filename)):
            output.append(filename)

    return output

def check_for_new_files(input_folder_path : str,
                        refresh_time_s : float) -> Tuple[bool, List[str]]:
    
    """
    Checks if after refresh_time_s seconds there are
    new files in the folder whose path is given by
    input_folder_path.

    Parameters
    ----------
    input_folder_path : str
        The path to the folder where we will check
        for new files.
    refresh_time_s : float
        The time interval in seconds between the
        retrieval of the file names and the checking
        for new files.

    Returns
    -------
    result : Tuple[bool, List[str]]
        A tuple where the first element is a boolean
        which is True if there is at least one new file
        in the folder, and False otherwise. The second 
        element is a list with the paths to the new
        files, which are built by joining the input 
        folder path and the names for the spotted new 
        files.
    """

    initial_file_names = get_file_names(input_folder_path)
    
    time.sleep(refresh_time_s)

    final_file_names = get_file_names(input_folder_path)

    fNewFiles = False
    new_file_paths = []

    for file_name in final_file_names:
        if file_name not in initial_file_names:
            fNewFiles = True
            new_file_paths.append(os.path.join(input_folder_path, file_name))

    return fNewFiles, new_file_paths

def last_line_is_emtpy(input_file_path : str) -> bool:

    """
    This function checks if the last line of the text
    file, whose path is given by the 'input_file_path'
    parameter, is empty.

    Parameters
    ----------
    filepath : str
        The path to the file to be checked

    Returns
    -------
    bool
        True if the last line of the file is emtpy,
        and False if Else
    """

    with open(input_file_path, 'r') as file:

        file.seek(0, 2)             # Moves the cursor a zero (0) 
                                    # offset from the end (2) of the file
        try:
            file.seek(file.tell() - 1)  # Moves the cursor back by 1 character
                                        # with respect to its previous position

        except ValueError:  # Happens if the input file is empty
            return True

        last_char = file.read(1)  # Read the last character
        
        return last_char == '\n'

def append_to_file( input_file_path : str, 
                    new_line : str) -> None:

    """
    This function adds a new line whose content matches
    the string given to the 'new_line' parameter, to the
    end of the file whose path is given by the 
    'input_file_path' parameter.

    Parameters
    ----------
    input_file_path : str
    new_line : str

    Returns
    -------
    None
    """

    if not os.path.isfile(input_file_path):
        raise Exception(f"In function append_to_file(): {input_file_path} is not a valid file")
    
    with open(input_file_path, 'a') as file:
        
        aux = new_line if last_line_is_emtpy(input_file_path) else ('\n'+new_line)
        file.write(aux)

    return
    
def monitor_directory( refresh_time_s : float,
                       path_to_target_directory : str,
                       path_to_log_file : str,
                       waiting_time_s : float,
                       max_grab_trials : int) -> None:
    
    """
    This function starts an infinite loop where the
    directory whose path is given by the 
    'path_to_target_directory' parameter is monitored.
    The monitoring process is done in such a way that
    the directory is checked every refresh_time_s seconds
    to see if there are new files. If so, then the name
    of such files is appended to the file whose path is
    given by the 'path_to_log_file' parameter.

    Parameters
    ----------
    refresh_time_s : float
        Time elapsed between two consecutive checks
        of the target directory
    path_to_target_directory : str
        The path to the directory to monitor
    path_to_log_file : str
        The path to the file where to append the
        names of the new files
    waiting_time_s : float
        This parameter is given to the 'waiting_time_s'
        parameter of the grab_file() function. Refer
        to its docstring for more information.
    max_grab_trials : int
        This parameter is given to the 'max_trials'
        parameter of the grab_file() function. Refer
        to its docstring for more information.

    Returns
    -------
    None
    """

    refresh_time_s_ = abs(refresh_time_s)

    if not os.path.isdir(path_to_target_directory):
        raise Exception(f"The given path to the target directory ({path_to_target_directory}) does not point to a valid directory.")

    if not os.path.isfile(path_to_log_file):
        raise Exception(f"The given path to the log file ({path_to_log_file}) does not point to a valid file.")

    waiting_time_s_ = abs(waiting_time_s)
    max_grab_trials_ = abs(max_grab_trials)

    while True: # Infinite loop, the execution of this
                # function should be keyboard-interrupted

        output =    check_for_new_files(path_to_target_directory,
                                        refresh_time_s_)
        
        if output[0]:   # If there are new files in the target directory

            log_file_name_while_writing = grab_file(    path_to_log_file,   
                                                        waiting_time_s_,    # If the function does not manage to grab the 
                                                        max_grab_trials_)   # file after wating_time_s*(max_grab_trials - 1)
                                                                            # seconds, then it will raise an exception.
            for new_file_path in output[1]:

                append_to_file( log_file_name_while_writing, 
                                new_file_path)
                
            os.rename(log_file_name_while_writing, path_to_log_file)    # Rename the log file back to 
                                                                        # its original name when we are
                                                                        # done with the writing process
    return None     # Never reached

def grab_file(  path_to_file_to_grab : str,         ## This function is duplicated. The other copy is in the tools module of the
                waiting_time_s : float = 2,         ## receiver side script. For the moment, they are duplicated for convenience 
                max_trials : int = 5) -> str:       ## (so that the import statements are simple). If you introduce a change here,
                                                    ## consider if you should introduce it also to the other copy.
    """
    This function tries to grab the file whose path is
    given by the 'path_to_file_to_grab' parameter, meaning
    that if such file is found, then such file is renamed
    by adding the '.writing' suffix. If the file is not
    found this function waits for waiting_time_s seconds
    before trying again. If this function is unable to find
    the given file after max_trials trials, then it raises
    an exception.

    Parameters
    ----------
    path_to_file_to_grab : str
        The path to the file to grab
    waiting_time_s : float
        The time to wait before trying again to grab
        the file
    max_trials : int
        The maximum number of trials before raising an
        exception

    Returns
    -------
    str
        The path to the grabbed file, which is the same
        as the given path but having appended the
        '.writing' suffix
    """

    max_trials_ = math.ceil(max_trials)
    waiting_time_s_ = abs(waiting_time_s)

    fGrabbedTheFile = False
    trials_done = 0
    
    while not fGrabbedTheFile and trials_done < max_trials_:

        file_name_while_writing = path_to_file_to_grab + ".writing"

        try:    # Another process could have renamed the file so that different writings 
                # do not collide. In that case, the os.rename() function will not find 
                # the file to rename, and will raise a FileNotFoundError. If that's the 
                # case, just wait a certain waiting time and try again.

            os.rename(path_to_file_to_grab, file_name_while_writing)

        except FileNotFoundError:
            
            trials_done += 1

            if trials_done < max_trials_:
                time.sleep(waiting_time_s_) # Do not sleep if the maximum number
                                            # of trials has already been reached

        else:
            
            fGrabbedTheFile = True

    if not fGrabbedTheFile:

        raise Exception(f"In function grab_file(): could not grab the file {path_to_file_to_grab} after {max_trials_} trial(s) in {waiting_time_s_*(max_trials_ - 1)} seconds")
    
    else:

        return file_name_while_writing