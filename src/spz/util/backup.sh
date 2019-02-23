#!/usr/bin/env bash

set -euo pipefail

pg_dump --host=postgres --port=5432 --username=postgres spz \
    | xz --stdout --best \
    | gpg --batch --homedir=/state/gpg --sign --encrypt --default-key "SPZ Backup" --default-recipient "SPZ Admin" \
    > "$1"
