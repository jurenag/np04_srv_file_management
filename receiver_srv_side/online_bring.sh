#!/bin/bash

# Check if the user name is provided
if [ -z "$1" ]; then
    echo "The user name was not provided. Ending the script."
    return
fi

USER_NAME="$1"

# Check if the file path is provided
if [ -z "$2" ]; then
    echo "The target file was not provided. Ending the script."
    return
fi

# Check if the file exists
if [ ! -f "$2" ]; then
    echo "File not found: $2"
    return
fi

TARGET_FILEPATH="$2"

# Check if the destination folder path is provided
if [ -z "$3" ]; then
    echo "The destination folder path not provided. Ending the script."
    return
fi

# Check if the destination folder exists
if [ ! -d "$3" ]; then
    echo "Folder not found: $3"
    return
fi

DESTINATION_FOLDERPATH="$3"

# Check if the refresh time is provided
if [ -z "$4" ]; then
    echo "The refresh time was not provided. Ending the script."
    return
fi

REFRESH_TIME="$4"

while true; do

    NEW_FILE_PATH=$(python3 pop_first_line.py -tf $TARGET_FILEPATH) # Won't print anything 
                                                                    # if the target file is empty

    if [ -n "$NEW_FILE_PATH" ]; then                                                 	    # Only copy if the length 
        echo "Copying np04-srv-004:$NEW_FILE_PATH to $DESTINATION_FOLDERPATH" by running:   # of $NEW_FILE_PATH is non-zero
	    echo "    scp $USER_NAME@np04-srv-004:$NEW_FILE_PATH $DESTINATION_FOLDERPATH"

        scp $USER_NAME@np04-srv-004:$NEW_FILE_PATH $DESTINATION_FOLDERPATH  # Assuming that $NEW_FILE_PATH is an absolute
                                                                            # path within the np04-srv-004 remote server
    fi

    sleep $REFRESH_TIME

done
