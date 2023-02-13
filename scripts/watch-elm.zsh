#!/usr/bin/env zsh
# vim: expandtab:
#
# __        __    _       _       _____ _           
# \ \      / /_ _| |_ ___| |__   | ____| |_ __ ___  
#  \ \ /\ / / _` | __/ __| '_ \  |  _| | | '_ ` _ \ 
#   \ V  V / (_| | || (__| | | | | |___| | | | | | |
#    \_/\_/ \__,_|\__\___|_| |_| |_____|_|_| |_| |_|
#                                                   

FILE=.watch-elm.hash
touch $FILE

while true; do
    HASH=$(shasum elm/**/*.elm)

    if [[ $HASH != $(cat $FILE) ]]; then
        echo "\n\nNEW CHANGES $(date +%H:%M:%S)\n"
        make build-debug-elm
    fi

    echo -n $HASH > $FILE
    sleep 1
done
