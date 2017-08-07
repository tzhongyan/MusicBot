#!/bin/bash

TARGET_DIR='audio_cache'
MAX_DIR_SIZE=5000000

if [ ! -d $TARGET_DIR ]; then echo "$TARGET_DIR does not exists"; exit; fi
cd $TARGET_DIR
DIR_SIZE=`du -s . | cut -f 1`

if [ "$DIR_SIZE" -gt "$MAX_DIR_SIZE" ]
    then
    echo "$DIR_SIZE > $MAX_DIR_SIZE"
    echo "Delete extra files"
    ls -ltu | tail -n 100 | tr -s ' ' | cut -d ' ' -f 9 | xargs rm
    echo "Done!"
    else
    echo "$DIR_SIZE < $MAX_DIR_SIZE"
    echo "Nothing to delete"
fi
