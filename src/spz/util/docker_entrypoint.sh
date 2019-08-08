#!/usr/bin/env bash

FILE_LOCK=/state/lock
FILE_DONE=/state/initialized
FILE_PROCESS=/state/inprocess

# echo function for stderr
echoerr() { echo "$@" 1>&2; }

# test if connection is reachable
# usage: test_connection_by_protocol PROTO URI
#     PROTO: {tcp,udp}
#     URI: HOST:PORT
#
# return 1 on success, 0 otherwise
test_connection_by_protocol()  {
    address=$(echo $2 | sed 's/:.*//')
    port=$(echo $2 | sed 's/[^:]*://')
    printf "$1://$address:$port..."

    # use builtin bash function,
    # emulate `timeout` because our busybox version does not return exit
    # code of its child
    bash -c "cat < /dev/null > /dev/$1/$address/$port" 2> /dev/null &
    pid=$!
    bash -c "sleep 5; kill $pid" 2> /dev/null &
    wait $pid
    if [ $? == 0 ]; then
        echo YES
        return 1
    else
        echo NO
        return 0
    fi
}

# test if connection is reachable
# usage: test_connection NAME URI
#     NAME: name of the conneciton
#     URI: {tcp,udp}://HOST:PORT
#
# return 1 on success, 0 otherwise
test_connection() {
    printf "Test $1..."

    # TCP or UDP?
    if [[ $2 =~ ^tcp://.*$ ]]; then
        address_port=$(echo $2 | sed 's/tcp:\/\///')
        test_connection_by_protocol tcp $address_port
        return $?
    elif [[ $2 =~ ^udp://.*$ ]]; then
        address_port=$(echo $2 | sed 's/udp:\/\///')
        test_connection_by_protocol udp $address_port
        return $?
    fi

    # always succeed for unkown protocols
    return 1
}

# wait for all ports described in ENV variables of the form [A-Z]*_PORT
wait_for_services() {
    echo "Check if all services are reachable:"
    ok=0

    while [[ $ok == 0 ]]; do
        sleep 2
        ok=1
        for e in $(printenv); do
            # still ok or can we skip that cycle?
            if [[ $ok == 1 ]]; then
                k=$(echo $e | sed 's/=.*//')
                if [[ $k =~ ^[A-Z]*_PORT$  ]]; then
                    v=$(echo $e | sed 's/[^=]*=//')
                    test_connection $k $v
                    ok=$?
                fi
            fi
        done
    done
    echo "DONE, all services are up"
}

init() {
    echo "run global first run init"

    # setup DB
    PGPASSWORD=mysecretpassword psql --host=postgres --port=5432 --username=postgres --command="CREATE DATABASE spz;"
    YES_I_KNOW_THAT_WORLD_ENDS_NOW=1 python -m util.init_db

    # build+compress assets
    python -m util.build_assets
    gzip --keep --recursive --force --best spz/static

    echo "finished initialization"
}

wait_for_services

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

        # update python documentation
        bash util/build_docs.sh

        # remember that we reached this point
        touch $FILE_DONE
        rm -f $FILE_PROCESS
    fi
) 200>$FILE_LOCK

# run payload
exec $@
