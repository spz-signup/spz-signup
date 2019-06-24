#!/bin/bash

docker exec -t spz-signup_postgres_1 pg_dumpall -c -U postgres

exit 0
