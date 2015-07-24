#!/usr/bin/env bash

FILE_LOCK=/home/spz/lock
FILE_DONE=/home/spz/initialized
FILE_PROCESS=/home/spz/inprocess

# echo function for stderr
echoerr() { echo "$@" 1>&2; }

init() {
    YES_I_KNOW_THAT_WORLD_ENDS_NOW=1 python init_db
}

# locked block
(
    flock --exclusive 200

    # init required?
    if [ ! -f $FILE_DONE ]; then
        # check if a process tried to init but somehow failed
        if [ -f $FILE_PROCESS ]; then
            echoerr 'Something went wrong. System is partial initialized and not recoverable!'
            echoerr 'Deletion and recreation of containers is the recommended solution.'
            exit 1
        fi
        touch $FILE_PROCESS

        init


        # remember that we reached this point
        touch $FILE_DONE
        rm -f $FILE_PROCESS
    fi
) 200>$FILE_LOCK

# run payload
exec $@
