#! /bin/bash

echo -n '{
    "test_data": {
        "_type": "choice",
        "_value": [
'
cat $1 | head -n -1 | cut -d " " -f1 | awk '{print "\"/gpfs/project/festi100/data/animals/'$2'/"$1"/test_data.h5\","}'
cat $1 | tail -1 | cut -d " " -f1 | awk '{print "\"/gpfs/project/festi100/data/animals/'$2'/"$1"/test_data.h5\""}'

echo -n '        ]
    }
}'


