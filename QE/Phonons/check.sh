#!/bin/sh
PREFIX='w'
TMP_DIR='./tmp'
for q in `seq 1 29 ` ; do
        state=$(grep 'JOB DONE.' ph.$q.out)
        echo "$q $state"
done
