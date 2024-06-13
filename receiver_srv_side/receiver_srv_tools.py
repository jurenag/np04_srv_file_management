import os
import math
import time

def grab_file(  path_to_file_to_grab : str,                 ## This function is duplicated. The other copy is in the tools module of the        
                waiting_time_s : float = 2,                 ## receiver side script. For the moment, they are duplicated for convenience             
                max_trials : int = 5) -> str:               ## (so that the import statements are simple). If you introduce a change here,            
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
    
def pop_first_line_from_file(   target_file_path : str,
                                waiting_time_s : float,
                                max_grab_trials : int) -> None:

    """
    This function gets the first line of the
    file whose path is given by the 
    'target_file_path' parameter, removes it 
    from the file and prints it. If the given
    file contains no lines, then nothing is
    printed.

    Parameters
    ----------
    target_file_path : str
        The path of the file whose first line
        will be removed and printed. If such
        file contains no lines, then nothing
        is printed by this function.
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

    if not os.path.isfile(target_file_path):
        raise Exception(f"In function pop_first_line_from_file(): {target_file_path} is not a valid file")
    
    waiting_time_s_ = abs(waiting_time_s)
    max_grab_trials_ = abs(max_grab_trials)

    target_file_name_while_writing = grab_file( target_file_path,   
                                                waiting_time_s_,    # If the function does not manage to grab the 
                                                max_grab_trials_)   # file after wating_time_s*(max_grab_trials - 1)
                                                                    # seconds, then it will raise an exception.
    with open(target_file_name_while_writing, 'r') as file:
        lines = file.readlines()

    if len(lines) > 0:  # If there are no lines in the given
                        # file, then do nothing and print nothing

        with open(target_file_name_while_writing, 'w') as file:
            file.writelines(lines[1:])

        print(lines[0]) # This should be grabbed by a bash script

    os.rename(target_file_name_while_writing, target_file_path) # In either case, rename the
    return                                                      # file back to its original name