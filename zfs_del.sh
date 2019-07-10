#!/usr/bin/env bash

# zfs_del.sh deletes all but the given amount of backup snapshots.


re='^[0-9]+$'
if [[ $1 =~ $re ]]
then
        snapshots=`zfs list -t snapshot -o name | grep "^backup@" | tail -r | tail -n +$1 | xargs echo`
        set -f
        array=(${snapshots// / })

        if [ -z "$array" ]; then
                echo "Seems like there are less than $1 snapshots."
        else
                # echo snapshot list for verification
                for i in "${!array[@]}"
                do
                        echo "${array[i]}"
                done

                read -p "Really delete those snapshots? [y/N] " -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]
                then
                        for i in "${!array[@]}"
                        do
                                echo "destroying snapshot: ${array[i]}"
                                zfs destroy -r "${array[i]}"
                        done
                fi
        fi
else
        echo "usage: $0 <num of snapshots to keep>"
fi
